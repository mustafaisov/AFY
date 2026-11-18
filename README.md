# Aile Finans

Aile bütçesi, gelir/gider, varlıklar, borç taksitleri, BES, birikimli hayat sigortaları, hedefler ve emeklilik hesaplayıcı.

- Sunucu yok: program GitHub Pages'ten yüklenir, **tüm veriler kullanıcının kendi bilgisayarında** (tarayıcı + isteğe bağlı JSON dosyası) saklanır.
- İnternet sadece döviz/altın kurlarını almak için kullanılır.
- İsteğe bağlı kilit: parola (PBKDF2) ve parmak izi / Windows Hello (WebAuthn PRF); kilit açıkken veriler, yedekler ve bağlı kayıt dosyası AES-256-GCM ile şifrelenir.
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

## BES fon fiyatları (günlük)

- `prices/fonlar.txt`: takip edilen BES fon kodları (her satıra bir kod).
- `.github/workflows/fon-fiyatlari.yml` her gün iki kez `scripts/fon_fiyatlari.py`'yi çalıştırır; betik TEFAS'tan (tefas-crawler) fiyatları çekip `prices/emk.json`'a yazar.
- Program bu dosyayı aynı adresten okur. Dosyada sadece fon kodu, tarih ve fiyat vardır; kişisel veri yoktur.
- Yeni fon eklemek: kodu `prices/fonlar.txt`'ye ekleyip gönder; iş otomatik çalışır.

## BES içe aktarma dosyası

```json
{"type":"aile-finans-bes","v":1,"contracts":[{"name":"...","contractNo":"...","company":"...","start":"YYYY-MM-DD",
  "monthly":0,"day":1,"rate":20,"funds":[{"acct":"own|state","code":"AH5","name":"...","units":0,"price":0,"priceDate":"YYYY-MM-DD","alloc":0}]}]}
```
