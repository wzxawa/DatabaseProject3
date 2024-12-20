import psycopg2
import time

# OpenGauss 配置
config_og = {
    "dbname": "postgres",
    "user": "gaussdb",
    "password": "@Wzxyyds123",
    "host": "localhost",
    "port": 15432  # docker port    
}

def test_index_performance_og():
    try:
        conn = psycopg2.connect(**config_og)
        print("OpenGauss 数据库连接成功")
        with conn.cursor() as cursor:
            # 测试索引创建时间
            print("\n开始测试索引创建时间...")
            start_time = time.time()
            cursor.execute("CREATE INDEX idx_value ON test_table(value)")
            conn.commit()
            elapsed_time = time.time() - start_time
            print("OpenGauss 索引创建时间:", elapsed_time, "秒")

            # 测试索引查询性能
            print("\n开始测试索引查询性能...")
            start_time = time.time()
            cursor.execute("SELECT * FROM test_table WHERE value <= 500")
            rows = cursor.fetchall()
            elapsed_time = time.time() - start_time
            print("OpenGauss 索引查询耗时:", elapsed_time, "秒, 查询结果行数:", len(rows))
            
            # 删除索引以便多次测试
            cursor.execute("DROP INDEX IF EXISTS idx_value")
            conn.commit()

    except Exception as e:
        print("OpenGauss 索引性能测试出错:", e)
    finally:
        conn.close()
        print("OpenGauss 数据库连接关闭")

if __name__ == "__main__":
    test_index_performance_og()