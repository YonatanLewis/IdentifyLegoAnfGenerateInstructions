import requests
from typing import Dict, Any, List, Optional
from .config import REBRICKABLE_API_KEY, REBRICKABLE_BASE

HEADERS = {"Authorization": f"key {REBRICKABLE_API_KEY}"} if REBRICKABLE_API_KEY else {}

def _get(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def paged_get(url: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    out = []
    page = 1
    params = params.copy() if params else {}
    while True:
        params.update({"page": page})
        data = _get(url, params=params)
        results = data.get("results", [])
        out.extend(results)
        if not data.get("next"):
            break
        page += 1
    return out

def get_part_colors(part_num: str) -> List[Dict[str, Any]]:
    url = f"{REBRICKABLE_BASE}/parts/{part_num}/colors/"
    return paged_get(url)

def get_color_info(color_id: int) -> Dict[str, Any]:
    url = f"{REBRICKABLE_BASE}/colors/{color_id}/"
    return _get(url)

def build_part_image_url(part_num: str, color_id: int) -> str:
    return f"https://cdn.rebrickable.com/media/parts/{color_id}/{part_num}.png"
