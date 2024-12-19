import psycopg2
import time

# 数据库连接配置
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "wzx",
    "host": "localhost",
    "port": 5432
}

def generate_data(start, count):
    for i in range(start, start + count):
        yield (f"name_{i}", i)

def single_insert():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    start_time = time.time()
    for data in generate_data(1, 300000):  # 插入30万条数据
        cursor.execute("INSERT INTO test_table (name, value) VALUES (%s, %s)", data)
        connection.commit()

    cursor.close()
    connection.close()
    print(f"Single insert completed in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    print("Starting single insert...")
    single_insert()
