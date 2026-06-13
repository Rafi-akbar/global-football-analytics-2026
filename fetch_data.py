import mysql.connector
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': 'localhost',
    'user': 'rafi_developer',
    'password': os.getenv('DB_PASSWORD'),
    'database': 'db_worldcup_science',
    'port': 3306
}

API_TOKEN = os.getenv('FOOTBALL_API_TOKEN')
API_URL = "https://api.football-data.org/v4/competitions/WC/matches"

def ambil_data_dari_api_riil():
    headers = { 
        "X-Auth-Token": API_TOKEN,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print("🌐 Sedang menembak API football-data.org...")
        respons = requests.get(API_URL, headers=headers, timeout=10)
        
        if respons.status_code == 200:
            data_mentah = respons.json()
            return data_mentah['matches']
        else:
            print(f"❌ Server menolak akses. Kode Eror: {respons.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Gagal terhubung ke internet: {e}")
        return []

def simpan_ke_database(daftar_pertandingan):
    if not daftar_pertandingan:
        print("⚠️ Tidak ada data pertandingan yang diproses.")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query_insert = """
        INSERT INTO tabel_pertandingan 
        (matchday, tim_home, tim_away, skor_home, skor_away, possession_home, possession_away, shots_home, shots_away, tanggal_tanding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for match in daftar_pertandingan:
            if match['status'] == 'FINISHED':
                tim_a = match['homeTeam']['name']
                tim_b = match['awayTeam']['name']
                skor_a = match['score']['fullTime']['home']
                skor_b = match['score']['fullTime']['away']
                matchday = match['matchday']
                tanggal = match['utcDate'][:10] 
                
                pos_a = 50
                pos_b = 50
                shot_a = 0
                shot_b = 0

                query_cek = "SELECT id FROM tabel_pertandingan WHERE tim_home = %s AND tim_away = %s"
                cursor.execute(query_cek, (tim_a, tim_b))
                if cursor.fetchone() is None:
                    cursor.execute(query_insert, (matchday, tim_a, tim_b, skor_a, skor_b, pos_a, pos_b, shot_a, shot_b, tanggal))
                    print(f"✔ Data Riil Tersimpan: {tim_a} ({skor_a}) vs {tim_b} ({skor_b})")

        conn.commit()
        cursor.close()
        conn.close()
        print("🎉 Sinkronisasi data riil selesai!")

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")

if __name__ == "__main__":
    data_live = ambil_data_dari_api_riil()
    simpan_ke_database(data_live)