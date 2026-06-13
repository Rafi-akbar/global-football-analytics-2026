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

prediksi_data = [
    {"fase": "Round of 32", "tim_1": "Belgium", "tim_2": "Spain", "prediksi_pemenang": "Belgium"},
    {"fase": "Round of 32", "tim_1": "Netherlands", "tim_2": "Switzerland", "prediksi_pemenang": "Netherlands"},
    {"fase": "Round of 32", "tim_1": "Morocco", "tim_2": "England", "prediksi_pemenang": "Morocco"},
    {"fase": "Round of 32", "tim_1": "Croatia", "tim_2": "Senegal", "prediksi_pemenang": "Croatia"},
    {"fase": "Round of 32", "tim_1": "Austria", "tim_2": "Japan", "prediksi_pemenang": "Austria"},
    {"fase": "Round of 32", "tim_1": "Argentina", "tim_2": "United States", "prediksi_pemenang": "Argentina"},
    {"fase": "Round of 32", "tim_1": "Bosnia and Herzegovina", "tim_2": "Mexico", "prediksi_pemenang": "Bosnia and Herzegovina"},
    {"fase": "Round of 32", "tim_1": "Norway", "tim_2": "Portugal", "prediksi_pemenang": "Norway"},
    {"fase": "Round of 32", "tim_1": "France", "tim_2": "Germany", "prediksi_pemenang": "France"},
    {"fase": "Round of 32", "tim_1": "Turkey", "tim_2": "Brazil", "prediksi_pemenang": "Brazil"},
    {"fase": "Round of 32", "tim_1": "Ivory Coast", "tim_2": "Czech Republic", "prediksi_pemenang": "Ivory Coast"},
    {"fase": "Round of 32", "tim_1": "Colombia", "tim_2": "Iran", "prediksi_pemenang": "Colombia"},
    {"fase": "Round of 32", "tim_1": "Egypt", "tim_2": "Canada", "prediksi_pemenang": "Egypt"},
    {"fase": "Round of 32", "tim_1": "Algeria", "tim_2": "Cape Verde", "prediksi_pemenang": "Algeria"},
    {"fase": "Round of 32", "tim_1": "Curaçao", "tim_2": "Australia", "prediksi_pemenang": "Curaçao"},
    {"fase": "Round of 32", "tim_1": "Uzbekistan", "tim_2": "South Korea", "prediksi_pemenang": "Uzbekistan"},
    {"fase": "16 Besar", "tim_1": "Belgium", "tim_2": "Netherlands", "prediksi_pemenang": "Belgium"},
    {"fase": "16 Besar", "tim_1": "Morocco", "tim_2": "Croatia", "prediksi_pemenang": "Croatia"},
    {"fase": "16 Besar", "tim_1": "Austria", "tim_2": "Argentina", "prediksi_pemenang": "Austria"},
    {"fase": "16 Besar", "tim_1": "Bosnia and Herzegovina", "tim_2": "Norway", "prediksi_pemenang": "Norway"},
    {"fase": "16 Besar", "tim_1": "France", "tim_2": "Brazil", "prediksi_pemenang": "France"},
    {"fase": "16 Besar", "tim_1": "Ivory Coast", "tim_2": "Colombia", "prediksi_pemenang": "Colombia"},
    {"fase": "16 Besar", "tim_1": "Egypt", "tim_2": "Algeria", "prediksi_pemenang": "Algeria"},
    {"fase": "16 Besar", "tim_1": "Curaçao", "tim_2": "Uzbekistan", "prediksi_pemenang": "Uzbekistan"},
    {"fase": "Perempat Final", "tim_1": "Belgium", "tim_2": "Croatia", "prediksi_pemenang": "Belgium"},
    {"fase": "Perempat Final", "tim_1": "Austria", "tim_2": "Norway", "prediksi_pemenang": "Austria"},
    {"fase": "Perempat Final", "tim_1": "France", "tim_2": "Colombia", "prediksi_pemenang": "France"},
    {"fase": "Perempat Final", "tim_1": "Algeria", "tim_2": "Uzbekistan", "prediksi_pemenang": "Algeria"},
    {"fase": "Semi Final", "tim_1": "Belgium", "tim_2": "Austria", "prediksi_pemenang": "Belgium"},
    {"fase": "Semi Final", "tim_1": "France", "tim_2": "Algeria", "prediksi_pemenang": "France"},
    {"fase": "Final", "tim_1": "Belgium", "tim_2": "France", "prediksi_pemenang": "Belgium"}
]

def masukan_prediksi(data_prediksi):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query_insert = """
        INSERT INTO tabel_prediksi_bracket (fase, tim_1, tim_2, prediksi_pemenang)
        VALUES (%s, %s, %s, %s)
        """

        for pred in data_prediksi:
            query_cek = "SELECT id FROM tabel_prediksi_bracket WHERE tim_1 = %s AND tim_2 = %s"
            cursor.execute(query_cek, (pred["tim_1"], pred["tim_2"]))
            hasil_cek = cursor.fetchone()

            if hasil_cek is not None:
                print(f"⚠️ Prediksi untuk {pred['tim_1']} vs {pred['tim_2']} sudah tercatat.")
            else:
                data_values = (
                    pred["fase"],
                    pred["tim_1"],
                    pred["tim_2"],
                    pred["prediksi_pemenang"]
                )
                cursor.execute(query_insert, data_values)
                print(f"✔ Prediksi Berhasil Disimpan: {pred['tim_1']} vs {pred['tim_2']} -> Juara: {pred['prediksi_pemenang']}")

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Eror pada database: {err}")

if __name__ == "__main__":
    print("⏳ Memasukkan cetak biru prediksi bracket ke database...")
    masukan_prediksi(prediksi_data)
    print("🎉 Selesai!")