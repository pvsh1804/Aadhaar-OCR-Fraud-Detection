from PIL import Image, ExifTags

def extract_exif(path):
    try:
        img = Image.open(path)
        info = img._getexif() or {}
        inv = {ExifTags.TAGS.get(k, k): v for k, v in info.items()}
        keep = {
            "DateTimeOriginal": inv.get("DateTimeOriginal"),
            "Make": inv.get("Make"),
            "Model": inv.get("Model"),
            "GPSInfo": inv.get("GPSInfo"),
        }
        return {k:v for k,v in keep.items() if v is not None}
    except Exception:
        return {}
