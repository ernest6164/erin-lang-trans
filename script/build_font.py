"""
data/transparent/*.png (투명 배경 + #000000 에린어 글리프 이미지)를 벡터 윤곽선(TrueType Quadratic Spline)으로 변환하여
단순 한글 자모(U+3131~U+3163)나 완성형 한글(U+AC00~U+D7A3), 영문자(A-Z, a-z)는 건드리지 않고
유니코드 Halfwidth and Fullwidth Forms 블록의 한글 자모 코드(U+FFA1 ~ U+FFDC)만 에린어로 표현하는
전용 폰트 파일(ErinLang.ttf, ErinLang.woff2)을 생성하는 스크립트입니다.

생성 결과물:
- data/ErinLang.ttf, docs/data/ErinLang.ttf
- data/ErinLang.woff2, docs/data/ErinLang.woff2
"""

import shutil
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import zoom, gaussian_filter
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

BASE_DIR = Path(__file__).resolve().parent.parent
TRANS_DIR = BASE_DIR / "data" / "transparent"
DATA_DIR = BASE_DIR / "data"
DOCS_DATA_DIR = BASE_DIR / "docs" / "data"

# 유니코드 Halfwidth and Fullwidth Forms 블록 내 한글 자모 (U+FFA1 ~ U+FFDC)
# 일반 한글 호환 자모(U+3131~U+3163)나 영문자(A-Z, a-z)와 충돌하지 않는 전용 코드 영역
SINGLE_JAMO_CODEPOINTS = {
    "ㄱ": 0xFFA1,
    "ㄲ": 0xFFA2,
    "ㄴ": 0xFFA4,
    "ㄷ": 0xFFA7,
    "ㄸ": 0xFFA8,
    "ㄹ": 0xFFA9,
    "ㅁ": 0xFFB1,
    "ㅂ": 0xFFB2,
    "ㅃ": 0xFFB3,
    "ㅅ": 0xFFB5,
    "ㅆ": 0xFFB6,
    "ㅇ": 0xFFB7,
    "ㅈ": 0xFFB8,
    "ㅉ": 0xFFB9,
    "ㅊ": 0xFFBA,
    "ㅋ": 0xFFBB,
    "ㅌ": 0xFFBC,
    "ㅍ": 0xFFBD,
    "ㅎ": 0xFFBE,
    "ㅏ": 0xFFC2,
    "ㅐ": 0xFFC3,
    "ㅑ": 0xFFC4,
    "ㅒ": 0xFFC5,
    "ㅓ": 0xFFC6,
    "ㅔ": 0xFFC7,
    "ㅕ": 0xFFCA,
    "ㅖ": 0xFFCB,
    "ㅗ": 0xFFCC,
    "ㅘ": 0xFFCD,
    "ㅙ": 0xFFCE,
    "ㅚ": 0xFFCF,
    "ㅛ": 0xFFD2,
    "ㅜ": 0xFFD3,
    "ㅝ": 0xFFD4,
    "ㅞ": 0xFFD5,
    "ㅟ": 0xFFD6,
    "ㅠ": 0xFFD7,
    "ㅡ": 0xFFDA,
    "ㅢ": 0xFFDB,
    "ㅣ": 0xFFDC,
}

# U+FFA1~U+FFDC 블록에 포함된 겹받침(11자)도 두 단자음 글리프를 나란히 조합하여 지원
COMPOUND_JONG_CODEPOINTS = {
    "ㄳ": (0xFFA3, ["ㄱ", "ㅅ"]),
    "ㄵ": (0xFFA5, ["ㄴ", "ㅈ"]),
    "ㄶ": (0xFFA6, ["ㄴ", "ㅎ"]),
    "ㄺ": (0xFFAA, ["ㄹ", "ㄱ"]),
    "ㄻ": (0xFFAB, ["ㄹ", "ㅁ"]),
    "ㄼ": (0xFFAC, ["ㄹ", "ㅂ"]),
    "ㄽ": (0xFFAD, ["ㄹ", "ㅅ"]),
    "ㄾ": (0xFFAE, ["ㄹ", "ㅌ"]),
    "ㄿ": (0xFFAF, ["ㄹ", "ㅍ"]),
    "ㅀ": (0xFFB0, ["ㄹ", "ㅎ"]),
    "ㅄ": (0xFFB4, ["ㅂ", "ㅅ"]),
}

UPM = 1000
ASCENT = 860
DESCENT = -140


def extract_marching_squares_contours(alpha_2d: np.ndarray, threshold: float = 0.46):
    """
    2D 스칼라 필드(Y-up 좌표계로 변환된 알파 맵)에서 Marching Squares로
    내부(>=threshold)를 오른쪽에 두는 유향 등고선 루프들을 추출합니다.
    - 외곽선: 시계 방향(CW, TrueType 외곽선 표준)
    - 내부 구멍(ㅇ, ㅁ, ㅂ, ㅎ, ㅏ 등): 반시계 방향(CCW, TrueType 홀 표준)
    """
    # 테두리가 항상 0이 되도록 패딩
    field = np.pad(alpha_2d, pad_width=2, mode="constant", constant_values=0.0)
    h, w = field.shape

    segments = {}

    def interp(v1, v2):
        dv = v2 - v1
        if abs(dv) < 1e-8:
            return 0.5
        return float(np.clip((threshold - v1) / dv, 0.0, 1.0))

    # Y-up 좌표계: row j가 아래에서 위로 증가하도록 field를 이미 뒤집어서 전달받음
    for j in range(h - 1):
        for i in range(w - 1):
            v00 = field[j, i]          # bottom-left (i, j)
            v10 = field[j, i + 1]      # bottom-right (i+1, j)
            v11 = field[j + 1, i + 1]  # top-right (i+1, j+1)
            v01 = field[j + 1, i]      # top-left (i, j+1)

            b0 = 1 if v00 >= threshold else 0
            b1 = 2 if v10 >= threshold else 0
            b2 = 4 if v11 >= threshold else 0
            b3 = 8 if v01 >= threshold else 0
            case = b0 | b1 | b2 | b3
            if case == 0 or case == 15:
                continue

            # 각 변 위의 보간점 (소수점 정밀도 고정으로 정점 키 일치 보장)
            p_bottom = (round(i + interp(v00, v10), 4), round(float(j), 4))
            p_right = (round(float(i + 1), 4), round(j + interp(v10, v11), 4))
            p_top = (round(i + interp(v01, v11), 4), round(float(j + 1), 4))
            p_left = (round(float(i), 4), round(j + interp(v00, v01), 4))

            # 내부(>=threshold)가 진행 방향의 오른쪽에 위치하도록 세그먼트 방향 설정 (외곽선 CW, 구멍 CCW)
            edges = []
            if case == 1:      # v00만 내부
                edges.append((p_left, p_bottom))
            elif case == 2:    # v10만 내부
                edges.append((p_bottom, p_right))
            elif case == 3:    # v00, v10 내부
                edges.append((p_left, p_right))
            elif case == 4:    # v11만 내부
                edges.append((p_right, p_top))
            elif case == 5:    # v00, v11 안장점
                center = 0.25 * (v00 + v10 + v11 + v01)
                if center >= threshold:
                    edges.append((p_left, p_top))
                    edges.append((p_right, p_bottom))
                else:
                    edges.append((p_left, p_bottom))
                    edges.append((p_right, p_top))
            elif case == 6:    # v10, v11 내부
                edges.append((p_bottom, p_top))
            elif case == 7:    # v01만 외부
                edges.append((p_left, p_top))
            elif case == 8:    # v01만 내부
                edges.append((p_top, p_left))
            elif case == 9:    # v00, v01 내부
                edges.append((p_top, p_bottom))
            elif case == 10:   # v10, v01 안장점
                center = 0.25 * (v00 + v10 + v11 + v01)
                if center >= threshold:
                    edges.append((p_bottom, p_left))
                    edges.append((p_top, p_right))
                else:
                    edges.append((p_bottom, p_right))
                    edges.append((p_top, p_left))
            elif case == 11:   # v11만 외부
                edges.append((p_top, p_right))
            elif case == 12:   # v11, v01 내부
                edges.append((p_right, p_left))
            elif case == 13:   # v10만 외부
                edges.append((p_right, p_bottom))
            elif case == 14:   # v00만 외부
                edges.append((p_bottom, p_left))

            for start_pt, end_pt in edges:
                if start_pt != end_pt:
                    segments.setdefault(start_pt, []).append(end_pt)

    loops = []
    while segments:
        start_pt = next(iter(segments))
        curr = start_pt
        loop = [curr]
        while True:
            next_list = segments.get(curr)
            if not next_list:
                break
            nxt = next_list.pop()
            if not next_list:
                del segments[curr]
            if nxt == start_pt:
                break
            loop.append(nxt)
            curr = nxt
        if len(loop) >= 6:
            loops.append(loop)

    return loops


def simplify_rdp_closed(points: list, epsilon: float) -> list:
    """폐곡선 정점 열을 Ramer-Douglas-Peucker 알고리즘으로 단순화합니다."""
    pts = np.array(points, dtype=np.float64)
    if len(pts) <= 6:
        return points

    # 가장 먼 두 점을 기준으로 두 구간으로 나누어 RDP 수행
    d0 = np.sum((pts - pts[0]) ** 2, axis=1)
    idx1 = int(np.argmax(d0))
    d1 = np.sum((pts - pts[idx1]) ** 2, axis=1)
    idx2 = int(np.argmax(d1))

    if idx1 > idx2:
        idx1, idx2 = idx2, idx1

    def rdp_open(arr):
        if len(arr) <= 2:
            return arr.tolist()
        start, end = arr[0], arr[-1]
        line_vec = end - start
        line_len = np.hypot(line_vec[0], line_vec[1])
        if line_len < 1e-8:
            dists = np.hypot(arr[:, 0] - start[0], arr[:, 1] - start[1])
        else:
            dists = np.abs(
                line_vec[1] * arr[:, 0] - line_vec[0] * arr[:, 1] + end[0] * start[1] - end[1] * start[0]
            ) / line_len
        max_idx = int(np.argmax(dists))
        if dists[max_idx] > epsilon:
            left = rdp_open(arr[: max_idx + 1])
            right = rdp_open(arr[max_idx:])
            return left[:-1] + right
        return [start.tolist(), end.tolist()]

    part1 = pts[idx1 : idx2 + 1]
    part2 = np.vstack([pts[idx2:], pts[: idx1 + 1]])

    s1 = rdp_open(part1)
    s2 = rdp_open(part2)
    merged = s1[:-1] + s2[:-1]
    return merged


def draw_loops_to_pen(loops: list, pen: TTGlyphPen, scale_to_font: float, pad_offset: float, x_shift: float = 0.0, y_shift: float = -60.0):
    """단순화된 다각형 루프를 부드러운 TrueType 2차 베지어 곡선(qCurveTo)으로 변환하여 기록합니다."""
    for loop in loops:
        simplified = simplify_rdp_closed(loop, epsilon=0.85)
        if len(simplified) < 4:
            continue

        # 폰트 좌표계로 스케일링
        fpts = []
        for x, y in simplified:
            fx = round((x - pad_offset) * scale_to_font + x_shift)
            fy = round((y - pad_offset) * scale_to_font + y_shift)
            if not fpts or fpts[-1] != (fx, fy):
                fpts.append((fx, fy))

        if len(fpts) < 3:
            continue

        # 면적이 너무 작은 노이즈 제거
        area = 0.0
        n = len(fpts)
        for k in range(n):
            x1, y1 = fpts[k]
            x2, y2 = fpts[(k + 1) % n]
            area += x1 * y2 - x2 * y1
        if abs(area) * 0.5 < 120:
            continue

        # 코너 여부에 따라 직선/곡선 혼합 또는 중점 스플라인 적용
        pen.moveTo(fpts[0])
        for k in range(n):
            p_prev = fpts[(k - 1) % n]
            p_curr = fpts[k]
            p_next = fpts[(k + 1) % n]

            v1 = (p_curr[0] - p_prev[0], p_curr[1] - p_prev[1])
            v2 = (p_next[0] - p_curr[0], p_next[1] - p_curr[1])
            l1 = (v1[0] ** 2 + v1[1] ** 2) ** 0.5
            l2 = (v2[0] ** 2 + v2[1] ** 2) ** 0.5

            mid = (round((p_curr[0] + p_next[0]) * 0.5), round((p_curr[1] + p_next[1]) * 0.5))
            if l1 > 0 and l2 > 0:
                cos_ang = (v1[0] * v2[0] + v1[1] * v2[1]) / (l1 * l2)
                if cos_ang < 0.35 or l1 > 90 or l2 > 90:
                    pen.lineTo(p_curr)
                    pen.lineTo(mid)
                else:
                    pen.qCurveTo(p_curr, mid)
            else:
                pen.lineTo(p_curr)
        pen.closePath()


def trace_jamo_image(img_path: Path):
    """투명 PNG 파일에서 윤곽선 루프와 폰트 단위 폭(advance width)을 추출합니다."""
    im = Image.open(img_path).convert("RGBA")
    alpha = np.array(im)[:, :, 3].astype(np.float32) / 255.0

    # Y-up 변환 (이미지 상단이 폰트 상단이 되도록 상하 반전)
    alpha_yup = np.flipud(alpha)

    # 6배 슈퍼샘플링 + 가우시안 스무딩으로 계단 현상 제거
    upsample = 6
    up_alpha = zoom(alpha_yup, upsample, order=3)
    up_alpha = gaussian_filter(up_alpha, sigma=1.15)

    loops = extract_marching_squares_contours(up_alpha, threshold=0.45)

    # 원본 높이 86px -> 폰트 높이 약 880 유닛 (베이스라인 아래 여유 포함)
    font_height_span = 880.0
    scale_to_font = font_height_span / (im.height * upsample)
    glyph_w = round(im.width * (font_height_span / im.height))
    side_bearing = 24
    advance_width = glyph_w + side_bearing * 2

    return loops, scale_to_font, advance_width, side_bearing


def build_erin_font():
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    glyph_order = [".notdef", "space", "uni3000"]
    cmap = {
        0x0020: "space",
        0x3000: "uni3000",
    }
    glyphs = {}
    metrics = {}

    # 1. .notdef 및 공백 글리프
    pen_notdef = TTGlyphPen(None)
    glyphs[".notdef"] = pen_notdef.glyph()
    metrics[".notdef"] = (500, 0)

    pen_space = TTGlyphPen(None)
    glyphs["space"] = pen_space.glyph()
    metrics["space"] = (420, 0)

    pen_fw_space = TTGlyphPen(None)
    glyphs["uni3000"] = pen_fw_space.glyph()
    metrics["uni3000"] = (650, 0)

    # 2. 40개 에린어 기본/쌍자음/복합모음 글리프 생성 (U+FFA1 ~ U+FFDC)
    traced_cache = {}
    for jamo, cp in SINGLE_JAMO_CODEPOINTS.items():
        gname = f"uni{cp:04X}"
        glyph_order.append(gname)
        cmap[cp] = gname

        img_path = TRANS_DIR / f"{jamo}.png"
        loops, scale_to_font, adv_w, sb = trace_jamo_image(img_path)
        traced_cache[jamo] = (loops, scale_to_font, adv_w, sb)

        pen = TTGlyphPen(None)
        draw_loops_to_pen(loops, pen, scale_to_font, pad_offset=2.0, x_shift=float(sb), y_shift=-50.0)
        glyphs[gname] = pen.glyph()
        metrics[gname] = (adv_w, sb)

    # 3. 겹받침 11종 (U+FFA3 등)도 두 자음을 나란히 배치하여 지원
    for jong, (cp, parts) in COMPOUND_JONG_CODEPOINTS.items():
        gname = f"uni{cp:04X}"
        glyph_order.append(gname)
        cmap[cp] = gname

        pen = TTGlyphPen(None)
        cur_x = 24.0
        for idx, p_jamo in enumerate(parts):
            loops, scale_to_font, adv_w, sb = traced_cache[p_jamo]
            draw_loops_to_pen(loops, pen, scale_to_font, pad_offset=2.0, x_shift=cur_x, y_shift=-50.0)
            cur_x += (adv_w - sb * 2) + (18.0 if idx == 0 else 24.0)

        glyphs[gname] = pen.glyph()
        metrics[gname] = (round(cur_x), 24)

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ASCENT, descent=DESCENT)
    fb.setupNameTable({
        "familyName": "ErinLang",
        "styleName": "Regular",
        "uniqueFontIdentifier": "ErinLang-Regular",
        "fullName": "ErinLang Regular",
        "psName": "ErinLang-Regular",
        "version": "Version 1.0",
    })
    fb.setupOS2(
        sTypoAscender=ASCENT,
        sTypoDescender=DESCENT,
        sTypoLineGap=100,
        usWinAscent=ASCENT,
        usWinDescent=abs(DESCENT),
        sxHeight=520,
        sCapHeight=760,
    )
    fb.setupPost()

    ttf_path = DATA_DIR / "ErinLang.ttf"
    woff2_path = DATA_DIR / "ErinLang.woff2"

    fb.save(str(ttf_path))

    # WOFF2 웹폰트도 함께 저장
    fb.font.flavor = "woff2"
    fb.save(str(woff2_path))

    shutil.copy2(ttf_path, DOCS_DATA_DIR / "ErinLang.ttf")
    shutil.copy2(woff2_path, DOCS_DATA_DIR / "ErinLang.woff2")

    print(f"에린어 전용 폰트 생성 완료: {ttf_path.name}, {woff2_path.name} (총 {len(cmap)}개 글리프)")


if __name__ == "__main__":
    build_erin_font()
