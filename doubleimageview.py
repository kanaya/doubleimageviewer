#!/usr/bin/env python3
"""同じ解像度の画像2枚を受け取り、1枚目を表示する。"""

import argparse
import sys
from pathlib import Path

import cv2

SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="同じ解像度の画像2枚を受け取り、1枚目を表示します。"
    )
    parser.add_argument("image1", type=Path, help="表示する画像（JPEG または PNG）")
    parser.add_argument("image2", type=Path, help="比較用の2枚目の画像（JPEG または PNG）")
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


def load_image(path: Path):
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


def main() -> None:
    args = parse_args()
    validate_path(args.image1)
    validate_path(args.image2)

    image1 = load_image(args.image1)
    image2 = load_image(args.image2)
    check_same_resolution(image1, image2, args.image1, args.image2)

    window_name = args.image1.name
    cv2.imshow(window_name, image1)
    print("画像を表示しています。何かキーを押すと終了します。")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
