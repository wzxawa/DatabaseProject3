import psycopg2
from psycopg2 import pool
import threading
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

def worker(thread_id, start, count, connection_pool):
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    for data in generate_data(start, count):
        cursor.execute("INSERT INTO test_table (name, value) VALUES (%s, %s)", data)
        connection.commit()

    cursor.close()
    connection_pool.putconn(connection)
    print(f"Thread {thread_id} completed.")

def concurrent_insert(thread_count=10, total_rows=300000):
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, thread_count, **DB_CONFIG)
    rows_per_thread = total_rows // thread_count
    threads = []

    start_time = time.time()

    for i in range(thread_count):
        start = i * rows_per_thread + 1
        count = rows_per_thread
        if i == thread_count - 1:  # 最后一个线程处理剩余数据
            count += total_rows % thread_count
        thread = threading.Thread(target=worker, args=(i, start, count, connection_pool))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    connection_pool.closeall()
    print(f"Concurrent insert completed in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    print("Starting concurrent insert...")
    concurrent_insert(thread_count=10)
