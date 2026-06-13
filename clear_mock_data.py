import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': 'localhost',
    'user': 'rafi_developer',
    'password': os.getenv('DB_PASSWORD'),
    'database': 'db_worldcup_science',
    'port': 3306
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query_hapus = "TRUNCATE TABLE tabel_pertandingan"
    cursor.execute(query_hapus)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("🧹 Sukses! tabel_pertandingan telah dibersihkan dari data palsu.")

except mysql.connector.Error as err:
    print(f"❌ Gagal membersihkan database: {err}")