"""
data/transparent/*.png (투명 배경 + #000000 에린어 글리프)에서
디스코드 커스텀 이모지 표준 규격(128x128 정사각형 PNG, 256KB 이하)에 맞춘
에린어 이모지 이미지 세트 및 일괄 등록용 ZIP 아카이브를 생성하는 스크립트입니다.

지원 스타일:
1. outline (기본 추천) : 밝은 흰색(#F8FAFF) 글리프 + 진한 남색(#101522) 외곽선 (디스코드 다크/라이트 모드 모두 선명)
2. slate              : 마비노기 인게임 비석(슬레이트) 둥근 타일 배경 + 밝은 각인(#EEF4FF) 글리프
3. white              : 순수 흰색(#FFFFFF) 투명 배경 글리프 (디스코드 다크 모드용)
4. black              : 순수 검은색(#000000) 투명 배경 글리프 (디스코드 라이트 모드용)

지원 패키지 구성 (디스코드 서버 기본 이모지 슬롯 50개 제한 고려):
- 40종 전체 세트 (full_40)      : 기본자음(14) + 쌍자음(5) + 기본모음(10) + 복합모음(11) = 40개
- 31종 필수 세트 (essential_31) : 기본자음(14) + 쌍자음(5) + 기본모음(10) + 반점모음(ㅒ,ㅖ 2) = 31개 (나머지 복합모음 9종은 조합 표기)
- 26종 최소 세트 (minimal_26)   : 기본자음(14) + 기본모음(10) + 반점모음(ㅒ,ㅖ 2) = 26개 (쌍자음·복합모음 모두 조합 표기)
"""

import json
import shutil
import zipfile
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, gaussian_filter

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TRANS_DIR = DATA_DIR / "transparent"
EMOJI_DIR = DATA_DIR / "discord_emoji"

DOCS_DATA_DIR = BASE_DIR / "docs" / "data"
DOCS_EMOJI_DIR = DOCS_DATA_DIR / "discord_emoji"

CANVAS_SIZE = 128

# 세트별 포함 자모 정의
BASIC_CONSONANTS = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
DOUBLE_CONSONANTS = ["ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"]
BASIC_VOWELS = ["ㅏ", "ㅓ", "ㅗ", "ㅜ", "ㅡ", "ㅣ", "ㅑ", "ㅕ", "ㅛ", "ㅠ"]
TICK_VOWELS = ["ㅒ", "ㅖ"]
COMPOUND_VOWELS = ["ㅐ", "ㅔ", "ㅚ", "ㅟ", "ㅘ", "ㅙ", "ㅝ", "ㅞ", "ㅢ"]

SET_DEFINITIONS = {
    "26": BASIC_CONSONANTS + BASIC_VOWELS + TICK_VOWELS,
    "31": BASIC_CONSONANTS + DOUBLE_CONSONANTS + BASIC_VOWELS + TICK_VOWELS,
    "40": BASIC_CONSONANTS + DOUBLE_CONSONANTS + BASIC_VOWELS + TICK_VOWELS + COMPOUND_VOWELS,
}

STYLES = ["outline", "slate", "white", "black"]


def get_discord_code(qwerty_key: str, prefix: str = "erin_") -> str:
    """
    대소문자 구분이 없는 Windows 파일시스템 및 디스코드 이모지 자동완성에 맞춰
    Shift 대문자 키(R, E, Q, T, W, O, P)는 소문자 2회 반복(rr, ee, qq, tt, ww, oo, pp)으로 매핑합니다.
    """
    suffix = qwerty_key.lower() * 2 if qwerty_key.isupper() else qwerty_key.lower()
    return f"{prefix}{suffix}"


def place_glyph_alpha(glyph_img: Image.Image, target_height: int) -> np.ndarray:
    """원본 투명 PNG의 비율을 유지한 채 target_height로 리사이즈하여 128x128 중앙에 배치한 알파 배열(0.0~1.0)을 반환합니다."""
    orig_w, orig_h = glyph_img.size
    scale = target_height / float(orig_h)
    new_w = max(1, int(round(orig_w * scale)))
    new_h = max(1, int(round(orig_h * scale)))

    resized = glyph_img.resize((new_w, new_h), Image.Resampling.LANCZOS).convert("RGBA")
    alpha_crop = np.array(resized, dtype=np.float32)[:, :, 3] / 255.0

    canvas_alpha = np.zeros((CANVAS_SIZE, CANVAS_SIZE), dtype=np.float32)
    x0 = (CANVAS_SIZE - new_w) // 2
    y0 = (CANVAS_SIZE - new_h) // 2

    # 캔버스 범위 클리핑 안전 처리
    cx0 = max(0, x0)
    cy0 = max(0, y0)
    cx1 = min(CANVAS_SIZE, x0 + new_w)
    cy1 = min(CANVAS_SIZE, y0 + new_h)

    sx0 = cx0 - x0
    sy0 = cy0 - y0
    sx1 = sx0 + (cx1 - cx0)
    sy1 = sy0 + (cy1 - cy0)

    canvas_alpha[cy0:cy1, cx0:cx1] = alpha_crop[sy0:sy1, sx0:sx1]
    return canvas_alpha


def composite_over(fg_rgba: np.ndarray, bg_rgba: np.ndarray) -> np.ndarray:
    """표준 Porter-Duff source-over 알파 합성 (입력/출력 shape: HxWx4, 범위: 0.0~1.0)"""
    fg_a = fg_rgba[:, :, 3:4]
    bg_a = bg_rgba[:, :, 3:4]
    out_a = fg_a + bg_a * (1.0 - fg_a)
    safe_a = np.where(out_a > 1e-6, out_a, 1.0)
    out_rgb = (fg_rgba[:, :, :3] * fg_a + bg_rgba[:, :, :3] * bg_a * (1.0 - fg_a)) / safe_a
    out_rgb = np.where(out_a > 1e-6, out_rgb, 0.0)
    return np.concatenate([out_rgb, out_a], axis=2)


def make_slate_badge_bg() -> np.ndarray:
    """128x128 캔버스에 들어갈 마비노기 비석(슬레이트) 스타일 둥근 사각형 배지 배경을 생성합니다."""
    yy, xx = np.mgrid[0:CANVAS_SIZE, 0:CANVAS_SIZE].astype(np.float32)
    center = (CANVAS_SIZE - 1) / 2.0
    half_size = 57.0  # 114x114 타일
    radius = 22.0

    dx = np.maximum(np.abs(xx - center) - (half_size - radius), 0.0)
    dy = np.maximum(np.abs(yy - center) - (half_size - radius), 0.0)
    dist = np.sqrt(dx * dx + dy * dy) - radius

    # 안티앨리어싱 외곽 마스크 및 테두리 마스크
    badge_alpha = np.clip(0.5 - dist, 0.0, 1.0)
    inner_mask = np.clip(-dist - 2.2, 0.0, 1.0)
    border_weight = badge_alpha * (1.0 - inner_mask)

    # 대각선 슬레이트 그라데이션 (#324a63 -> #3d5875 -> #2c4259)
    t = (xx + yy) / (2.0 * CANVAS_SIZE)
    c1 = np.array([0x32, 0x4A, 0x63], dtype=np.float32) / 255.0
    c2 = np.array([0x3D, 0x58, 0x75], dtype=np.float32) / 255.0
    c3 = np.array([0x2C, 0x42, 0x59], dtype=np.float32) / 255.0

    grad_rgb = np.where(
        (t < 0.5)[:, :, None],
        c1 + (c2 - c1) * (t * 2.0)[:, :, None],
        c2 + (c3 - c2) * ((t - 0.5) * 2.0)[:, :, None],
    )

    border_rgb = np.array([0x64, 0x86, 0xAC], dtype=np.float32) / 255.0
    rgb = grad_rgb * (1.0 - border_weight[:, :, None] * 0.65) + border_rgb * (border_weight[:, :, None] * 0.65)

    out = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 4), dtype=np.float32)
    out[:, :, :3] = rgb
    out[:, :, 3] = badge_alpha
    return out


SLATE_BG_CACHE = make_slate_badge_bg()


def render_emoji_style(glyph_img: Image.Image, style: str) -> Image.Image:
    """지정한 스타일(outline, slate, white, black)로 128x128 디스코드 이모지 이미지를 생성합니다."""
    if style == "slate":
        alpha = place_glyph_alpha(glyph_img, target_height=88)
        # 부드러운 음각 그림자
        shadow_a = gaussian_filter(np.roll(alpha, shift=2, axis=0), sigma=1.2) * 0.48
        shadow_rgba = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 4), dtype=np.float32)
        shadow_rgba[:, :, :3] = np.array([0x0C, 0x15, 0x22], dtype=np.float32) / 255.0
        shadow_rgba[:, :, 3] = shadow_a * SLATE_BG_CACHE[:, :, 3]

        fg_rgba = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 4), dtype=np.float32)
        fg_rgba[:, :, :3] = np.array([0xF0, 0xF6, 0xFF], dtype=np.float32) / 255.0
        fg_rgba[:, :, 3] = alpha

        comp = composite_over(shadow_rgba, SLATE_BG_CACHE)
        comp = composite_over(fg_rgba, comp)
        rgba_u8 = np.clip(np.round(comp * 255.0), 0, 255).astype(np.uint8)
        return Image.fromarray(rgba_u8, mode="RGBA")

    alpha = place_glyph_alpha(glyph_img, target_height=104)

    if style == "white":
        out = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 4), dtype=np.float32)
        out[:, :, :3] = 1.0
        out[:, :, 3] = alpha
        return Image.fromarray(np.clip(np.round(out * 255.0), 0, 255).astype(np.uint8), mode="RGBA")

    if style == "black":
        out = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 4), dtype=np.float32)
        out[:, :, 3] = alpha
        return Image.fromarray(np.clip(np.round(out * 255.0), 0, 255).astype(np.uint8), mode="RGBA")

    # style == "outline" (기본 추천: 다크/라이트 모드 겸용 외곽선)
    inside = alpha >= 0.42
    dist_outside = distance_transform_edt(~inside)
    stroke_radius = 4.6
    stroke_alpha = np.clip((stroke_radius + 0.7 - dist_outside) / 1.3, 0.0, 1.0)
    stroke_alpha = np.maximum(stroke_alpha, alpha)

    bg_stroke = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 4), dtype=np.float32)
    bg_stroke[:, :, :3] = np.array([0x10, 0x16, 0x24], dtype=np.float32) / 255.0
    bg_stroke[:, :, 3] = stroke_alpha

    fg_fill = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 4), dtype=np.float32)
    fg_fill[:, :, :3] = np.array([0xF8, 0xFA, 0xFF], dtype=np.float32) / 255.0
    fg_fill[:, :, 3] = alpha

    comp = composite_over(fg_fill, bg_stroke)
    return Image.fromarray(np.clip(np.round(comp * 255.0), 0, 255).astype(np.uint8), mode="RGBA")


def build_all_discord_emojis():
    mapping_path = DATA_DIR / "mapping.json"
    if not mapping_path.exists():
        raise FileNotFoundError(f"mapping.json을 찾을 수 없습니다: {mapping_path}")

    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    characters = mapping["characters"]

    EMOJI_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_EMOJI_DIR.mkdir(parents=True, exist_ok=True)

    # 1. 스타일별 40종 128x128 PNG 생성
    for style in STYLES:
        style_dir = EMOJI_DIR / style
        docs_style_dir = DOCS_EMOJI_DIR / style
        style_dir.mkdir(parents=True, exist_ok=True)
        docs_style_dir.mkdir(parents=True, exist_ok=True)

        for jamo, meta in characters.items():
            src_png = BASE_DIR / meta["transparent_image"]
            glyph_img = Image.open(src_png).convert("RGBA")
            emoji_img = render_emoji_style(glyph_img, style=style)

            discord_code = meta.get("discord_code") or get_discord_code(meta["qwerty"])
            out_path = style_dir / f"{discord_code}.png"
            emoji_img.save(out_path, format="PNG", optimize=True)
            shutil.copy2(out_path, docs_style_dir / f"{discord_code}.png")

    # 2. 스타일별 · 세트 크기별(40종 / 31종 / 26종) 일괄 업로드용 ZIP 패키지 생성
    zip_count = 0
    for style in STYLES:
        for set_key, jamo_list in SET_DEFINITIONS.items():
            zip_name = f"erin_discord_emoji_{style}_{set_key}.zip"
            zip_path = EMOJI_DIR / zip_name
            with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                for jamo in jamo_list:
                    meta = characters[jamo]
                    discord_code = meta.get("discord_code") or get_discord_code(meta["qwerty"])
                    img_path = EMOJI_DIR / style / f"{discord_code}.png"
                    zf.write(img_path, arcname=f"{discord_code}.png")
            shutil.copy2(zip_path, DOCS_EMOJI_DIR / zip_name)
            zip_count += 1

    print(
        f"디스코드 128x128 이모지 생성 완료: {len(STYLES)}종 스타일 x {len(characters)}자 = {len(STYLES) * len(characters)}개 PNG 및 {zip_count}개 ZIP 패키지 (docs/ 동기화 완료)"
    )


if __name__ == "__main__":
    build_all_discord_emojis()
