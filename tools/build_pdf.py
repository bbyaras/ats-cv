#!/usr/bin/env python3
"""CV markdown dosyasını ATS uyumlu tek sütunlu HTML'e ve PDF'e çevirir.

Kullanım: python tools/build_pdf.py output/cv-sirket.md [--out output/Ad_Soyad_CV.pdf]
Aynı .md dosyasından üretildiği için ats_check.py ile kontrol edilen metin ile PDF aynı olur.
PDF için Edge veya Chrome gerekir (yoksa yalnızca HTML üretilir, tarayıcıdan Yazdır → PDF yap).
Desteklenen markdown: # başlık, ## bölüm, - madde, **kalın**, boş satırla paragraf.
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CSS = """
@page { size: A4; margin: 15mm; }
body { font-family: Arial, Calibri, sans-serif; font-size: 11pt; line-height: 1.35; color: #000; max-width: 180mm; margin: 0 auto; }
h1 { font-size: 20pt; margin: 0 0 4pt; }
h2 { font-size: 12.5pt; text-transform: uppercase; border-bottom: 1px solid #000; margin: 14pt 0 6pt; padding-bottom: 2pt; break-after: avoid; }
p, ul { margin: 0 0 6pt; }
ul { padding-left: 16pt; }
li, p { break-inside: avoid; }
"""


def inline(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(text))


def md_to_html(md: str, title: str) -> str:
    out, para, items = [], [], []

    def flush():
        nonlocal para, items
        if para:
            out.append("<p>" + "<br>\n".join(inline(l) for l in para) + "</p>")
            para = []
        if items:
            out.append("<ul>\n" + "\n".join(f"  <li>{inline(i)}</li>" for i in items) + "\n</ul>")
            items = []

    for line in md.splitlines():
        s = line.strip()
        if not s:
            flush()
        elif s.startswith("## "):
            flush()
            out.append(f"<h2>{inline(s[3:])}</h2>")
        elif s.startswith("# "):
            flush()
            out.append(f"<h1>{inline(s[2:])}</h1>")
        elif s.startswith(("- ", "• ")):
            if para:
                flush()
            items.append(s[2:])
        else:
            if items:
                flush()
            para.append(s)
    flush()
    body = "\n".join(out)
    return (f'<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n<title>{html.escape(title)}</title>\n'
            f"<style>{CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n")


def find_browser() -> str | None:
    for name in ("msedge", "microsoft-edge", "google-chrome", "chrome", "chromium"):
        if shutil.which(name):
            return shutil.which(name)
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    return next((c for c in candidates if os.path.exists(c)), None)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md")
    ap.add_argument("--out", help="PDF yolu (varsayılan: .md ile aynı ad, .pdf)")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    src = Path(a.md).resolve()
    pdf = Path(a.out).resolve() if a.out else src.with_suffix(".pdf")
    page = src.with_suffix(".html")
    page.write_text(md_to_html(src.read_text(encoding="utf-8-sig"), pdf.stem), encoding="utf-8")
    print(f"HTML: {page}")

    browser = find_browser()
    if not browser:
        print("Edge/Chrome bulunamadı. HTML'i tarayıcıda açıp Yazdır → PDF olarak kaydet.")
        return 1
    with tempfile.TemporaryDirectory() as profile:  # çalışan tarayıcıyla çakışmasın
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--user-data-dir={profile}", f"--print-to-pdf={pdf}", page.as_uri()],
                       capture_output=True, timeout=90)
    if pdf.exists() and pdf.stat().st_size > 0:
        print(f"PDF : {pdf} ({pdf.stat().st_size // 1024} KB)")
        print("Sonraki adım: python tools/ats_check.py", pdf, "[ilan.txt]")
        return 0
    print("PDF oluşturulamadı; HTML'i tarayıcıdan yazdırmayı dene.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
