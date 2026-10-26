from flask import Flask, render_template, request
from hibp_check import check_pwned_api
from database import init_db, insert_password, password_exists

app = Flask(__name__)

# Uygulama başlatıldığında SQLite veritabanını hazırla
init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password", "").strip()

        # 1️⃣ Boş parola kontrolü
        if not password:
            return render_template(
                "index.html",
                result="empty",
                message="Parola alanı boş bırakılamaz."
            )

        # 2️⃣ Parola daha önce veritabanına eklenmiş mi?
        if password_exists(password):
            return render_template(
                "index.html",
                result="exists",
                message="Bu parola daha önce sisteme kaydedilmiş."
            )

        # 3️⃣ Have I Been Pwned (HIBP) API kontrolü
        leaked_count = check_pwned_api(password)

        # ⬇⬇⬇ EN ÖNEMLİ GÜNCELLEME ⬇⬇⬇
        if leaked_count == -1:
            return render_template(
                "index.html",
                result="error",
                message="Dış servis şu anda yanıt vermiyor. Lütfen tekrar deneyin."
            )

        if leaked_count > 0:
            return render_template(
                "index.html",
                result="leaked",
                count=leaked_count,
                message=f"Bu parola {leaked_count} kez sızdırılmış!"
            )

        # 4️⃣ Temiz parola → veritabanına kaydet
        insert_password(password)

        return render_template(
            "index.html",
            result="clean",
            message="Parola güvenli. Başarıyla kaydedildi."
        )

    # GET isteği
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
