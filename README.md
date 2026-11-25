# ATS Uyumlu CV Hazırlama

ATS (Applicant Tracking System) başvuru sistemleri CV'nizi önce bir yazılımla okur. Bu repo, CV'nizin bu yazılımlar tarafından doğru okunmasını sağlamak için şablon, rehber ve basit bir kontrol aracı içerir. Şablonlar ve rehber, İK uzmanları tarafından kontrol edilmektedir.

## İçerik

| Yol | Açıklama |
|---|---|
| [`docs/ats-rehberi.md`](docs/ats-rehberi.md) | ATS kuralları, yapılması/yapılmaması gerekenler |
| [`docs/kontrol-listesi.md`](docs/kontrol-listesi.md) | Göndermeden önce işaretlenecek liste |
| [`templates/cv-tr.md`](templates/cv-tr.md) | Türkçe CV şablonu, yazılım örneği (Markdown) |
| [`templates/cv-satis-tr.md`](templates/cv-satis-tr.md) | Türkçe CV şablonu, satış/saha örneği |
| [`templates/cv-en.md`](templates/cv-en.md) | İngilizce CV şablonu (Markdown) |
| [`templates/cv.html`](templates/cv.html) | Tek sütunlu, yazdırmaya hazır HTML şablonu (PDF'e çevrilir) |
| [`tools/ats_check.py`](tools/ats_check.py) | CV'yi ilan metniyle karşılaştıran kontrol scripti |
| [`tools/build_pdf.py`](tools/build_pdf.py) | Markdown CV'yi ATS uyumlu PDF'e çevirir (Edge/Chrome ile) |
| [`examples/ilan.txt`](examples/ilan.txt) | Örnek iş ilanı |

## Claude Code ile otomatik uyarlama

Repo klasöründe Claude Code'u aç ve `/cv-uyarla` yaz. Akış:

1. Mevcut CV'ni yüklemeni ister (`inputs/` klasörüne koyabilirsin).
2. Başvuracağın ilanın linkini ister. İlanın yoksa hedef pozisyon, sektör, kıdem, öne çıkarmak istediklerin gibi sorular sorar.
   Birden fazla ilan verirsen her biri için ayrı CV hazırlanır ve her başvuruda öne çıkarmak istediğin özellikleri sorar.
   CV ile ilan arasındaki **uyumluluk oranını** (zorunlu gereksinim %50, tercih edilen %20, anahtar kelime %30; ağırlıklar sezgiseldir, sonuç bir tahmindir) önce/sonra olarak hesaplar. LinkedIn ilanlarında "Yetenekler" eşleşmesine de bakar.
   Çıktı formatını sorar (PDF, DOCX, Markdown); **başvuruda PDF'i önerir (ilan başka format istiyorsa onu)** ve PDF'i Edge/Chrome ile üretir.
   En sonda CV'nin profesyonel bir İK uzmanı gözüyle incelenmesini isteyip istemediğini sorar; istersen puan, güçlü yönler ve öncelikli düzeltmeleri verir.
   İstersen CV'ndeki özelliklere göre güncel iş ilanları da bulur; seçtiğin ilanlar için ayrı CV hazırlar. Başvuruyu senin adına göndermez.
3. CV'ni ilana (veya cevaplarına) göre ATS uyumlu hale getirip `output/` klasörüne yazar; ne değiştiğini ve eksik kalanları raporlar.

CV'nde olmayan bir şeyi eklemek istersen önce onayını alır; deneyim maddeleri için sayısal sonuçlar (yüzde, süre, hacim, ekip büyüklüğü) sorarak CV'yi somutlaştırır. Onaysız veya uydurma bilgi eklenmez. `inputs/` ve `output/` git'e girmez.

## Hızlı başlangıç

1. `templates/cv-tr.md` dosyasını kopyalayıp kendi bilgilerinle doldur.
2. İlan metnini bir `.txt` dosyasına yapıştır.
3. Kontrol et:

```powershell
python tools/ats_check.py templates/cv-tr.md examples/ilan.txt
```

CV `.md`, `.txt`, `.docx` veya `.pdf` olabilir (PDF için `pip install pypdf` veya `pdftotext` gerekir); teslim edeceğin son dosyayı da kontrol et. Türkçe ekler (yönetim/yönetimi) ve büyük harfli kelimeler (SATIŞ) eşleşir.

Çıktı: yapısal uyarılar, ilan anahtar kelime eşleşmesi (%), eksik kelimeler ve **ATS sonucu (GEÇER / RİSKLİ / GEÇEMEZ)**. İlan vermezsen yalnızca yapı kontrol edilir. Sonuç GEÇER değilse çıkış kodu 1 olur. Bu bir ön tahmindir, geçiş garantisi vermez.

4. PDF üretmek için `templates/cv.html` dosyasını doldurup tarayıcıdan **Yazdır → PDF olarak kaydet** yap (metin seçilebilir kalır).

## Temel ilkeler

- Tek sütun, tablo/grafik/ikon yok.
- Standart başlıklar: Özet, Deneyim, Eğitim, Yetenekler.
- İlandaki anahtar kelimeleri (dürüstçe) kullan.
- Sade yazı tipi (Arial, Calibri), `.docx` veya metin tabanlı PDF.

Script yalnızca bir yaklaşık göstergedir; gerçek ATS'ler farklı çalışabilir.

## Lisans

MIT
