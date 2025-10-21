import csv, time
from pathlib import Path
from typing import List, Tuple
import requests, pandas as pd
from .config import IMAGES_DIR, DATASETS_DIR, TOP_N_PARTS, MIN_COLORS_PER_PART
from .rebrickable_client import get_part_colors, build_part_image_url

def select_common_parts_from_csv(csv_path: Path, top_n: int = TOP_N_PARTS) -> List[str]:
    counts = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            part = row.get('part_num')
            qty = int(row.get('quantity', '1') or 1)
            if part:
                counts[part] = counts.get(part, 0) + qty
    top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [p for p,_ in top]

def ensure_download(url: str, out_path: Path, retries: int = 3, sleep: float = 0.5) -> bool:
    if out_path.exists(): 
        return True
    for i in range(retries):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200 and r.content:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                with open(out_path, 'wb') as f:
                    f.write(r.content)
                return True
        except Exception:
            pass
        time.sleep(sleep * (i+1))
    return False

def download_part_color_images(parts: List[str]) -> List[Tuple[str, int, Path]]:
    items = []
    for part in parts:
        try:
            colors = get_part_colors(part)
        except Exception as e:
            print(f"[warn] failed colors for {part}: {e}")
            continue
        color_items = []
        for c in colors:
            color_id = c.get('color_id')
            url = c.get('part_img_url') or build_part_image_url(part, color_id)
            if not color_id or not url:
                continue
            out = IMAGES_DIR / part / str(color_id) / f"{part}_{color_id}.png"
            ok = ensure_download(url, out)
            if ok:
                color_items.append((part, int(color_id), out))
        if len(color_items) >= MIN_COLORS_PER_PART:
            items.extend(color_items)
    return items

def write_common_parts_outputs(parts: List[str]) -> None:
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    (DATASETS_DIR/"common_parts.txt").write_text("\n".join(parts))
    pd.DataFrame({"part_num": parts}).to_excel(DATASETS_DIR/"common_parts.xlsx", index=False)

def write_dataset_index(items: List[Tuple[str,int,Path]]) -> Path:
    out_csv = DATASETS_DIR / "index.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["image_path","part_num","color_id"]) 
        for part, color, path in items:
            writer.writerow([str(path), part, color])
            rows.append({"image_path": str(path), "part_num": part, "color_id": color})
    # Excel mirror
    pd.DataFrame(rows or [{"image_path":"","part_num":"","color_id":""}]).to_excel(DATASETS_DIR/"index.xlsx", index=False)
    return out_csv
