---
name: cv-uyarla
description: Kullanıcının mevcut CV'sini alıp başvurmak istediği iş ilanına (ilan yoksa sorulara verdiği cevaplara) göre ATS uyumlu hale getirir. "CV'mi ilana göre düzenle", "ATS uyumlu CV hazırla", "ilana uyarla" dendiğinde kullan.
---

# CV'yi ilana göre uyarla

Adımları sırayla izle. Bir adımın girdisi gelmeden sonrakine geçme.

## 1. Mevcut CV'yi iste
Kullanıcıdan mevcut CV'sini yüklemesini (dosya yolu: PDF, DOCX, MD, TXT) ya da metnini yapıştırmasını iste. Sadece bunu sor ve cevabı bekle.
- Dosyayı `inputs/` klasörüne koymasını öner (git'e girmez).
- **Gizlilik uyarısı (kısa, bir kez söyle):** CV içeriği bu oturumda yapay zekâ sağlayıcısının sunucularına gönderilir; `inputs/` yalnızca git'e girmez. Yüklemeden önce TC kimlik no, tam ev adresi, referans kişilerin telefonları gibi gereksiz kişisel bilgileri çıkarmasını öner.
- PDF/DOCX ise metni çıkar ve doğru okunup okunmadığını (sütun, tablo bozulması) kullanıcıya kısaca bildir.

## 2. İlan linkini iste
CV geldikten sonra başvurmak istediği ilanın linkini (birden fazlaysa hepsini) iste ve bekle.
- Sayfayı WebFetch veya tarayıcı aracıyla oku.
- Giriş duvarı varsa (LinkedIn vb.) veya okunamazsa kullanıcıdan ilan metnini yapıştırmasını iste; atlama.
- Her ilanı ayrı dosyaya kaydet: tek ilan `inputs/ilan.txt`, birden çok ilan `inputs/ilan-<sirket>.txt`.

### Birden çok ilan varsa
Her ilan için **ayrı bir CV** hazırla; tek CV'yi hepsine uydurmaya çalışma. İlanları tek tek ele al (5. adım dahil), çıktılar birbirinin üzerine yazılmasın.

### Öne çıkarılacak özellikleri sor
Her ilan (veya hedef) için, analizden önce `AskUserQuestion` ile sor:
- Bu başvuruda en çok öne çıkarmak istediğin 2–3 özellik, başarı veya proje hangisi? (CV'deki ve ilandaki gereksinimlerden 3–4 somut seçenek sun.)
- Bu ilan için geri planda bırakmak veya çıkarmak istediğin bir şey var mı?
Cevapları o ilanın CV'sinde özet, ilk maddeler ve yetenek sırasını belirlemekte kullan. Seçilenler CV'de gerçekten varsa öne çıkar; yoksa uydurma, kullanıcıya sor.

### İlan yoksa: hedef belirleme soruları
Kullanıcının ilanı yoksa ilan istemeyi bırak ve hedefi sorularla çıkar. `AskUserQuestion` ile en fazla 4 soruluk gruplar hâlinde, kısa sor; CV'de zaten cevabı olan şeyi sorma:
1. Hedef pozisyon/unvan nedir (birden fazlaysa öncelik sırası)?
2. Hedef sektör veya şirket türü (startup, kurumsal, kamu, freelance)?
3. Kıdem seviyesi ve çalışma şekli (junior/mid/senior/yönetici; uzaktan/hibrit/ofis)?
4. Başvuru dili (Türkçe/İngilizce) ve ülke/şehir?
5. En çok öne çıkarmak istediği 3 başarı, proje veya beceri?
6. Kariyer değişikliği var mı? Varsa hangi deneyimlerin aktarılabilir olduğunu düşünüyor?
7. Hangi araç/teknolojilerde gerçekten rahat, hangilerinde yüzeysel?
8. CV'de çıkarılmasını veya vurgulanmamasını istediği bir şey var mı?
Cevaplardan hedef profilini çıkar (pozisyon, anahtar kelimeler, vurgulanacak deneyimler) ve `inputs/ilan.txt` yerine `inputs/hedef.md` olarak kaydet. Anahtar kelimeleri hedef pozisyonun yaygın gereksinimlerinden türet ve kullanıcıya onaylat. Sonra 4. adımda bu profile göre CV'yi düzenle; `ats_check.py` için `hedef.md`'yi ilan yerine ver.

## 3. Analiz
- İlandan (veya hedef profilinden) zorunlu ve tercih edilen gereksinimleri, araçları, anahtar kelimeleri çıkar.
- CV ile eşleştir: karşılanan, zayıf anlatılan, eksik olanlar.
- **Gerçek bir ilan yoksa (hedef profili modu) uyumluluk oranı BASMA.** Anahtar kelimeleri kendin türetip CV'yi onlara göre puanlamak gerçek bir ilana uyumu göstermez. Bu modda sadece yapı kontrolü (`ats_check.py` ilansız), CV güçlendirme (somut veri, anahtar kelime önerileri) ve 6. adımdaki İK incelemesi yapılır; gerçek bir ilan bulunduğunda oranı o zaman hesapla.
- **Uyumluluk oranını hesapla** (yalnızca gerçek ilan varsa) ve uyarlamadan ÖNCE kullanıcıya göster:
  1. Anahtar kelime oranı: `python tools/ats_check.py inputs/cv.md inputs/ilan.txt` çıktısındaki %.
  2. Gereksinim oranı: ilandaki zorunlu gereksinimlerin kaçı CV'de karşılanıyor (tam = 1, zayıf/kısmi = 0,5, yok = 0) ve tercih edilenlerin kaçı karşılanıyor.
  3. **Genel uyumluluk = %50 zorunlu gereksinim + %20 tercih edilen + %30 anahtar kelime.** Tercih edilen gereksinim yoksa ağırlığı zorunluya ekle (%70 / %30).
  Hesabın dökümünü tablo olarak göster (gereksinim, durum, puan), tahmini bir değer olduğunu belirt. Her ilan için ayrı hesapla; CV'yi güncelledikten sonra 5. adımda tekrar hesapla (önce/sonra).
- **ATS geçiş kontrolü:** `ats_check.py` sonunda GEÇER / RİSKLİ / GEÇEMEZ sonucu verir (kritik yapı sorunu varsa GEÇEMEZ, ilan eşleşmesi %50 altındaysa RİSKLİ). Bu sonucu uyarlamadan önce ve sonra kullanıcıya göster; GEÇEMEZ veya RİSKLİ ise teslimden önce düzelt. Garanti değil, ön tahmindir; öyle söyle.
- `ats_check.py` .md, .txt, .docx ve .pdf okur (PDF için `pypdf` veya `pdftotext` gerekir; yoksa `pip install pypdf` öner). Teslim edilecek **son PDF/DOCX dosyasını** da kontrol et: metin doğru çıkıyor mu, sayfa sayısı 2'yi geçiyor mu.
- Eşleşme sayısı "ilan anahtar kelime eşleşmesi"dir; gerçek ATS'ler adaya oran göstermez. Sonucu "tahmin" olarak sun, "geçer/geçemez"i garanti gibi söyleme. Eksik kelimeler için her zaman "gerçekten sahipsen ekle" de.

### LinkedIn Yetenekler eşleşmesi (ilan LinkedIn'deyse)
- İlan sayfasındaki "Yetenekler" (Skills) eşleşme listesini oku. Sayfa giriş istiyorsa kullanıcı **kendisi** giriş yapsın ya da listenin ekran görüntüsünü versin; bu adımı atlama, "başvurmaya hazır" demeden önce yap.
- Her yetenek için tablo: yetenek · CV'de var mı · profilde var mı · kanıt (hangi deneyim).
- Kullanıcı onaylarsa, gerçekten sahip olduklarını ilandaki yazımıyla CV'ye ekle (Yetenekler bölümü + ilgili deneyim maddesi) ve "LinkedIn profilindeki Yetenekler'e de ekle" listesini ver. Çoğu zaman yetenek vardır, yalnız farklı kelimeyle yazılmıştır.
- Olmayanları asla ekleme; "açık" olarak raporla ve 6. adımdaki İK incelemesinde mülakat riski olarak işaretle (mülakatta bu sorulursa ne denileceğini hazırla).

## 4. CV'yi uyarla
`docs/ats-rehberi.md` kurallarına uy: tek sütun, standart başlıklar, tutarlı tarih, eylemle başlayan ve ölçülebilir maddeler, en fazla 2 sayfa.
- İlana en uygun deneyimleri öne çıkar, özet bölümünü ilana göre yeniden yaz.
- İlandaki terimleri, kullanıcı gerçekten yaptıysa, ilandaki yazımıyla kullan.
- **Yankı tuzakları:** İlanın kelimelerini ikiye ayır. *Sert anahtar kelimeler* (araç, yöntem, sertifika, unvan, alan terimi) aynen kullanılır. *İlanın üslubu ve cümleleri* CV'ye taşınmaz:
  - İlandan 5 veya daha fazla ardışık kelime kopyalama; cümleyi kullanıcının kendi deneyiminden yeniden yaz (hangi proje, ne yaptı, ne değişti). `ats_check.py` bunları "İlandan kopyalanmış ifadeler" başlığında listeler; hepsini gider.
  - Kullanıcının mülakatta kendiliğinden kullanmayacağı gayriresmi veya pazarlama dilini (şirket sloganları, "About us" ifadeleri) yazma.
  - **%100 eşleşme hedef değildir.** Eksik bir kelimeyi yalnızca skor için klişe cümleye veya yetenek satırına sıkıştırma; aynı ifadeyi tekrarlama. Kullanıcı bunu isterse riski (işe alımcıya ilandan kopyalanmış görünür, mülakatta kanıt istenir) önce söyle.
- Tarih aralıklarını düz tireyle yaz (`03/2022 - 08/2024`), uzun tire (– —) kullanma.
- **Asla uydurma:** olmayan deneyim, beceri, unvan, tarih, rakam ekleme. Eksik gereksinimler için kullanıcıya "Bu konuda deneyimin var mı?" diye sor; sadece evet derse ekle.
- **CV'de olmayan ama kullanıcının eklemek istediği özellik** (beceri, proje, sertifika, deneyim) olursa eklemeden önce onay al: ne ekleneceğini ve nereye (hangi bölüme/maddeye) yazılacağını göster, "Bu doğru ve CV'ne eklememi onaylıyor musun?" diye sor. Onay gelmeden ekleme. Onaylanan her ekleme için somut detay iste (nerede, ne zaman, hangi araç, sonuç).
- **Somut verileri artır:** Her deneyim maddesi için mümkün olduğunca sayı iste: yüzde artış/azalış, süre, hacim, bütçe, ekip büyüklüğü, kullanıcı/müşteri sayısı, tasarruf. Sayısı olmayan zayıf maddeleri listele ve kullanıcıya hedefli sorular sor ("Bu süreci kaç kişi kullandı?", "Ne kadar süre kısaldı?"). Tahmini rakamları kullanıcı "yaklaşık" olarak onaylarsa "~" veya "yaklaşık" ile yaz.
- Sayısal sonuç yoksa asla uydurma; kullanıcıdan iste. Rakam gelmezse maddeyi sayısız ama somut (ne, nasıl, hangi araçla) bırak.
- Şablon: `templates/cv-tr.md` veya `cv-en.md` (ilan diline göre).

## 5. Doğrula ve teslim et
- Her ilan için sonucu ayrı `output/cv-<sirket>.md` olarak yaz; `ats_check.py` ile tekrar çalıştır, eşleşme düşükse (ve kullanıcı sahipse) iyileştir.
- Kullanıcıya şunu sun: ne değiştirdin, eşleşme oranı öncesi/sonrası, hâlâ eksik olan gereksinimler. Birden çok ilanda tüm CV'leri tek tabloda özetle (ilan, öne çıkarılanlar, eşleşme %).
- **Formatı sor:** Teslimden önce `AskUserQuestion` ile CV'yi hangi formatta istediğini sor: PDF (önerilen), DOCX, Markdown/metin. Seçenekler arasında PDF'i ilk sırada "(Önerilen)" olarak ver.
- **PDF vurgusu:** Kullanıcıya açıkça söyle: başvuruda PDF genellikle en güvenli seçimdir; yazı tipi ve düzen bozulmadan her cihazda aynı görünür. Metin tabanlı (metni seçilebilen) PDF olmalı, resim/tarama olmamalı. **İlan veya başvuru formu hangi formatı istiyorsa onu gönder** (ör. DOCX); bu durumda o formatı üret ve kullanıcıya belirt.
- PDF üretimi: HTML'i elle yazma; kontrol ettiğin `.md` dosyasından betikle üret, böylece PDF ile kontrol edilen metin aynı olur:
  ```powershell
  python tools/build_pdf.py output/cv-<sirket>.md --out output/Ad_Soyad_CV.pdf
  ```
  Betik Edge veya Chrome'u (Windows/Mac/Linux) kendisi bulur. Bulamazsa HTML üretir; kullanıcıya tarayıcıdan Yazdır → PDF yapmasını söyle. Sonra **son PDF'i** `python tools/ats_check.py output/Ad_Soyad_CV.pdf inputs/ilan.txt` ile yeniden kontrol et.
- Seçenekler: `--font 10` 2 sayfaya sığdırmak için yazıyı küçültür (10–12 pt aralığında kal); `--justify` paragraf ve maddeleri iki yana yaslar. `--justify`'ı yalnızca kullanıcı isterse ekle (varsayılan sola yaslı) ve kullandıysan PDF'i açıp kelime aralarında büyük boşluk oluşup oluşmadığına bak.
- Çok sayfalı çıktıda sayfa sayısını kontrol et (en fazla 2).
- **Sayfa yerleşimi:** `ats_check.py` PDF'te yalnız kalan başlığı, rolün ortasında başlayan sayfayı ve neredeyse boş son sayfayı uyarır. Bu metne dayalı yaklaşık bir kontroldür; PDF'i ayrıca gözünle de aç ve bak. Düzeltmek için önce ilanla en az ilgili satırları kısalt.

## 6. İK uzmanı incelemesi (son adım)
CV hazır ve format seçildikten sonra `AskUserQuestion` ile sor: "CV'ni profesyonel bir İK uzmanı gözüyle de incelememi ister misin?" (Evet / Hayır). Hayır derse bitir; evet derse incele.

İnceleme, 6–10 saniyelik ilk taramayı yapan deneyimli bir işe alım uzmanı gibi yapılır. Her ilan için ayrı yap:
- **İlk izlenim:** Üstteki özet ve ilk maddeler hedef pozisyona uygunluğu hemen gösteriyor mu?
- **Hikâye ve tutarlılık:** Kariyer akışı mantıklı mı; boşluk, sık iş değişimi, unvan atlamaları, tarih çelişkileri var mı ve nasıl açıklanabilir?
- **Etki ve kanıt:** Maddeler görev mi başarı mı anlatıyor; sayısal sonuç yeterli mi?
- **Kırmızı bayraklar:** Abartı gibi görünen iddialar, belirsiz ifadeler, klişeler ("takım oyuncusu", "dinamik"), yazım ve dil hataları, gereksiz bilgi (fotoğraf, yaş, medeni hal).
- **Uygunluk:** Kıdem ile aranan seviye uyumlu mu; "aşırı nitelikli" veya "yetersiz" algısı doğar mı?
- **Mülakat riski:** CV'deki hangi iddialar mülakatta soru çekecek; kullanıcı hazır mı?

Çıktı: 10 üzerinden genel puan, en güçlü 3 yön, düzeltilmesi gereken sorunlar (öncelik sırasıyla: kritik / önemli / küçük) ve her biri için somut öneri. Önerileri CV'ye otomatik uygulama; kullanıcıya göster, onay gelenleri uygula (4. adımdaki uydurma yasağı ve onay kuralları geçerli). Uygulanırsa PDF'i yeniden üret.

## 7. Uygun iş ilanı bul (isteğe bağlı)
İK incelemesinden sonra `AskUserQuestion` ile sor: "CV'indeki özelliklere göre sana uygun güncel iş ilanları bulmamı ister misin?" (Evet / Hayır). Kullanıcı ilan bulmayı akışın başında da isteyebilir; ilanı olmayan kullanıcıya 2. adımda bu seçeneği sun.

Evet derse:
1. CV'den ve hedef cevaplarından arama profilini çıkar: pozisyon unvanları (eş anlamlılarıyla), temel beceriler, kıdem, şehir/uzaktan tercihi, dil. Eksik olanı (özellikle konum, çalışma şekli) kısaca sor ve profili kullanıcıya göster.
2. `WebSearch` veya tarayıcı aracıyla ara (Kariyer.net, LinkedIn, Indeed, şirket kariyer sayfaları vb.). Giriş gerektiren sitelerde (LinkedIn vb.) önce kullanıcıya sor: "Giriş yaparak aramamı ister misin?" Evet derse:
   - **Kullanıcı adı veya şifre isteme, sohbete yazdırma, forma kendin girme.** Bunlar yasaktır, kullanıcı kendisi verse de.
   - Siteyi yerleşik tarayıcı panelinde (built-in browser) aç ve kullanıcıdan giriş sayfasında **kendisinin** giriş yapmasını iste (şifre yöneticisi, 2 adımlı doğrulama dahil). "Giriş yaptım" demesini bekle.
   - Giriş yapıldıktan sonra o oturumda ilanları ara ve incele (kayıtlı aramalar, "Easy Apply" etiketi, kişiselleştirilmiş öneriler dahil). Oturumla ilgili hiçbir hesap ayarını değiştirme, çıkış yapma, başvuru gönderme veya mesaj atma.
   - Kullanıcı giriş yapmak istemezse veya yapamazsa açık ilanlarla devam et, gerekirse ilan metnini yapıştırmasını iste.
3. Güncel olmayan (kapanmış, eski tarihli) ilanları ele. **Sadece gerçekten açıp gördüğün ilanları ve linkleri ver;** link, şirket veya detay uydurma.
4. 5–10 ilanı tabloda sun: pozisyon, şirket, yer/çalışma şekli, link, neden uygun, tahmini uyumluluk (3. adımdaki formülle; ilan metnini okumadan kesin oran verme, "ön tahmin" de).
5. Kullanıcı hangi ilanlara başvurmak istediğini seçsin; seçilenleri ilan olarak alıp 2. adımdan itibaren her biri için ayrı CV hazırla.

Başvuruyu kullanıcı adına gönderme; başvuru kullanıcıya aittir.

## Gizlilik
CV ve ilan kişisel veridir: `inputs/` ve `output/` `.gitignore`'dadır; commit etme, GitHub'a gönderme.
