# Double Image Viewer

同じ解像度の JPEG または PNG 画像を2枚受け取り、1枚目を表示します。

## セットアップ

```bash
pip install -r requirements.txt
```

## 使い方

```bash
python3 doubleimageview.py a.jpeg b.jpeg
```

2枚目の画像は解像度の一致確認に使われます。解像度が異なる場合はエラーで終了します。
