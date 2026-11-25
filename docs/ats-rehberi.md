# ATS Rehberi

## ATS nasıl çalışır?

1. CV'yi yükleyince metin çıkarılır (parse).
2. Metin başlıklara göre bölümlere ayrılır: iletişim, deneyim, eğitim, yetenekler.
3. İlandaki kelimelerle eşleştirilip işe alımcıya sıralı liste sunulur.

Parse bozulursa (tablo, sütun, görsel) bilgiler yanlış alana düşer veya kaybolur.

## Yapılması gerekenler

- **Tek sütun** ve yukarıdan aşağı akış.
- **Standart başlıklar:** Özet, İş Deneyimi, Eğitim, Yetenekler, Sertifikalar, Projeler, Diller.
- **Tarih formatı tutarlı:** `03/2022 – 08/2024` veya `Mart 2022 – Ağustos 2024`.
- **Her deneyim:** Pozisyon, Şirket, Şehir, Tarih, 3–6 madde.
- **Maddeler eylemle başlasın ve sayı içersin:** "Sipariş işleme süresini %30 azalttım".
- **İlandaki terimleri aynen kullan** (ör. "Proje Yönetimi", "SQL", "Agile"). Kısaltmanın yanında açılımını da yaz: "Arama Motoru Optimizasyonu (SEO)".
- **Dosya:** İlan hangi formatı istiyorsa onu gönder. Belirtilmemişse metin tabanlı PDF (veya `.docx`). Dosya adı: `Ad_Soyad_CV.pdf`.
- **Yazı tipi:** Arial, Calibri, Times New Roman; 10–12 pt. Başlıklar 12–14 pt.
- **Uzunluk:** 1 sayfa (0–8 yıl), en fazla 2 sayfa.
- **İletişim bilgisi sayfanın gövdesinde** olsun: e-posta, telefon, şehir, LinkedIn.

## Kaçınılması gerekenler

- Tablo, çok sütun, metin kutusu.
- Header/footer içine iletişim bilgisi koymak (bazı ATS'ler üst/alt bilgiyi okumaz, sistemden sisteme değişir).
- Fotoğraf, ikon, grafik, ilerleme çubuğu ("Python ●●●●○").
- Resim olarak taranmış PDF.
- Süslü madde işaretleri; sade `-` veya `•` kullan.
- Yaratıcı başlıklar ("Yolculuğum", "Neler Yapabilirim").
- Anahtar kelime doldurma (beyaz yazı, gizli metin) — elenir.
- Doğum tarihi, medeni hal, TC kimlik no (başvuru ülkesine göre gereksiz veya riskli).

## Anahtar kelime stratejisi

1. İlanı oku, tekrar eden teknik terimleri, araçları ve sorumlulukları işaretle.
2. Gerçekten sahip olduklarını CV'ye ilanın kullandığı biçimde yaz.
3. Hem **Yetenekler** bölümünde hem **Deneyim** maddelerinde kullan (bağlam gösterir).
4. Her ilan için CV'yi küçük ölçüde uyarla; `tools/ats_check.py` ile eksikleri gör.

Sahip olmadığın beceriyi yazma; mülakatta ortaya çıkar.

## Türkçe CV notları

- Türkçe karakterler (ç, ğ, ı, ö, ş, ü) UTF-8 PDF/DOCX'te sorun çıkarmaz; dosya adında yine de kullanma.
- İngilizce ilana İngilizce CV gönder. Türkçe ve İngilizce terimi birlikte geçirmek eşleşmeyi artırır: "Veri Analizi (Data Analysis)".

## Türkiye'ye özgü notlar

- **Fotoğraf:** ATS'ye yüklenecek CV'de fotoğraf kullanma (okunmaz, düzeni bozabilir). Doğrudan İK'ya e-postayla gönderdiğin CV'de fotoğraf Türkiye'de hâlâ yaygındır; istersen iki sürüm tut: ATS için fotoğrafsız, e-posta için fotoğraflı. Yurt dışı başvurularında fotoğraf koyma.
- **Askerlik, sürücü belgesi, seyahat engeli:** Özellikle saha/satış ilanlarında sık sorulur. İlan istiyorsa kısa bir "Ek Bilgiler" bölümüne yaz (ör. `Askerlik: Yapıldı | Sürücü belgesi: B | Seyahat engeli: Yok`). İlan sormuyorsa ekleme.
- **Başvuru formundaki ön eleme soruları:** "Çalışma izniniz var mı", "en az X yıl deneyim", "maaş beklentisi" gibi sorular birçok sistemde ilk elemeyi yapar (sistemden sisteme değişir). Dürüst ve dikkatli yanıtla.
- **Workday, SuccessFactors gibi sistemler:** CV yüklemek bazı alanları otomatik doldurur; yüklemeden sonra açılan formda unvan, şirket ve tarihleri kontrol edip düzelt.
- **Kariyer.net:** İK'lar şehir, sektör, askerlik gibi filtrelerle arama yapabilir; profildeki bu alanları doldur.
