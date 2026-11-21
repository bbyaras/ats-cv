#!/usr/bin/env python3
"""CV'yi ATS açısından kontrol eder ve ilan anahtar kelimeleriyle karşılaştırır.

Kullanım: python tools/ats_check.py cv.md ilan.txt [--top 25]
Bağımlılık yok (yalnızca standart kütüphane). CV: .md veya .txt.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

SECTIONS = {
    "Deneyim": ["deneyim", "experience", "work history"],
    "Eğitim": ["eğitim", "egitim", "education"],
    "Yetenekler": ["yetenek", "beceri", "skills"],
}

STOPWORDS = set("""
ve veya ile için bir bu şu o da de ki mi olan olarak daha çok en gibi ya
veya artı değerdir olmak olmuş sahip tercihen aranan aradığımız nitelikler
bilgisi deneyimi deneyim hakimiyet yatkın güçlü benzeri
the and or for with a an to of in on is are be as at by we you our your will
have has experience knowledge ability work working years year plus strong
""".split())


def lower_tr(text: str) -> str:
    # "I"→"ı" yapılmaz: İngilizce terimler (API, FastAPI) bozulur
    return text.replace("İ", "i").lower()


def tokens(text: str) -> list[str]:
    # c++, c#, ci/cd gibi terimleri koru
    return re.findall(r"[a-zçğıöşü0-9][a-zçğıöşü0-9+#./-]*[a-zçğıöşü0-9+#]|[a-zçğıöşü]", lower_tr(text))


def structure_warnings(raw: str) -> list[str]:
    low = lower_tr(raw)
    out = []
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", raw):
        out.append("E-posta adresi bulunamadı.")
    if not re.search(r"\+?\d[\d\s()-]{8,}\d", raw):
        out.append("Telefon numarası bulunamadı.")
    for name, keys in SECTIONS.items():
        if not any(re.search(rf"^#+\s*.*{k}|^{k}", low, re.M) for k in keys):
            out.append(f"Standart '{name}' başlığı bulunamadı.")
    if re.search(r"^\s*\|.*\|\s*$", raw, re.M) and re.search(r"^\s*\|?\s*:?-{3,}", raw, re.M):
        out.append("Tablo var; ATS tabloları yanlış okuyabilir.")
    if "![" in raw or "<img" in low:
        out.append("Görsel var; ATS görselleri okuyamaz.")
    if re.search(r"[●○◐★☆■□◆▪►]", raw):
        out.append("Süslü simgeler/puan işaretleri var; sade '-' kullan.")
    words = len(raw.split())
    if words > 900:
        out.append(f"Çok uzun ({words} kelime); 2 sayfayı aşabilir.")
    elif words < 150:
        out.append(f"Çok kısa ({words} kelime).")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cv")
    ap.add_argument("ilan")
    ap.add_argument("--top", type=int, default=25, help="İlandan alınacak anahtar kelime sayısı")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # Windows konsolunda Türkçe karakterler için

    cv = Path(a.cv).read_text(encoding="utf-8")
    ilan = Path(a.ilan).read_text(encoding="utf-8")

    print("== Yapı kontrolü ==")
    warns = structure_warnings(cv)
    print("\n".join(f"- {w}" for w in warns) if warns else "- Sorun bulunamadı.")

    counts = Counter(t for t in tokens(ilan) if t not in STOPWORDS and len(t) > 2)
    keywords = [k for k, _ in counts.most_common(a.top)]
    cv_text = " ".join(tokens(cv))
    found = [k for k in keywords if re.search(rf"(?<![\w+#]){re.escape(k)}", cv_text)]
    missing = [k for k in keywords if k not in found]

    pct = round(100 * len(found) / len(keywords)) if keywords else 0
    print(f"\n== Anahtar kelime eşleşmesi: %{pct} ({len(found)}/{len(keywords)}) ==")
    print("Bulunan :", ", ".join(found) or "-")
    print("Eksik   :", ", ".join(missing) or "-")
    print("\nNot: Eksik kelimeleri yalnızca gerçekten sahipsen ekle.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
