# Parola Sızıntı Kontrol Sistemi

Yerel veritabanı kontrolünü Have I Been Pwned (HIBP) sızıntı sorgulamasıyla birleştiren, Python ve Flask tabanlı Türkçe bir web uygulaması. Proje, girilen parolanın sistemde daha önce kaydedilip kaydedilmediğini ve bilinen veri sızıntılarında yer alıp almadığını farklı amaçlara hizmet eden iki kontrol katmanıyla değerlendirir.

## Projenin amacı ve gelişimi

Projenin ilk sürümünde kendi yerel veritabanımızı oluşturduk ve girilen parolaları bu veritabanındaki kayıtlarla karşılaştırarak doğrulama yaptık. Bu aşama, veritabanı oluşturma, kayıt ekleme ve eşleşme sorgulama işlemleriyle temel kontrol altyapısını kurmamızı sağladı. Ancak kontrol kapsamı, kendi veritabanımıza eklediğimiz kayıtlarla sınırlıydı.

Sonraki aşamada, parola değerlendirmesini daha kapsamlı ve etkili hale getirmek amacıyla HIBP'nin Pwned Passwords API servisini projeye entegre ettik. Böylece uygulama, yerel kayıt kontrolünün ardından gerektiğinde dış servisteki bilinen sızıntı kayıtlarını da sorgulayabilen iki aşamalı bir yapıya dönüştü. Yerel veritabanı uygulamanın kayıt geçmişini tutarken HIBP, parolanın bilinen sızıntılardaki durumuna ilişkin ek bilgi sağlar.

Bu projedeki **çift kontrol**, yerel kayıt eşleşmesi ile dış servis üzerinden sızıntı sorgulamasını ifade eder. Kullanıcı kimliğini doğrulayan iki faktörlü kimlik doğrulama (2FA) değildir. Mevcut akışta yerel eşleşme bulunduğunda işlem sonlanır; HIBP yalnızca yerel veritabanında bulunmayan parolalar için sorgulanır.

## Projeyi öne çıkaran noktalar

- **Yerel ve dış kaynaklı kontrol:** Uygulamanın kayıt geçmişi ile bilinen sızıntı bilgileri aynı işlem akışında değerlendirilir.
- **Parolanın tamamını dış servise göndermeyen sorgulama:** HIBP isteğinde SHA-1 özetinin yalnızca ilk 5 karakteri paylaşılır; eşleşme uygulama sunucusunda tamamlanır.
- **Özet tabanlı yerel kayıt:** Parolalar yerel veritabanına düz metin olarak değil, SHA-256 özetleriyle eklenir.
- **Anlaşılır kullanıcı arayüzü:** Türkçe ekran, anlık temel parola gücü göstergesi, göster/gizle seçeneği ve işlem sırasında bekleme bildirimi sunulur.
- **Modüler Python yapısı:** Web akışı, API iletişimi ve veritabanı işlemleri ayrı dosyalarda tutulur.

Proje; API entegrasyonu, HTTP istekleri, hash algoritmaları, ilişkisel veritabanı sorguları ve istemci–sunucu iletişimini tek bir uygulamada bir araya getirir.

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

1. Kullanıcı parolayı forma yazar. JavaScript, uzunluk ve karakter türlerine göre temel bir güç göstergesi oluşturur.
2. Form `POST` isteğiyle Flask sunucusuna gönderilir. Başındaki ve sonundaki boşluklar kaldırıldıktan sonra boş giriş kontrolü yapılır.
3. **Birinci katman — yerel veritabanı:** Parolanın SHA-256 özeti hesaplanır ve `passwords.db` içindeki kayıtlarla karşılaştırılır. Eşleşme varsa sunucu `exists` sonucunu üretir ve kontrol burada sonlanır. Bu sonuç, parolanın sızdırıldığı anlamına gelmez; daha önce kaydedildiğini belirtir.
4. **İkinci katman — HIBP:** Yerel eşleşme yoksa parolanın SHA-1 özeti hesaplanır. İlk 5 karakter API'ye gönderilir ve yanıt içindeki özet son ekleri, kalan 35 karakterle sunucuda karşılaştırılır.
5. HIBP eşleşmesi varsa servisin bildirdiği görülme sayısı ekranda gösterilir. Bu parola yerel veritabanına kaydedilmez.
6. HIBP eşleşmesi yoksa parolanın SHA-256 özeti yerel veritabanına eklenir ve sızıntı kaydı bulunmadığına ilişkin sonuç gösterilir.
7. Dış servis zaman aşımına uğrarsa veya başarılı bir HTTP yanıtı dönmezse sunucu hata sonucu üretir; parola kaydedilmez.

Parolanın tamamı form üzerinden Flask sunucusuna ulaşır. Dış servise ise parolanın kendisi veya tam özeti gönderilmez.

### Yerel veritabanının rolü

Mevcut sürümde yerel veritabanı, HIBP sorgusunda eşleşme bulunmayan parolaların özetlerini tutar. Bu nedenle yerel kayıtlar bir sızdırılmış parola listesi değildir. Aynı parola tekrar girildiğinde kayıt geçmişi üzerinden tespit edilir; HIBP yeniden sorgulanmaz. Önceden kaydedilmiş bir parolanın sonradan sızıntı kayıtlarına eklenip eklenmediğini öğrenmek için yeniden sorgulama mekanizması ayrıca geliştirilmelidir.

## Teknik yapı

| Katman | Teknoloji | Görevi |
| --- | --- | --- |
| Sunucu | Python, Flask | `GET` ve `POST` isteklerini işlemek, kontrol sırasını yönetmek |
| Şablon | Jinja2, HTML | Sunucudan gelen sonuçları sayfaya aktarmak |
| Arayüz | CSS, JavaScript | Görünüm, parola gücü göstergesi ve etkileşimler |
| Yerel veri | SQLite, `sqlite3` | Parola özetlerini kaydetmek ve eşleşme sorgulamak |
| Özet hesaplama | Python `hashlib` | Yerelde SHA-256, HIBP sorgusunda SHA-1 üretmek |
| Dış servis iletişimi | `requests`, HIBP Pwned Passwords API | HTTPS üzerinden özet öneki sorgulamak |

### API entegrasyonu

`hibp_check.py` içindeki `check_pwned_api()` fonksiyonu, SHA-1 özetini büyük harfe dönüştürür ve `https://api.pwnedpasswords.com/range/{prefix}` adresine 5 saniyelik zaman aşımıyla istek gönderir. Yanıttaki `özet_son_eki:adet` satırları ayrıştırılır ve tam özet eşleşmesi sunucuda belirlenir.

Fonksiyonun dönüş değeri kontrol akışını yönlendirir: `-1` servis veya bağlantı hatasını, `0` eşleşme bulunmadığını, pozitif bir sayı ise eşleşen parolanın serviste bildirilen görülme sayısını ifade eder. SHA-1 burada dış servisin sorgu protokolü için kullanılır; yerel kayıt algoritması SHA-256'dır.

### Veritabanı tasarımı

Uygulama açılırken `init_db()` fonksiyonu `passwords` tablosunu yoksa oluşturur. Tabloda otomatik artan `id` ve `TEXT NOT NULL UNIQUE` tanımlı `password_text` alanları bulunur. Alanın adı `password_text` olsa da mevcut kod bu alana parolanın SHA-256 özetini yazar.

Ekleme ve arama işlemleri parametreli SQL sorgularıyla yapılır. Bağlantılar işlem sonunda kapatılır; SQLite bağlantısında 10 saniyelik kilit bekleme süresi tanımlıdır ve WAL günlük modu etkinleştirilmeye çalışılır.

### Parola gücü göstergesi

Tarayıcıdaki JavaScript; en az 8 karakter, büyük harf, rakam ve alfasayısal olmayan karakter koşullarını puanlar. Sonuç “Zayıf”, “Orta” veya “Güçlü” olarak gösterilir. Bu gösterge temel bir biçim kontrolüdür; HIBP sorgusundan bağımsızdır ve sunucuda parola kabulünü engelleyen bir kural olarak uygulanmaz.

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
