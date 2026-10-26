# Parola Sızıntı Kontrol Sistemi

Python ve Flask ile geliştirilmiş, parolaların bilinen veri sızıntılarında bulunup bulunmadığını kontrol eden Türkçe bir web uygulaması.

## Özellikler

- Have I Been Pwned Pwned Passwords API ile sızıntı sorgulama.
- Tarayıcıda uzunluk ve karakter türlerine dayalı basit parola gücü göstergesi.
- Parolayı gösterme ve gizleme.
- SQLite üzerinde daha önce kaydedilen parola özetlerini kontrol etme.
- Dış servis istekleri için 5 saniyelik zaman aşımı.

## Kurulum

Python 3 ve internet bağlantısı gerekir. Windows PowerShell üzerinde:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```

Tarayıcıda http://127.0.0.1:5000 adresini açın. `passwords.db` dosyası ilk çalıştırmada otomatik oluşturulur ve Git deposuna dahil edilmez.

## Çalışma şekli

1. Sunucu boş girişleri ve yerel veritabanında bulunan parolaları kontrol eder.
2. Girilen parolanın SHA-1 özeti hesaplanır. Dış servise yalnızca özetin ilk 5 karakteri gönderilir; kalan bölüm sunucuda karşılaştırılır.
3. Eşleşme varsa servisin bildirdiği görülme sayısı gösterilir.
4. Eşleşme yoksa parolanın SHA-256 özeti yerel SQLite veritabanına kaydedilir.

Parolanın tamamı form üzerinden Flask sunucusuna ulaşır. Dış servise ise parolanın kendisi veya tam özeti gönderilmez.

## Dosyalar

| Dosya | Açıklama |
| --- | --- |
| `app.py` | Flask rotası ve kontrol akışı |
| `hibp_check.py` | Pwned Passwords API sorgusu |
| `database.py` | SQLite bağlantısı ve parola özeti işlemleri |
| `templates/index.html` | HTML, sayfa stilleri ve JavaScript |
| `static/style.css` | Mevcut HTML tarafından kullanılmayan stil dosyası |
| `requirements.txt` | Python bağımlılıkları |

## Mevcut sınırlamalar

- Bir parolanın sızıntı verilerinde bulunmaması, güvenli olduğunu garanti etmez.
- Arayüzdeki “Parolanız hiçbir şekilde kaydedilmez” ifadesine rağmen uygulama parola özetlerini yerel veritabanına kaydeder.
- Boş giriş, daha önce kaydedilmiş parola ve API hatası için sunucuda sonuç üretilir; mevcut şablon bu mesajları göstermez.
- SHA-256 kayıtları tuzsuzdur. Bu yöntem gerçek bir kullanıcı giriş sisteminde parola saklamak için kullanılmamalıdır.
- Girdiye `strip()` uygulandığı için parolanın başındaki ve sonundaki boşluklar kaldırılır.
- `requirements.txt` içindeki MySQL paketi mevcut kod tarafından kullanılmaz; uygulama SQLite kullanır.
- Uygulama Flask geliştirme sunucusuyla çalışır; üretim ortamına dağıtım yapılandırması içermez.

Bu proje eğitim ve geliştirme amaçlıdır. Denemelerde gerçek hesap parolaları yerine örnek parolalar kullanın.
