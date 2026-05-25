# Double Image Viewer

同じ解像度の JPEG または PNG 画像を2枚受け取り、1枚目を表示します。表示中にマウスをクリックすると、その周辺（半径 50 ピクセル）が2枚目の画像の同じ位置で置き換わります。

## セットアップ

```bash
pip install -r requirements.txt
```

## 使い方

```bash
python3 doubleimageview.py a.jpeg b.jpeg
```

2枚目はクリックした位置の置換元として使われます。解像度が異なる場合はエラーで終了します。
