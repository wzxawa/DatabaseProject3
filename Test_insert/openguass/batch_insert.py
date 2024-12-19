import psycopg2
import time

# 数据库连接配置
DB_CONFIG = {
    "dbname": "postgres",
    "user": "gaussdb",
    "password": "@Wzxyyds123",
    "host": "localhost",
    "port": 15432  # docker port
}

def generate_data(start, count):
    for i in range(start, start + count):
        yield (f"name_{i}", i)

def batch_insert(batch_size=1000):
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    start_time = time.time()
    data_batch = []
    for i, data in enumerate(generate_data(1, 300000), start=1):
        data_batch.append(data)
        if i % batch_size == 0:
            args_str = ",".join(cursor.mogrify("(%s, %s)", row).decode("utf-8") for row in data_batch)
            cursor.execute("INSERT INTO test_table (name, value) VALUES " + args_str)
            connection.commit()
            data_batch = []

    if data_batch:  # 插入剩余数据
        args_str = ",".join(cursor.mogrify("(%s, %s)", row).decode("utf-8") for row in data_batch)
        cursor.execute("INSERT INTO test_table (name, value) VALUES " + args_str)
        connection.commit()

    cursor.close()
    connection.close()
    print(f"Batch insert completed in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    print("Starting batch insert...")
    batch_insert()
