---
name: cv-uyarla
description: Kullanıcının mevcut CV'sini alıp başvurmak istediği iş ilanına göre ATS uyumlu hale getirir. "CV'mi ilana göre düzenle", "ATS uyumlu CV hazırla", "ilana uyarla" dendiğinde kullan.
---

# CV'yi ilana göre uyarla

Adımları sırayla izle. Bir adımın girdisi gelmeden sonrakine geçme.

## 1. Mevcut CV'yi iste
Kullanıcıdan mevcut CV'sini yüklemesini (dosya yolu: PDF, DOCX, MD, TXT) ya da metnini yapıştırmasını iste. Sadece bunu sor ve cevabı bekle.
- Dosyayı `inputs/` klasörüne koymasını öner (git'e girmez).
- PDF/DOCX ise metni çıkar ve doğru okunup okunmadığını (sütun, tablo bozulması) kullanıcıya kısaca bildir.

## 2. İlan linkini iste
CV geldikten sonra başvurmak istediği ilanın linkini iste ve bekle.
- Sayfayı WebFetch veya tarayıcı aracıyla oku.
- Giriş duvarı varsa (LinkedIn vb.) veya okunamazsa kullanıcıdan ilan metnini yapıştırmasını iste; atlama.
- İlan metnini `inputs/ilan.txt` olarak kaydet.

## 3. Analiz
- İlandan zorunlu ve tercih edilen gereksinimleri, araçları, anahtar kelimeleri çıkar.
- CV ile eşleştir: karşılanan, zayıf anlatılan, eksik olanlar.
- Gerekirse `python tools/ats_check.py inputs/cv.md inputs/ilan.txt` çalıştır.

## 4. CV'yi uyarla
`docs/ats-rehberi.md` kurallarına uy: tek sütun, standart başlıklar, tutarlı tarih, eylemle başlayan ve ölçülebilir maddeler, en fazla 2 sayfa.
- İlana en uygun deneyimleri öne çıkar, özet bölümünü ilana göre yeniden yaz.
- İlandaki terimleri, kullanıcı gerçekten yaptıysa, ilandaki yazımıyla kullan.
- **Asla uydurma:** olmayan deneyim, beceri, unvan, tarih, rakam ekleme. Eksik gereksinimler için kullanıcıya "Bu konuda deneyimin var mı?" diye sor; sadece evet derse ekle.
- Sayısal sonuç yoksa uydurma; kullanıcıdan iste.
- Şablon: `templates/cv-tr.md` veya `cv-en.md` (ilan diline göre).

## 5. Doğrula ve teslim et
- Sonucu `output/cv-<sirket>.md` olarak yaz; `ats_check.py` ile tekrar çalıştır, eşleşme düşükse (ve kullanıcı sahipse) iyileştir.
- Kullanıcıya şunu sun: ne değiştirdin, eşleşme oranı öncesi/sonrası, hâlâ eksik olan gereksinimler.
- İstenirse `templates/cv.html` ile PDF'e çevrilecek HTML üret.

## Gizlilik
CV ve ilan kişisel veridir: `inputs/` ve `output/` `.gitignore`'dadır; commit etme, GitHub'a gönderme.
