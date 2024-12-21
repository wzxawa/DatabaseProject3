import psycopg2
from psycopg2 import pool
import threading
import time

# 数据库连接配置
DB_CONFIG = {
    "dbname": "postgres",
    "user": "gaussdb",
    "password": "@Wzxyyds123",
    "host": "localhost",
    "port": 15432
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
    return time.time() - start_time

def test_thread_counts(thread_counts, total_rows=300000):
    for thread_count in thread_counts:
        print(f"\nTesting with {thread_count} threads:")
        elapsed_time = concurrent_insert(thread_count=thread_count, total_rows=total_rows)
        print(f"Time taken with {thread_count} threads: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    print("Starting concurrent insert testing...")

    # 要测试的线程数
    thread_counts_to_test = [1,2,4,8,16,32,64]
    test_thread_counts(thread_counts_to_test)
