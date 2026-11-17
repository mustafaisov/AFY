# Aile Finans

Aile bütçesi, gelir/gider, varlıklar, borç taksitleri, BES, birikimli hayat sigortaları, hedefler ve emeklilik hesaplayıcı.

- Sunucu yok: program GitHub Pages'ten yüklenir, **tüm veriler kullanıcının kendi bilgisayarında** (tarayıcı + isteğe bağlı JSON dosyası) saklanır.
- İnternet sadece döviz/altın kurlarını almak için kullanılır.
- Chrome/Edge'de "Uygulamayı yükle" ile masaüstü uygulaması gibi kurulur, internetsiz de çalışır.

## Dosyalar

| Dosya | Görevi |
|---|---|
| `index.html` | Programın tamamı |
| `sw.js` | Çevrimdışı çalışma ve güncelleme |
| `manifest.webmanifest`, `icon-*.png` | Uygulama olarak kurulum |

## Yeni sürüm yayınlama

1. `index.html` içindeki `APP_VERSION` ve `sw.js` içindeki `VERSION` değerini **aynı** yeni numaraya çıkar (ör. 1.4.0 → 1.5.0).
2. Değişiklikleri `main` dalına gönder.
3. Kullanıcı programı açtığında (ya da en geç bir saat içinde) ekranın altında **"Güncelle"** düğmesi çıkar.

Veri yapısı değişirse eski verilerle uyum `defaults()` + `merge()` ile sağlanır; alan silmeyin, yeni alanları varsayılan değerle ekleyin.
