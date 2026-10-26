import hashlib
import requests
from requests.exceptions import RequestException


def check_pwned_api(password):
    """
    Parolanın Have I Been Pwned veritabanında
    kaç kez sızdırıldığını kontrol eder.

    Dönüş:
    -1 → API hatası / timeout
     0 → temiz
    >0 → sızdırılma sayısı
    """
    try:
        sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()

        prefix = sha1_password[:5]
        suffix = sha1_password[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return -1

        hashes = (line.split(":") for line in response.text.splitlines())

        for h, count in hashes:
            if h == suffix:
                return int(count)

        return 0

    except RequestException:
        # ⬅⬅⬅ İKİNCİ PAROLADA ÇÖKMENİN SEBEBİ BUYDU
        return -1
