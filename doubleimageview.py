#!/usr/bin/env python3
"""同じ解像度の画像2枚を受け取り、1枚目を表示する。クリックで周辺を2枚目で置換。"""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png"}
# クリック位置を中心とする置換領域の半径（ピクセル）
PATCH_RADIUS = 50


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="同じ解像度の画像2枚を受け取り、1枚目を表示します。"
        "クリックした周辺を2枚目の画像で置き換えます。"
    )
    parser.add_argument("image1", type=Path, help="表示する画像（JPEG または PNG）")
    parser.add_argument("image2", type=Path, help="置換に使う2枚目の画像（JPEG または PNG）")
    return parser.parse_args()


def validate_path(path: Path) -> None:
    if not path.is_file():
        print(f"エラー: ファイルが見つかりません: {path}", file=sys.stderr)
        sys.exit(1)
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        print(
            f"エラー: 対応していない形式です（JPEG/PNG のみ）: {path}",
            file=sys.stderr,
        )
        sys.exit(1)


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        print(f"エラー: 画像を読み込めませんでした: {path}", file=sys.stderr)
        sys.exit(1)
    return image


def check_same_resolution(image1, image2, path1: Path, path2: Path) -> None:
    if image1.shape != image2.shape:
        h1, w1 = image1.shape[:2]
        h2, w2 = image2.shape[:2]
        print(
            "エラー: 2枚の画像の解像度が一致しません。\n"
            f"  {path1}: {w1} x {h1}\n"
            f"  {path2}: {w2} x {h2}",
            file=sys.stderr,
        )
        sys.exit(1)


def patch_bounds(
    width: int, height: int, cx: int, cy: int, radius: int
) -> tuple[int, int, int, int]:
    """クリック中心の矩形領域 (x1, y1, x2, y2)。x2/y2 はスライス終端（排他的）。"""
    x1 = max(0, cx - radius)
    y1 = max(0, cy - radius)
    x2 = min(width, cx + radius + 1)
    y2 = min(height, cy + radius + 1)
    return x1, y1, x2, y2


def circular_mask(
    x1: int, y1: int, x2: int, y2: int, cx: int, cy: int, radius: int
) -> np.ndarray:
    """バウンディングボックス内の円形マスク（bool, shape: (y2-y1, x2-x1)）。"""
    ys = np.arange(y1, y2)[:, None]
    xs = np.arange(x1, x2)[None, :]
    return (xs - cx) ** 2 + (ys - cy) ** 2 <= radius**2


def apply_patch(
    display: np.ndarray, source: np.ndarray, cx: int, cy: int, radius: int
) -> None:
    h, w = display.shape[:2]
    x1, y1, x2, y2 = patch_bounds(w, h, cx, cy, radius)
    mask = circular_mask(x1, y1, x2, y2, cx, cy, radius)
    region = display[y1:y2, x1:x2]
    region[mask] = source[y1:y2, x1:x2][mask]


def on_mouse(event: int, x: int, y: int, _flags: int, state: dict) -> None:
    if event != cv2.EVENT_LBUTTONDOWN:
        return
    apply_patch(state["display"], state["source"], x, y, state["radius"])
    cv2.imshow(state["window_name"], state["display"])


def main() -> None:
    args = parse_args()
    validate_path(args.image1)
    validate_path(args.image2)

    image1 = load_image(args.image1)
    image2 = load_image(args.image2)
    check_same_resolution(image1, image2, args.image1, args.image2)

    window_name = args.image1.name
    display = image1.copy()
    state = {
        "display": display,
        "source": image2,
        "radius": PATCH_RADIUS,
        "window_name": window_name,
    }

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, on_mouse, state)
    cv2.imshow(window_name, display)
    print(
        "画像を表示しています。"
        f"クリックで周辺の円（半径 {PATCH_RADIUS}px）を2枚目の画像で置き換えます。"
        "何かキーを押すと終了します。"
    )
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
