"""
data/transparent/*.png에서 OCR 템플릿 매칭용 28x28 정규화 그리드 데이터를 생성하여
data/ 및 GitHub Pages 배포용 docs/data/ 폴더에 저장하는 스크립트입니다.

포함 템플릿:
- 기본 자음 14자 (ㄱ~ㅎ)
- 쌍자음 5자 (ㄲ, ㄸ, ㅃ, ㅆ, ㅉ : 단자음 오른쪽 위 반점 포함 단일 런)
- 기본 모음 10자 (ㅏ, ㅓ, ㅗ, ㅜ, ㅡ, ㅣ, ㅑ, ㅕ, ㅛ, ㅠ)
- ㅒ/ㅖ 우측 반점 결합 조각 2종:
  - "ㅣ'" : ㅒ(ㅏ + ㅣ')의 우측 파트 (ㅣ 오른쪽 위에 반점)
  - "ㅏ'" : ㅖ(ㅣ + ㅏ')의 우측 파트 (ㅏ 오른쪽 위에 반점)
"""

import json
import shutil
from pathlib import Path
import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
TRANS_DIR = BASE_DIR / "data" / "transparent"
OUT_JSON = BASE_DIR / "data" / "ocr_templates.json"
OUT_JS = BASE_DIR / "data" / "ocr_templates.js"

DOCS_DATA_DIR = BASE_DIR / "docs" / "data"

TEMPLATE_JAMOS = [
    "ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ",
    "ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ",
    "ㅏ", "ㅓ", "ㅗ", "ㅜ", "ㅡ", "ㅣ", "ㅑ", "ㅕ", "ㅛ", "ㅠ",
]

GRID_SIZE = 28


def resize_bilinear_28(crop: np.ndarray) -> np.ndarray:
    """브라우저 JS와 동일한 양선형 보간(Bilinear Interpolation)으로 28x28 그리드를 생성합니다."""
    h, w = crop.shape
    out = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float32)
    for gy in range(GRID_SIZE):
        sy = (gy + 0.5) * (h / float(GRID_SIZE)) - 0.5
        y0 = int(np.floor(sy))
        fy = sy - y0
        y1 = min(h - 1, max(0, y0 + 1))
        y0 = min(h - 1, max(0, y0))
        for gx in range(GRID_SIZE):
            sx = (gx + 0.5) * (w / float(GRID_SIZE)) - 0.5
            x0 = int(np.floor(sx))
            fx = sx - x0
            x1 = min(w - 1, max(0, x0 + 1))
            x0 = min(w - 1, max(0, x0))
            v00 = crop[y0, x0]
            v01 = crop[y0, x1]
            v10 = crop[y1, x0]
            v11 = crop[y1, x1]
            out[gy, gx] = (1.0 - fy) * ((1.0 - fx) * v00 + fx * v01) + fy * (
                (1.0 - fx) * v10 + fx * v11
            )
    return out


def extract_second_run_template(img_path: Path, key_name: str) -> dict:
    """ㅒ(ㅏ + ㅣ') 및 ㅖ(ㅣ + ㅏ')에서 오른쪽 반점이 찍힌 두 번째 컴포넌트만 추출합니다."""
    im = Image.open(img_path).convert("RGBA")
    mask = (np.array(im)[:, :, 3] > 80).astype(np.float32)
    col = np.sum(mask, axis=0)
    in_r = False
    runs = []
    xs = 0
    for x in range(len(col)):
        if col[x] > 0 and not in_r:
            in_r = True
            xs = x
        elif col[x] == 0 and in_r:
            in_r = False
            runs.append((xs, x - 1))
    if in_r:
        runs.append((xs, len(col) - 1))

    x0, x1 = runs[-1]
    sub = mask[:, x0 : x1 + 1]
    ys, xs_arr = np.where(sub > 0)
    crop = sub[ys.min() : ys.max() + 1, xs_arr.min() : xs_arr.max() + 1]
    h, w = crop.shape
    aspect = round(float(w) / float(h), 4)
    grid = resize_bilinear_28(crop)
    return {
        "jamo": key_name,
        "aspect": aspect,
        "w": int(w),
        "h": int(h),
        "grid": [round(float(v), 4) for v in grid.flatten()],
    }


def build_templates():
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = {
        "grid_size": GRID_SIZE,
        "templates": {},
    }

    for jamo in TEMPLATE_JAMOS:
        img_path = TRANS_DIR / f"{jamo}.png"
        im = Image.open(img_path).convert("RGBA")
        mask = (np.array(im)[:, :, 3] > 80).astype(np.float32)
        ys, xs = np.where(mask > 0)
        crop = mask[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
        h, w = crop.shape
        aspect = round(float(w) / float(h), 4)

        grid = resize_bilinear_28(crop)

        out["templates"][jamo] = {
            "jamo": jamo,
            "aspect": aspect,
            "w": int(w),
            "h": int(h),
            "grid": [round(float(v), 4) for v in grid.flatten()],
        }

    # ㅒ(ㅏ + ㅣ') 및 ㅖ(ㅣ + ㅏ')의 우측 반점 컴포넌트 추가
    out["templates"]["ㅣ'"] = extract_second_run_template(TRANS_DIR / "ㅒ.png", "ㅣ'")
    out["templates"]["ㅏ'"] = extract_second_run_template(TRANS_DIR / "ㅖ.png", "ㅏ'")

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    js_content = (
        "// 자동 생성 파일 (script/build_ocr_templates.py)\n"
        "window.ERIN_OCR_TEMPLATES = "
        + json.dumps(out, ensure_ascii=False)
        + ";\n"
    )
    with open(OUT_JS, "w", encoding="utf-8") as f:
        f.write(js_content)

    shutil.copy2(OUT_JSON, DOCS_DATA_DIR / OUT_JSON.name)
    shutil.copy2(OUT_JS, DOCS_DATA_DIR / OUT_JS.name)

    print(f"OCR 템플릿 {len(out['templates'])}개 생성 및 docs/data/ 동기화 완료")


if __name__ == "__main__":
    build_templates()
