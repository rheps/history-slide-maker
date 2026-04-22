"""교과서 PDF에서 텍스트와 이미지를 추출하는 스크립트.

사용법:
    python extract_pdf.py <pdf_path> <output_dir> [--pages 3-5]

출력:
    output_dir/
    ├── text.txt          # 전체 텍스트 (페이지별 구분)
    └── images/
        ├── p3_img0.jpeg  # 페이지번호_이미지순번.확장자
        ├── p3_img1.png
        └── ...
"""

import argparse
import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF가 필요합니다. 설치: pip install pymupdf")
    sys.exit(1)


def parse_page_range(page_str, max_pages):
    """'3-10' 또는 '3' 형태의 페이지 범위를 파싱."""
    if not page_str:
        return range(max_pages)
    if '-' in page_str:
        start, end = page_str.split('-')
        return range(int(start) - 1, min(int(end), max_pages))
    else:
        p = int(page_str) - 1
        return range(p, p + 1)


def extract(pdf_path, output_dir, page_range_str=None):
    doc = fitz.open(pdf_path)
    pages = parse_page_range(page_range_str, len(doc))

    # 디렉토리 생성
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # 텍스트 추출
    full_text = ""
    for i in pages:
        page = doc[i]
        text = page.get_text()
        full_text += f"\n\n=== 교과서 {i+1}페이지 ===\n{text}"

    text_path = os.path.join(output_dir, "text.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    # 이미지 추출
    image_count = 0
    image_manifest = []
    for i in pages:
        page = doc[i]
        images = page.get_images(full=True)
        for img_idx, img in enumerate(images):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
            except Exception:
                continue
            ext = base_image["ext"]
            width = base_image["width"]
            height = base_image["height"]
            data = base_image["image"]

            # 너무 작은 이미지 스킵 (아이콘/장식)
            if width < 50 or height < 50:
                continue

            # CMYK 이미지를 RGB로 변환 (브라우저 호환)
            colorspace = base_image.get("colorspace", 0)
            if colorspace == 4:  # CMYK
                try:
                    from PIL import Image
                    import io
                    img_pil = Image.open(io.BytesIO(data))
                    if img_pil.mode == "CMYK":
                        img_pil = img_pil.convert("RGB")
                        buf = io.BytesIO()
                        img_pil.save(buf, format="JPEG", quality=95)
                        data = buf.getvalue()
                        ext = "jpeg"
                except ImportError:
                    pass  # PIL 없으면 원본 그대로

            fname = f"p{i+1}_img{img_idx}.{ext}"
            fpath = os.path.join(images_dir, fname)
            with open(fpath, "wb") as f:
                f.write(data)

            image_manifest.append({
                "file": fname,
                "page": i + 1,
                "index": img_idx,
                "width": width,
                "height": height,
                "size_kb": len(data) // 1024,
            })
            image_count += 1

    # 매니페스트 저장
    import json
    manifest_path = os.path.join(output_dir, "image_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(image_manifest, f, ensure_ascii=False, indent=2)

    print(f"텍스트: {text_path} ({len(full_text)} chars)")
    print(f"이미지: {image_count}개 → {images_dir}")
    print(f"매니페스트: {manifest_path}")
    return text_path, images_dir, manifest_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="교과서 PDF에서 텍스트/이미지 추출")
    parser.add_argument("pdf_path", help="PDF 파일 경로")
    parser.add_argument("output_dir", help="출력 디렉토리")
    parser.add_argument("--pages", help="페이지 범위 (예: 3-10)", default=None)
    args = parser.parse_args()
    extract(args.pdf_path, args.output_dir, args.pages)
