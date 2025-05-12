import argparse
import subprocess
import time
from pathlib import Path

import Quartz
import pyautogui
import pywinctl
from PIL import Image
from tqdm import tqdm


def get_quartz_windows():
    return Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly,
        Quartz.kCGNullWindowID
    )


def find_matching_quartz_window_id(py_title, quartz_wins):
    py_title = py_title.strip().lower()
    for w in quartz_wins:
        name = w.get("kCGWindowName", "").strip().lower()
        if not name:
            continue
        if name == py_title or name in py_title or py_title in name:
            return w.get("kCGWindowNumber")
    return None


def crop_image(path: Path, trim_top: int, trim_bottom: int, trim_left: int, trim_right: int):
    with Image.open(path) as img:
        w, h = img.size
        left = trim_left
        top = trim_top
        right = w - trim_right
        bottom = h - trim_bottom

        if left >= right or top >= bottom:
            print(f"⚠️ 無効なトリミング範囲: {path.name}")
            return

        cropped = img.crop((left, top, right, bottom))
        cropped.save(path)


def capture(args):
    output = args.output.expanduser()
    output.mkdir(parents=True, exist_ok=True)

    if args.trim_all:
        try:
            top, bottom, left, right = [int(x.strip()) for x in args.trim_all.split(",")]
        except Exception:
            print("❌ --trim-all の形式は '上,下,左,右' で指定してください（例: 60,40,10,10）")
            exit(1)
    else:
        top, bottom, left, right = args.trim_top, args.trim_bottom, args.trim_left, args.trim_right

    py_windows = [w for w in pywinctl.getAllWindows() if w.title.strip()]
    if not py_windows:
        print("❌ ウィンドウが見つかりませんでした。")
        exit(1)

    print("📚 キャプチャ対象のウィンドウを選んでください：\n")
    for i, win in enumerate(py_windows):
        print(f"[{i}] {win.title}")

    index = int(input("番号を入力: "))
    selected = py_windows[index]
    title = selected.title.strip()

    print(f"\n🎯 選択されたウィンドウ: {title}")
    quartz_wins = get_quartz_windows()
    win_id = find_matching_quartz_window_id(title, quartz_wins)

    if not win_id:
        print("❌ 対応するQuartzウィンドウIDが見つかりませんでした。")
        exit(1)

    print(f"\n📸 {args.pages} ページ撮影を開始します...\n")
    selected.activate()
    time.sleep(1)

    for i in tqdm(range(1, args.pages + 1), desc="📸 キャプチャ中", unit="page"):
        fname = output / f"{i:04}.png"
        subprocess.run(["screencapture", "-x", "-o", "-l", str(win_id), str(fname)])
        crop_image(fname, top, bottom, left, right)

        if i < args.pages:
            pyautogui.press(args.key)
            time.sleep(args.interval)

    if args.pdf:
        images = [Image.open(output / f"{i:04}.png").convert("RGB") for i in range(1, args.pages + 1)]
        pdf_path = output / "output.pdf"
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        print(f"\n✅ PDFを保存しました → {pdf_path}")


def pdf_only(input_dir: Path):
    pngs = sorted(input_dir.glob("*.png"))
    if not pngs:
        print("❌ PNGファイルが見つかりません。")
        exit(1)

    images = [Image.open(p).convert("RGB") for p in pngs]
    pdf_path = input_dir / "output.pdf"
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f"✅ PDFのみを保存しました → {pdf_path}")


def main():
    parser = argparse.ArgumentParser(description="電子書籍キャプチャツール")
    subparsers = parser.add_subparsers(dest="command")

    cap = subparsers.add_parser("capture", help="画像キャプチャとPDF作成")
    cap.add_argument("--pages", "-p", type=int, default=1)
    cap.add_argument("--interval", type=float, default=1.2)
    cap.add_argument("--key", type=str, default="right")
    cap.add_argument("--output", "-o", type=Path, default=Path.home() / "Desktop" / "ebook-capture")
    cap.add_argument("--pdf", dest="pdf", action="store_true")
    cap.add_argument("--no-pdf", dest="pdf", action="store_false")
    cap.set_defaults(pdf=True)
    cap.add_argument("--trim", dest="trim_all", type=str, default=None, help="トリミング一括指定（例: 60,40,10,10）")
    cap.add_argument("--trim-top", type=int, default=55)
    cap.add_argument("--trim-bottom", type=int, default=0)
    cap.add_argument("--trim-left", type=int, default=0)
    cap.add_argument("--trim-right", type=int, default=0)
    cap.set_defaults(func=capture)

    pdfp = subparsers.add_parser("pdf-only", help="既存PNGからPDFのみを生成")
    pdfp.add_argument("--input", "-i", type=Path, default=Path.home() / "Desktop" / "ebook-capture")
    pdfp.set_defaults(func=lambda args: pdf_only(args.input))

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
