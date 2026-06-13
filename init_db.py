import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'host': 'localhost',
    'user': 'rafi_developer',
    'password': os.getenv('DB_PASSWORD'),
    'database': 'db_worldcup_science',
    'port': 3306
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("🚀 Berhasil terhubung ke database MySQL di Docker!")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tabel_pertandingan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        matchday INT,
        tim_home VARCHAR(50),
        tim_away VARCHAR(50),
        skor_home INT,
        skor_away INT,
        possession_home INT,
        possession_away INT,
        shots_home INT,
        shots_away INT,
        tanggal_tanding DATE
    )
    """)
    print("✔ Tabel 'tabel_pertandingan' siap!")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tabel_prediksi_bracket (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fase VARCHAR(30),
        tim_1 VARCHAR(50),
        tim_2 VARCHAR(50),
        prediksi_pemenang VARCHAR(50)
    )
    """)
    print("✔ Tabel 'tabel_prediksi_bracket' siap!")

    conn.commit()
    cursor.close()
    conn.close()
    print("🎉 Inisialisasi struktur database selesai dengan sukses!")

except mysql.connector.Error as err:
    print(f"❌ Terjadi kesalahan: {err}")