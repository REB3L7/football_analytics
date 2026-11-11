
import psycopg2

connection = psycopg2.connect(
    dbname="football_analytics"
)

cursor = connection.cursor()

cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'live'
    ORDER BY table_name;
""")

print("PostgreSQL connection successful!")

print("\nLive schema tables:")

for table in cursor.fetchall():
    print("-", table[0])

cursor.close()
connection.close()
