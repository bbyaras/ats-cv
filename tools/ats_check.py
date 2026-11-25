#!/usr/bin/env python3
"""CV'yi ATS açısından kontrol eder ve ilan anahtar kelimeleriyle karşılaştırır.

Kullanım: python tools/ats_check.py cv.(md|txt|pdf|docx) [ilan.txt] [--top 25]
Temel kullanım için bağımlılık yok. PDF için `pypdf` (pip install pypdf) veya
`pdftotext` (poppler) gerekir; DOCX yalnızca standart kütüphaneyle okunur.
Sonuç bir ön tahmindir; gerçek ATS'ler farklı çalışır.
"""
import argparse
import html
import re
import shutil
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path

SECTIONS = {
    "Deneyim": ["deneyim", "tecrübe", "experience", "employment", "work history", "iş geçmişi"],
    "Eğitim": ["eğitim", "egitim", "education", "öğrenim"],
    "Yetenekler": ["yetenek", "beceri", "yetkinlik", "uzmanlık", "skills", "competenc", "expertise"],
}

_STOP_TR = """
ve veya ile için bir bu şu o da de ki mi olan olarak daha çok en gibi ya her tüm
ayrıca ise ancak fakat hem gerek kadar sonra önce üzerine hakkında yeni
artı değerdir olmak olmuş sahip sahipseniz tercihen aranan aradığımız arıyoruz aranıyor
aranmaktadır arayan nitelikler nitelik bilgisi deneyimi deneyim hakimiyet yatkın güçlü
benzeri neler bekliyor birlikte almak katılmak istiyoruz ekibimize ekibimizde takımımıza
başvuru başvurun başvurabilirsiniz ilan pozisyon pozisyonu şirket şirketimiz tercih
avantaj avantajdır edilir olacak yapabilen yapabilecek konusunda alanında ilgili konularda
sorumluluklar sorumlulukları görevler sizi büyümek istediğimiz özellikler özellik beceri becerisi
"""
_STOP_EN = """
the and or for with a an to of in on is are be as at by we you our your will
have has experience knowledge ability work working years year plus strong
looking join team role position candidate candidates must should responsibilities
requirements qualifications about us what offer benefits
"""


def lower_tr(text: str) -> str:
    # "I"→"ı" yapılmaz: İngilizce terimler (API, FastAPI) bozulur.
    # Büyük harfli Türkçe ("SATIŞ") için karşılaştırmada ı→i katlanır (bkz. fold).
    return text.replace("İ", "i").lower()


def fold(text: str) -> str:
    """ı ile i'yi eşitler: 'SATIŞ'→'satış', 'satış' ile aynı anahtara iner."""
    return text.replace("ı", "i")


def stem(t: str) -> str:
    """Basit kök bulma: uzun kelimeleri ilk 5 harfe indirir (Türkçe ekler için).
    'yönetimi/yönetim', 'hedefleri/hedef' eşleşir. Sembollü terimler (c++, ci/cd) aynen kalır."""
    return t[:5] if len(t) > 5 and t.isalpha() else t


STOPWORDS = {fold(w) for w in (_STOP_TR + _STOP_EN).split()}
STOP_STEMS = {w[:5] for w in STOPWORDS if len(w) > 5}


def is_stop(t: str) -> bool:
    return t in STOPWORDS or stem(t) in STOP_STEMS


_TOKEN = re.compile(r"[a-zçğıöşü0-9][a-zçğıöşü0-9+#./-]*[a-zçğıöşü0-9+#]|[a-zçğıöşü]")
KEEP_SLASH = {"ci/cd", "tcp/ip", "pl/sql", "a/b", "i/o"}  # bölünmeyen terimler
SHORT_OK = {"ai", "ml", "ux", "ui", "bi", "hr", "it", "qa", "ar", "vr", "pm"}  # 2 harfli terimler (yalnız BÜYÜK yazıldığında)


def tokens_surface(text: str) -> list[tuple[str, str, bool]]:
    """(karşılaştırma_anahtarı, gösterim, büyük_harf_mi) üçlüleri.
    c++, c#, ci/cd gibi terimler korunur; "Satış/Pazarlama" gibi eğik çizgili ifadeler bölünür.
    Gösterim, metindeki orijinal yazılıştır (büyük harfli kelimelerde katlanmış hâl)."""
    folded = fold(lower_tr(text))
    out = []
    for m in _TOKEN.finditer(folded):
        raw = text[m.start():m.end()]
        if "/" in m.group() and m.group() not in KEEP_SLASH:
            pairs = zip(m.group().split("/"), raw.split("/"))
        else:
            pairs = [(m.group(), raw)]
        for key, r in pairs:
            if key:
                up = r.isupper()
                out.append((key, key if up else lower_tr(r), up))
    return out


def tokens(text: str) -> list[str]:
    return [k for k, _, _ in tokens_surface(text)]


# ---------- Dosya okuma ----------

def read_pdf(p: Path) -> tuple[str, int | None]:
    try:
        from pypdf import PdfReader
        r = PdfReader(str(p))
        return "\n".join((pg.extract_text() or "") for pg in r.pages), len(r.pages)
    except ImportError:
        pass
    exe = shutil.which("pdftotext")
    if exe:
        out = subprocess.run([exe, str(p), "-"], capture_output=True, check=True).stdout.decode("utf-8", "replace")
        return out, out.count("\f") or None
    sys.exit("PDF okumak için `pip install pypdf` veya poppler'ın `pdftotext` aracı gerekir.")


def read_docx(p: Path) -> tuple[str, list[tuple[bool, str]]]:
    with zipfile.ZipFile(p) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    extra = []
    if "<w:tbl>" in xml or "<w:tbl " in xml:
        extra.append((True, "Word dosyasında tablo var; ATS tabloları yanlış okuyabilir."))
    if "<w:drawing" in xml or "<w:pict" in xml:
        extra.append((True, "Word dosyasında görsel/şekil var; ATS bunları okuyamaz."))
    text = re.sub(r"</w:p>", "\n", xml)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return text, extra


def load(path: str) -> tuple[str, int | None, list[tuple[bool, str]]]:
    """(metin, sayfa sayısı veya None, dosyaya özgü uyarılar)"""
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".pdf":
        text, pages = read_pdf(p)
        return text, pages, []
    if ext == ".docx":
        text, extra = read_docx(p)
        return text, None, extra
    return p.read_text(encoding="utf-8-sig"), None, []


# ---------- Kontroller ----------

def has_section(low: str, keys: list[str]) -> bool:
    """Kısa (<=5 kelime) bir satırda başlık anahtar kelimesi geçiyorsa başlık sayılır."""
    keys = [fold(k) for k in keys]
    for line in low.splitlines():
        text = re.sub(r"^[\s#*_>]+|[\s*_:]+$", "", line)
        if text and not text.startswith(("-", "•")) and len(text.split()) <= 5 \
                and any(k in text for k in keys):
            return True
    return False


def structure_warnings(raw: str, pages: int | None = None) -> list[tuple[bool, str]]:
    """(kritik_mi, mesaj) listesi döndürür."""
    low = fold(lower_tr(raw))
    out = []
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", raw):
        out.append((True, "E-posta adresi bulunamadı."))
    if not re.search(r"\+?\d[\d\s()-]{8,}\d", raw):
        out.append((False, "Telefon numarası bulunamadı."))
    for name, keys in SECTIONS.items():
        if not has_section(low, keys):
            out.append((True, f"Standart '{name}' başlığı bulunamadı."))
    if re.search(r"^\s*\|.*\|\s*$", raw, re.M) and re.search(r"^\s*\|?\s*:?-{3,}", raw, re.M):
        out.append((True, "Tablo var; ATS tabloları yanlış okuyabilir."))
    if "![" in raw or "<img" in low:
        out.append((True, "Görsel var; ATS görselleri okuyamaz."))
    if re.search(r"[●○◐★☆■□◆▪►]", raw):
        out.append((False, "Süslü simgeler/puan işaretleri var; sade '-' kullan."))
    words = len(raw.split())
    if pages is not None:
        if pages > 2:
            out.append((False, f"{pages} sayfa; en fazla 2 sayfa önerilir."))
    elif words > 900:
        out.append((False, f"Çok uzun ({words} kelime); 2 sayfayı aşabilir (sayfa sayısı bilinmiyor)."))
    if words < 150:
        out.append((False, f"Çok kısa ({words} kelime)."))
    return out


MIN_ESLESME = 50  # % — sezgisel eşik; altı "riskli"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cv")
    ap.add_argument("ilan", nargs="?", help="İlan metni (isteğe bağlı; verilmezse yalnızca yapı kontrol edilir)")
    ap.add_argument("--top", type=int, default=25, help="İlandan alınacak anahtar kelime sayısı")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # Windows konsolunda Türkçe karakterler için

    cv, pages, extra = load(a.cv)

    print("== Yapı kontrolü ==")
    warns = extra + structure_warnings(cv, pages)
    critical = [m for c, m in warns if c]
    minor = [m for c, m in warns if not c]
    for m in critical:
        print(f"- [KRİTİK] {m}")
    for m in minor:
        print(f"- [uyarı] {m}")
    if not warns:
        print("- Sorun bulunamadı.")
    if pages is not None:
        print(f"- Sayfa sayısı: {pages}")

    pct = None
    if a.ilan:
        ilan = load(a.ilan)[0]
        surface: dict[str, str] = {}  # kök → ilandaki ilk yazılış (gösterim için)
        counts: Counter = Counter()
        for t, shown, upper in tokens_surface(ilan):
            if (len(t) > 2 or (upper and t in SHORT_OK)) and not is_stop(t):
                k = stem(t)
                # Gösterimde "ı" içeren (doğru Türkçe) yazılışı tercih et
                if k not in surface or ("ı" in shown and "ı" not in surface[k]):
                    surface[k] = shown
                counts[k] += 1
        keywords = [k for k, _ in counts.most_common(a.top)]
        if not keywords:
            print("\n== İlan anahtar kelime eşleşmesi ==\nİlan dosyası boş veya anlamlı kelime içermiyor; eşleşme hesaplanamadı.")
        else:
            cv_stems = {stem(t) for t in tokens(cv)}
            found = [surface[k] for k in keywords if k in cv_stems]
            missing = [surface[k] for k in keywords if k not in cv_stems]
            pct = round(100 * len(found) / len(keywords))
            print(f"\n== İlan anahtar kelime eşleşmesi: %{pct} ({len(found)}/{len(keywords)}) ==")
            print("Bulunan :", ", ".join(found) or "-")
            print("Eksik   :", ", ".join(missing) or "-")
            print("\nNot: Eksik kelimeleri yalnızca gerçekten sahipsen ekle.")

    if critical:
        verdict, code = "GEÇEMEZ", 1
        reason = "Kritik yapı sorunları ATS'nin CV'yi yanlış okumasına neden olur."
    elif pct is not None and pct < MIN_ESLESME:
        verdict, code = "RİSKLİ", 1
        reason = f"Anahtar kelime eşleşmesi %{MIN_ESLESME} altında; ilan gereksinimleri CV'de yeterince görünmüyor."
    elif minor:
        verdict, code = "GEÇER (küçük düzeltmelerle)", 0
        reason = "Kritik sorun yok; uyarıları gidermen önerilir."
    else:
        verdict, code = "GEÇER", 0
        reason = "Yapı ve anahtar kelime kontrolleri temiz."
    print(f"\n== ATS sonucu: {verdict} ==\n{reason}")
    print("Bu bir ön tahmindir; gerçek ATS'ler farklı çalışabilir ve geçiş garantisi vermez.")
    return code


if __name__ == "__main__":
    sys.exit(main())
