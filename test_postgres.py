import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="enfdb",
        user="enfdb",
        password="enfdb"
    )
    print("✅ PostgreSQL подключение успешно!")
    conn.close()
except Exception as e:
    print(f"❌ Ошибка: {e}")