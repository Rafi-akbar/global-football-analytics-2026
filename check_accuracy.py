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

def hitung_akurasi_prediksi():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query_komparasi = """
        SELECT 
            p.fase, 
            p.tim_1, 
            p.tim_2, 
            p.prediksi_pemenang,
            CASE 
                WHEN r.skor_home > r.skor_away THEN r.tim_home
                WHEN r.skor_away > r.skor_home THEN r.tim_away
                ELSE 'SERI'
            END as pemenang_asli
        FROM tabel_prediksi_bracket p
        INNER JOIN tabel_pertandingan r 
            ON (p.tim_1 = r.tim_home AND p.tim_2 = r.tim_away)
            OR (p.tim_1 = r.tim_away AND p.tim_2 = r.tim_home)
        """
        
        cursor.execute(query_komparasi)
        semua_pertandingan = cursor.fetchall()

        total_pertandingan_selesai = 0
        prediksi_tepat = 0

        print("\n=== HASIL EVALUASI PREDIKSI BRACKET ===")
        print(f"{'FASE':<15} | {'PERTANDINGAN':<25} | {'PREDIKSI':<12} | {'REALITAS':<12} | {'STATUS'}")
        print("-" * 80)

        for baris in semua_pertandingan:
            fase = baris[0]
            tim_1 = baris[1]
            tim_2 = baris[2]
            prediksi = baris[3]
            realitas = baris[4]
            
            total_pertandingan_selesai += 1
            
            if prediksi == realitas:
                prediksi_tepat += 1
                status = "✅ TEMBUS"
            else:
                status = "❌ ZONK"
                
            print(f"{fase:<15} | {tim_1+' vs '+tim_2:<25} | {prediksi:<12} | {realitas:<12} | {status}")

        print("-" * 80)
        if total_pertandingan_selesai > 0:
            persentase_accuracy = (prediksi_tepat / total_pertandingan_selesai) * 100
            print(f"Total Pertandingan Babak Gugur yang Selesai: {total_pertandingan_selesai}")
            print(f"Prediksi Benar: {prediksi_tepat}")
            print(f"🎯 AKURASI MODEL MODEL KAMU: {persentase_accuracy:.2f}%")
        else:
            print("⚠️ Belum ada pertandingan babak gugur yang selesai di tabel_pertandingan riil.")
            print("Silakan tunggu hingga fase grup berakhir dan babak gugur dimulai!")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Terjadi kesalahan SQL: {err}")

if __name__ == "__main__":
    hitung_akurasi_prediksi()