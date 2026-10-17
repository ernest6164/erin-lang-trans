"""
import 폴더의 에린어 변환표(19d00ea17f157c624.webp)에서
개별 에린어 문자 이미지를 추출하여 투명 배경 + 검은색(#000000) 글리프 형태로
data/transparent/ 및 GitHub Pages 배포용 docs/data/transparent/ 폴더에 저장하는 스크립트입니다.

생성 결과물:
- data/transparent/<자모>.png, docs/data/transparent/<자모>.png : 투명 배경 + 검은색(#000000) 글리프 이미지 (높이 86 고정, 좌우 여백 최적화)
- data/mapping.json, docs/data/mapping.json : 한글 자모, 영문(두벌식 쿼티) 키, 전용 유니코드(U+FFA1~U+FFDC), 에린어 고유 맞춤법(ㅔ=ㅣ+ㅏ, ㅒ/ㅖ 반점 규칙) 및 대칭 메타데이터
"""

import json
import shutil
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
IMPORT_IMAGE = BASE_DIR / "import" / "19d00ea17f157c624.webp"
DATA_DIR = BASE_DIR / "data"
TRANSPARENT_DIR = DATA_DIR / "transparent"

DOCS_DIR = BASE_DIR / "docs"
DOCS_DATA_DIR = DOCS_DIR / "data"
DOCS_TRANSPARENT_DIR = DOCS_DATA_DIR / "transparent"
DOCS_SAMPLE_DIR = DOCS_DIR / "sample"

# 7열 x 6행 그리드 좌표 (검은 테두리를 제외한 내부 슬레이트 영역)
X_RUNS = [
    (32, 135),
    (145, 248),
    (259, 362),
    (372, 475),
    (485, 588),
    (599, 702),
    (712, 815),
]
Y_RUNS = [
    (180, 270),
    (317, 410),
    (454, 546),
    (591, 679),
    (728, 815),
    (864, 951),
]

# 변환표의 6행 x 7열에 배치된 한글 자모 정의
GRID_CHARS = [
    # 1행: 기본 자음 (1)
    ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ"],
    # 2행: 기본 자음 (2)
    ["ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"],
    # 3행: 쌍자음 (오른쪽 위 반점 표기 / 6, 7열은 빈칸)
    ["ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ", None, None],
    # 4행: 모음 (1) - 변환표 하단 라벨은 상하 반전되어 있으나 실제 자모 순서는 아래와 같음
    ["ㅏ", "ㅐ", "ㅓ", "ㅔ", "ㅗ", "ㅚ", "ㅜ"],
    # 5행: 모음 (2)
    ["ㅟ", "ㅡ", "ㅣ", "ㅑ", "ㅒ", "ㅕ", "ㅖ"],
    # 6행: 모음 (3)
    ["ㅘ", "ㅙ", "ㅛ", "ㅝ", "ㅞ", "ㅠ", "ㅢ"],
]

# Halfwidth and Fullwidth Forms 블록(U+FF00~U+FFEF) 내 한글 자모 코드포인트 매핑
# 일반 한글 호환 자모(U+3131~U+3163)나 영문자(A-Z, a-z)를 침범하지 않고 에린어 폰트 전용으로 매핑할 유니코드 영역
JAMO_TO_FF_UNICODE = {
    "ㄱ": 0xFFA1, "ㄲ": 0xFFA2, "ㄴ": 0xFFA4, "ㄷ": 0xFFA7, "ㄸ": 0xFFA8,
    "ㄹ": 0xFFA9, "ㅁ": 0xFFB1, "ㅂ": 0xFFB2, "ㅃ": 0xFFB3, "ㅅ": 0xFFB5,
    "ㅆ": 0xFFB6, "ㅇ": 0xFFB7, "ㅈ": 0xFFB8, "ㅉ": 0xFFB9, "ㅊ": 0xFFBA,
    "ㅋ": 0xFFBB, "ㅌ": 0xFFBC, "ㅍ": 0xFFBD, "ㅎ": 0xFFBE,
    "ㅏ": 0xFFC2, "ㅐ": 0xFFC3, "ㅑ": 0xFFC4, "ㅒ": 0xFFC5, "ㅓ": 0xFFC6,
    "ㅔ": 0xFFC7, "ㅕ": 0xFFCA, "ㅖ": 0xFFCB, "ㅗ": 0xFFCC, "ㅘ": 0xFFCD,
    "ㅙ": 0xFFCE, "ㅚ": 0xFFCF, "ㅛ": 0xFFD2, "ㅜ": 0xFFD3, "ㅝ": 0xFFD4,
    "ㅞ": 0xFFD5, "ㅟ": 0xFFD6, "ㅠ": 0xFFD7, "ㅡ": 0xFFDA, "ㅢ": 0xFFDB,
    "ㅣ": 0xFFDC,
}

# 두벌식 키보드 기준 한글 자모 <-> 영문 쿼티 매핑 및 에린어 고유 맞춤법 규칙
CHAR_METADATA = {
    # 기본 자음 (14개)
    "ㄱ": {"qwerty": "r", "type": "consonant", "decompose": ["ㄱ"]},
    "ㄴ": {"qwerty": "s", "type": "consonant", "decompose": ["ㄴ"]},
    "ㄷ": {"qwerty": "e", "type": "consonant", "decompose": ["ㄷ"]},
    "ㄹ": {"qwerty": "f", "type": "consonant", "decompose": ["ㄹ"]},
    "ㅁ": {"qwerty": "a", "type": "consonant", "decompose": ["ㅁ"]},
    "ㅂ": {"qwerty": "q", "type": "consonant", "decompose": ["ㅂ"]},
    "ㅅ": {"qwerty": "t", "type": "consonant", "decompose": ["ㅅ"]},
    "ㅇ": {"qwerty": "d", "type": "consonant", "decompose": ["ㅇ"]},
    "ㅈ": {"qwerty": "w", "type": "consonant", "decompose": ["ㅈ"]},
    "ㅊ": {"qwerty": "c", "type": "consonant", "decompose": ["ㅊ"]},
    "ㅋ": {"qwerty": "z", "type": "consonant", "decompose": ["ㅋ"]},
    "ㅌ": {"qwerty": "x", "type": "consonant", "decompose": ["ㅌ"]},
    "ㅍ": {"qwerty": "v", "type": "consonant", "decompose": ["ㅍ"]},
    "ㅎ": {"qwerty": "g", "type": "consonant", "decompose": ["ㅎ"]},
    # 쌍자음 / 된소리 (5개) - 단자음 오른쪽 위 반점(tick) 또는 단자음 2개 연속 배치
    "ㄲ": {"qwerty": "R", "qwerty_pair": "rr", "type": "double_consonant", "base": "ㄱ", "tick": True, "decompose": ["ㄱ", "ㄱ"]},
    "ㄸ": {"qwerty": "E", "qwerty_pair": "ee", "type": "double_consonant", "base": "ㄷ", "tick": True, "decompose": ["ㄷ", "ㄷ"]},
    "ㅃ": {"qwerty": "Q", "qwerty_pair": "qq", "type": "double_consonant", "base": "ㅂ", "tick": True, "decompose": ["ㅂ", "ㅂ"]},
    "ㅆ": {"qwerty": "T", "qwerty_pair": "tt", "type": "double_consonant", "base": "ㅅ", "tick": True, "decompose": ["ㅅ", "ㅅ"]},
    "ㅉ": {"qwerty": "W", "qwerty_pair": "ww", "type": "double_consonant", "base": "ㅈ", "tick": True, "decompose": ["ㅈ", "ㅈ"]},
    # 기본 모음 및 대칭 관계
    "ㅏ": {"qwerty": "k", "type": "vowel", "symmetry": {"target": "ㅓ", "axis": "horizontal"}, "decompose": ["ㅏ"]},
    "ㅓ": {"qwerty": "j", "type": "vowel", "symmetry": {"target": "ㅏ", "axis": "horizontal"}, "decompose": ["ㅓ"]},
    "ㅗ": {"qwerty": "h", "type": "vowel", "symmetry": {"target": "ㅜ", "axis": "vertical"}, "decompose": ["ㅗ"]},
    "ㅜ": {"qwerty": "n", "type": "vowel", "symmetry": {"target": "ㅗ", "axis": "vertical"}, "decompose": ["ㅜ"]},
    "ㅡ": {"qwerty": "m", "type": "vowel", "decompose": ["ㅡ"]},
    "ㅣ": {"qwerty": "l", "type": "vowel", "decompose": ["ㅣ"]},
    "ㅑ": {"qwerty": "i", "type": "vowel", "symmetry": {"target": "ㅕ", "axis": "horizontal"}, "decompose": ["ㅑ"]},
    "ㅕ": {"qwerty": "u", "type": "vowel", "symmetry": {"target": "ㅑ", "axis": "horizontal"}, "decompose": ["ㅕ"]},
    "ㅛ": {"qwerty": "y", "type": "vowel", "symmetry": {"target": "ㅠ", "axis": "vertical"}, "decompose": ["ㅛ"]},
    "ㅠ": {"qwerty": "b", "type": "vowel", "symmetry": {"target": "ㅛ", "axis": "vertical"}, "decompose": ["ㅠ"]},
    # 복합 모음 (에린어 고유 맞춤법 반영)
    "ㅐ": {"qwerty": "o", "type": "compound_vowel", "orthography": "ㅏ + ㅣ", "decompose": ["ㅏ", "ㅣ"]},
    "ㅔ": {"qwerty": "p", "type": "compound_vowel", "orthography": "ㅣ + ㅏ (주의: ㅓ+ㅣ가 아님)", "decompose": ["ㅣ", "ㅏ"]},
    "ㅒ": {"qwerty": "O", "type": "compound_vowel", "base": "ㅐ", "tick": True, "orthography": "ㅐ(ㅏ+ㅣ) 오른쪽 위에 반점", "decompose": ["ㅒ"]},
    "ㅖ": {"qwerty": "P", "type": "compound_vowel", "base": "ㅔ", "tick": True, "orthography": "ㅔ(ㅣ+ㅏ) 오른쪽 위에 반점", "decompose": ["ㅖ"]},
    "ㅚ": {"qwerty": "hl", "type": "compound_vowel", "orthography": "ㅗ + ㅣ", "decompose": ["ㅗ", "ㅣ"]},
    "ㅟ": {"qwerty": "nl", "type": "compound_vowel", "orthography": "ㅜ + ㅣ", "decompose": ["ㅜ", "ㅣ"]},
    "ㅘ": {"qwerty": "hk", "type": "compound_vowel", "orthography": "ㅗ + ㅏ", "decompose": ["ㅗ", "ㅏ"]},
    "ㅙ": {"qwerty": "ho", "type": "compound_vowel", "orthography": "ㅗ + ㅐ(ㅏ+ㅣ)", "decompose": ["ㅗ", "ㅏ", "ㅣ"]},
    "ㅝ": {"qwerty": "nj", "type": "compound_vowel", "orthography": "ㅜ + ㅓ", "decompose": ["ㅜ", "ㅓ"]},
    "ㅞ": {"qwerty": "np", "type": "compound_vowel", "orthography": "ㅜ + ㅔ(ㅣ+ㅏ)", "decompose": ["ㅜ", "ㅣ", "ㅏ"]},
    "ㅢ": {"qwerty": "ml", "type": "compound_vowel", "orthography": "ㅡ + ㅣ", "decompose": ["ㅡ", "ㅣ"]},
}


def make_transparent_and_trim(tile_img: Image.Image, target_height: int = 86, pad_x: int = 3) -> Image.Image:
    """슬레이트 배경을 투명화하고 글자를 검은색(#000000)으로 변환한 뒤 좌우 여백을 글리프 폭에 맞게 다듬습니다."""
    resized = tile_img.resize((100, target_height), Image.Resampling.LANCZOS).convert("RGB")
    w, h = resized.size
    rgba = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    min_x, max_x = w, 0
    for y in range(h):
        for x in range(w):
            r, g, b = resized.getpixel((x, y))
            lum = (r + g + b) / 3.0
            if lum > 98:
                alpha = int(min(255, max(0, (lum - 98) / (242 - 98) * 255)))
                # 배경 투명, 글자 검은색(#000000)
                rgba.putpixel((x, y), (0, 0, 0, alpha))
                if alpha > 35:
                    if x < min_x:
                        min_x = x
                    if x > max_x:
                        max_x = x

    if min_x <= max_x:
        left = max(0, min_x - pad_x)
        right = min(w, max_x + 1 + pad_x)
        rgba = rgba.crop((left, 0, right, h))

    return rgba


def extract_all():
    if not IMPORT_IMAGE.exists():
        raise FileNotFoundError(f"변환표 이미지를 찾을 수 없습니다: {IMPORT_IMAGE}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TRANSPARENT_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_TRANSPARENT_DIR.mkdir(parents=True, exist_ok=True)

    # 기존에 crop만 했던 불투명 타일(data/*.png, docs/data/*.png)이 남아있다면 제거
    for old_png in DATA_DIR.glob("*.png"):
        old_png.unlink(missing_ok=True)
    for old_png in DOCS_DATA_DIR.glob("*.png"):
        old_png.unlink(missing_ok=True)

    img = Image.open(IMPORT_IMAGE).convert("RGB")
    mapping_output = {
        "source": "import/19d00ea17f157c624.webp",
        "description": "한국어/영어(두벌식) - 에린어 문자 매핑 및 고유 맞춤법 데이터 (투명 배경 + #000000 글리프)",
        "characters": {},
        "qwerty_to_jamo": {},
        "ff_unicode_to_jamo": {},
    }

    count = 0
    for r_idx, (y0, y1) in enumerate(Y_RUNS):
        for c_idx, (x0, x1) in enumerate(X_RUNS):
            jamo = GRID_CHARS[r_idx][c_idx]
            if jamo is None:
                continue

            crop_box = (x0 + 4, y0 + 4, x1 - 3, y1 - 3)
            raw_tile = img.crop(crop_box).resize((100, 86), Image.Resampling.LANCZOS)

            trans_img = make_transparent_and_trim(raw_tile, target_height=86, pad_x=3)
            trans_path = TRANSPARENT_DIR / f"{jamo}.png"
            trans_img.save(trans_path, format="PNG")
            trans_img.save(DOCS_TRANSPARENT_DIR / f"{jamo}.png", format="PNG")

            ff_cp = JAMO_TO_FF_UNICODE[jamo]
            ff_char = chr(ff_cp)

            meta = CHAR_METADATA[jamo].copy()
            meta.update({
                "jamo": jamo,
                "row": r_idx + 1,
                "col": c_idx + 1,
                "transparent_image": f"data/transparent/{jamo}.png",
                "width": trans_img.width,
                "height": trans_img.height,
                "font_codepoint": f"U+{ff_cp:04X}",
                "font_char": ff_char,
            })
            mapping_output["characters"][jamo] = meta

            qwerty_key = meta["qwerty"]
            if len(qwerty_key) == 1:
                mapping_output["qwerty_to_jamo"][qwerty_key] = jamo
            mapping_output["ff_unicode_to_jamo"][ff_char] = jamo

            count += 1

    mapping_file = DATA_DIR / "mapping.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping_output, f, ensure_ascii=False, indent=2)
    shutil.copy2(mapping_file, DOCS_DATA_DIR / "mapping.json")

    # 로컬 환경에서 sample 샘플 스크린샷이 존재하면 docs/sample/에 동기화 (둘 다 .gitignore에 의해 git 추적 제외)
    sample_img = BASE_DIR / "sample" / "MabinogiMobile_2026101714515366.png"
    if sample_img.exists():
        DOCS_SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sample_img, DOCS_SAMPLE_DIR / sample_img.name)

    print(f"총 {count}개의 투명 배경 + 검은색(#000000) 에린어 문자 이미지 추출 및 docs/ 동기화 완료")


if __name__ == "__main__":
    extract_all()
