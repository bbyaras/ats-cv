# ATS Uyumlu CV Hazırlama

ATS (Applicant Tracking System) başvuru sistemleri CV'nizi önce bir yazılımla okur. Bu repo, CV'nizin bu yazılımlar tarafından doğru okunmasını sağlamak için şablon, rehber ve basit bir kontrol aracı içerir.

## İçerik

| Yol | Açıklama |
|---|---|
| [`docs/ats-rehberi.md`](docs/ats-rehberi.md) | ATS kuralları, yapılması/yapılmaması gerekenler |
| [`docs/kontrol-listesi.md`](docs/kontrol-listesi.md) | Göndermeden önce işaretlenecek liste |
| [`templates/cv-tr.md`](templates/cv-tr.md) | Türkçe CV şablonu (Markdown) |
| [`templates/cv-en.md`](templates/cv-en.md) | İngilizce CV şablonu (Markdown) |
| [`templates/cv.html`](templates/cv.html) | Tek sütunlu, yazdırmaya hazır HTML şablonu (PDF'e çevrilir) |
| [`tools/ats_check.py`](tools/ats_check.py) | CV'yi ilan metniyle karşılaştıran kontrol scripti |
| [`examples/ilan.txt`](examples/ilan.txt) | Örnek iş ilanı |

## Claude Code ile otomatik uyarlama

Repo klasöründe Claude Code'u aç ve `/cv-uyarla` yaz. Akış:

1. Mevcut CV'ni yüklemeni ister (`inputs/` klasörüne koyabilirsin).
2. Başvuracağın ilanın linkini ister.
3. CV'ni ilana göre ATS uyumlu hale getirip `output/` klasörüne yazar; ne değiştiğini ve eksik kalanları raporlar.

Olmayan deneyim veya beceri eklenmez. `inputs/` ve `output/` git'e girmez.

## Hızlı başlangıç

1. `templates/cv-tr.md` dosyasını kopyalayıp kendi bilgilerinle doldur.
2. İlan metnini bir `.txt` dosyasına yapıştır.
3. Kontrol et:

```powershell
python tools/ats_check.py templates/cv-tr.md examples/ilan.txt
```

Çıktı: yapısal uyarılar, ilandaki anahtar kelimelerin CV'de geçme oranı ve eksik kelimeler.

4. PDF üretmek için `templates/cv.html` dosyasını doldurup tarayıcıdan **Yazdır → PDF olarak kaydet** yap (metin seçilebilir kalır).

## Temel ilkeler

- Tek sütun, tablo/grafik/ikon yok.
- Standart başlıklar: Özet, Deneyim, Eğitim, Yetenekler.
- İlandaki anahtar kelimeleri (dürüstçe) kullan.
- Sade yazı tipi (Arial, Calibri), `.docx` veya metin tabanlı PDF.

Script yalnızca bir yaklaşık göstergedir; gerçek ATS'ler farklı çalışabilir.

## Lisans

MIT
