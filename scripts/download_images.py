#!/usr/bin/env python3
#import argparse
#from pathlib import Path
#from src.dataset_builder import download_part_color_images, write_dataset_index
#from src.config import DATASETS_DIR 

#def main(parts_file: str):
#    parts = [p.strip() for p in Path(parts_file).read_text().splitlines() if p.strip()]
#    items = download_part_color_images(parts)
#    idx_csv = write_dataset_index(items)
#    print(f"Dataset index written to {idx_csv} and index.xlsx with {len(items)} rows.")

#if __name__ == "__main__":
#    ap = argparse.ArgumentParser()
#    ap.add_argument("--parts", required=True, help="Path to common_parts.txt") 
#    args = ap.parse_args()
#    main(args.parts)
# --- bootstrap so "from src..." works even when run as a .py script ---
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# ----------------------------------------------------------------------

import argparse
from pathlib import Path
from src.dataset_builder import download_part_color_images, write_dataset_index
from src.config import DATASETS_DIR

def main(parts_file: str):
    parts = [p.strip() for p in Path(parts_file).read_text().splitlines() if p.strip()]
    # Download images for each part/color via the Rebrickable API
    items = download_part_color_images(parts)
    # Build dataset index (CSV) from downloaded files
    idx_csv = write_dataset_index()
    print(f"Dataset index written to {idx_csv} with {len(items)} rows.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--parts", required=True, help="Path to data/datasets/common_parts.txt")
    args = ap.parse_args()
    main(args.parts)
