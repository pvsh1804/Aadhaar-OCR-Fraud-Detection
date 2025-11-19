import argparse
import json
import pathlib
import cv2

from .image_ops import normalize_image
from .exif_utils import extract_exif
from .qr_detector import QRDetector   # <-- YOLO QR Detection

VALID_EXT = [".jpg", ".jpeg", ".png", ".pdf", ".tif", ".tiff"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_dir", required=True)
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--manifest_out", required=True)
    args = parser.parse_args()

    in_dir = pathlib.Path(args.in_dir)
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = pathlib.Path(args.manifest_out)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    # Load YOLO QR detector
    qr_detector = QRDetector(model_path="runs/detect/train9/weights/best.pt")

    rows = []

    # Process each image
    for src in sorted(in_dir.rglob("*")):
        if src.suffix.lower() not in VALID_EXT:
            continue

        dst = out_dir / (src.stem + ".png")

        try:
            # 1. Normalize (deskew + denoise)
            info = normalize_image(src, dst, dpi=300)

            # 2. Extract EXIF
            exif = extract_exif(src)

            # 3. YOLO QR detection
            crop, bbox = qr_detector.detect_and_crop(str(dst))

            if crop is not None:
                qr_text = qr_detector.decode_qr(crop)

                # Save QR crop for debugging
                qr_crop_path = out_dir / f"{src.stem}_qr.png"
                cv2.imwrite(str(qr_crop_path), crop)

                qr_data = {
                    "payload": qr_text,
                    "bbox": bbox,
                    "ok": True if qr_text else False
                }
            else:
                qr_data = None

            # Add entry to manifest
            rows.append({
                "id": src.stem,
                "src": str(src),
                "norm_path": str(dst),
                "width": info["w"],
                "height": info["h"],
                "deskew_deg": info["deskew_deg"],
                "denoise_strength": info["denoise_strength"],
                "exif": exif,
                "qr_payload_raw": qr_data["payload"] if qr_data else None,
                "qr_bbox": [int(x) for x in qr_data["bbox"]] if qr_data else None,
                "qr_checksum_ok": qr_data["ok"] if qr_data else None
            })

            print(f"[OK] {src.name} → {dst.name}  | angle={info['deskew_deg']:.2f}°  QR={'Y' if qr_data else 'N'}")

        except Exception as e:
            print(f"[ERR] {src.name}: {e}")

    # Write manifest file
    with open(manifest_path, "w", encoding="utf-8") as f:
        for entry in rows:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n✨ Manifest written: {manifest_path}  ({len(rows)} items)")


if __name__ == "__main__":
    main()
