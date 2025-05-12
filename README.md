# 📚 ebookcap – 電子書籍キャプチャツール

macOS 上で動作する、電子書籍ビューアのウィンドウを自動でキャプチャし、ページごとに画像として保存、そして PDF に変換するツールです。
表紙から巻末まで、任意のページ数を連続でキャプチャして、読みやすい PDF として書き出すことができます。

---

## 🛠 インストール

このツールは Python 3.9 以上が必要です。仮想環境を作成し、以下のようにセットアップします：

```bash
python -m venv .venv
source .venv/bin/activate  # または .venv\\Scripts\\activate（Windows）
pip install -r requirements.txt
```

`requirements.txt` に含まれる主なライブラリ：

* `pyautogui`
* `pywinctl`
* `pyobjc`
* `pillow`
* `tqdm`

---

## 📦 使い方

### コマンド構文

```bash
python main.py capture [オプション]
```

### 主なオプション

| オプション            | 説明                                     |
| ---------------- | -------------------------------------- |
| `--pages`, `-p`  | 撮影するページ数（例：`--pages 20`）               |
| `--interval`     | ページ送りの待ち時間（秒）                          |
| `--key`          | ページ送りに使うキー（例：`right`, `left`, `space`） |
| `--output`, `-o` | 保存先フォルダ（デフォルト：デスクトップ）                  |
| `--trim`         | トリミング一括指定（例：`--trim 60,40,10,10`）      |
| `--trim-top` 等   | 上下左右を個別に指定（`--trim` と併用不可）             |
| `--no-pdf`       | PDF作成を無効化（PNGのみ保存）                     |

---

### 🔑 キーの一覧を確認するには：

```bash
python -c "import pyautogui; print(pyautogui.KEYBOARD_KEYS)"
```

PyAutoGUI がサポートしているすべてのキー一覧が表示されます。
使用できるキー名には `"right"`, `"left"`, `"space"`, `"enter"` などがあります。

---

### 📄 PDFのみを再作成したい場合

すでに PNG があるフォルダから、PDFだけ作り直すには：

```bash
python main.py pdf-only --input ./電子書籍キャプチャ
```

---

## 🧷 使い方の例

```bash
python main.py capture -p 10 --trim 60,40,10,10
```

→ 10ページ分キャプチャ、指定したトリミングで切り抜き、PDFも出力されます。

---

## ⚠️ 免責事項・注意事項

* **本ツールは、個人利用・研究・バックアップを目的とした利用を前提としています。**
* **著作権で保護されたコンテンツを複製・再配布する行為には、各自の責任のもと十分に注意してください。**
* **このツールを使用して生じたいかなる損害やトラブルについても、作成者は一切の責任を負いません。**
* **現在は macOS のみ対応しています。Windows や Linux では動作しません。**

---

## 💬 ライセンス

このツールは MIT ライセンスの下で配布されています。詳しくはリポジトリ内の LICENSE ファイルをご覧ください。
