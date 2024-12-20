import psycopg2
import time

# PostgreSQL 配置
config_db = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "wzx",
    "host": "localhost",
    "port": 5432
}

# 更新测试
def test_updates(conn):
    with conn.cursor() as cursor:
        # 批量更新测试
        conn.autocommit = False
        try:
            print("\n开始批量更新...")
            start_time = time.time()
            cursor.execute("UPDATE users SET city = 'UpdatedCity' WHERE age < 50")
            elapsed_time = time.time() - start_time
            print("批量更新耗时:", elapsed_time, "秒")
            conn.rollback()
        except Exception as e:
            print("批量更新出错:", e)
        
        # 带条件更新测试
        try:
            print("\n开始带条件更新...")
            start_time = time.time()
            cursor.execute("UPDATE users SET city = 'ConditionCity' WHERE id BETWEEN 1000 AND 2000")
            elapsed_time = time.time() - start_time
            print("带条件更新耗时:", elapsed_time, "秒")
            conn.rollback()
        except Exception as e:
            print("带条件更新出错:", e)


# 主函数
def main():
    try:
        conn = psycopg2.connect(**config_db)
        print("PostgreSQL 数据库连接成功")
        
        print("\n开始测试更新性能:")
        test_updates(conn)
        
    except Exception as e:
        print("发生错误:", e)
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
