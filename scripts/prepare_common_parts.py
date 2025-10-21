#!/usr/bin/env python3
#import argparse, shutil
#from pathlib import Path
#import pandas as pd
#from src.dataset_builder import select_common_parts_from_csv, write_common_parts_outputs
#from src.config import RAW_DIR, DATASETS_DIR, TOP_N_PARTS

#def main(csv_path: str, top_n: int = TOP_N_PARTS):
    #csvp = Path(csv_path)
    #RAW_DIR.mkdir(parents=True, exist_ok=True)
    #shutil.copy2(csvp, RAW_DIR/csvp.name)
    #parts = select_common_parts_from_csv(csvp, top_n=top_n)
    #write_common_parts_outputs(parts)
    #print(f"Wrote {len(parts)} common parts to {DATASETS_DIR} (txt + xlsx)")

#if __name__ == "__main__":
#    ap = argparse.ArgumentParser()
   # ap.add_argument("--csv", required=True, help="Path to inventory_parts.csv from Rebrickable dumps") 
#    ap.add_argument("--top", type=int, default=TOP_N_PARTS, help="How many parts to keep (100-200 recommended)")
#    args = ap.parse_args()
#    main(args.csv, top_n=args.top)
# --- bootstrap so "from src..." works even when run as a .py script ---
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# ----------------------------------------------------------------------

import argparse
from src.dataset_builder import (
    select_common_parts_from_csv,
    write_common_parts_outputs,
)
from src.config import DATASETS_DIR

def main(csv_path: str, top: int):
    parts = select_common_parts_from_csv(pathlib.Path(csv_path), top_n=top)
    write_common_parts_outputs(parts, DATASETS_DIR)
    print(f"Wrote {len(parts)} common parts to {DATASETS_DIR} (txt + csv).")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path to data/raw/inventory_parts.csv")
    ap.add_argument("--top", type=int, default=150, help="How many most-common parts")
    args = ap.parse_args()
    main(args.csv, args.top)
