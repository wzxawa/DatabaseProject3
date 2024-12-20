import psycopg2

# PostgreSQL 配置
config_postgres = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "wzx",
    "host": "localhost",
    "port": 5432
}

# OpenGauss 配置
config_opengauss = {
    "dbname": "postgres",
    "user": "gaussdb",
    "password": "@Wzxyyds123",
    "host": "localhost",
    "port": 15432  # Docker 中的 OpenGauss 端口
}

# 查询存储空间信息的 SQL
query_storage = """
SELECT 
    pg_size_pretty(pg_total_relation_size('{table_name}')) AS total_size,
    pg_size_pretty(pg_relation_size('{table_name}')) AS table_size,
    pg_size_pretty(pg_indexes_size('{table_name}')) AS index_size;
"""

# 查询索引存储详细信息的 SQL
query_indexes = """
SELECT 
    indexrelname,  -- 使用 OpenGauss 支持的列名
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM 
    pg_stat_user_indexes
WHERE 
    relname = '{table_name}';
"""

# 判断索引是否存在的 SQL
query_check_index = """
SELECT COUNT(*)
FROM pg_indexes
WHERE tablename = '{table_name}' AND indexname = '{index_name}';
"""

# 创建索引
def create_index(config, table_name, index_name, db_name):
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        print(f"\n[{db_name}] 检查索引 '{index_name}' 是否存在...")
        cursor.execute(query_check_index.format(table_name=table_name, index_name=index_name))
        index_exists = cursor.fetchone()[0] > 0

        if index_exists:
            print(f"[{db_name}] 索引 '{index_name}' 已存在，跳过创建。")
        else:
            print(f"[{db_name}] 正在为表 '{table_name}' 创建索引 '{index_name}'...")
            cursor.execute(f"CREATE INDEX {index_name} ON {table_name}(value)")
            conn.commit()
            print(f"[{db_name}] 索引 '{index_name}' 创建成功！")
    except Exception as e:
        print(f"[{db_name}] 创建索引时发生错误:", e)
    finally:
        if conn:
            conn.close()

# 查询存储空间和索引效率
def check_storage_efficiency(config, table_name, db_name):
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        # 查询表的存储空间占用
        print(f"\n[{db_name}] 查询表 '{table_name}' 的存储空间占用:")
        cursor.execute(query_storage.format(table_name=table_name))
        for row in cursor.fetchall():
            print(row)

        # 查询索引的存储效率
        print(f"\n[{db_name}] 查询表 '{table_name}' 的索引存储效率:")
        cursor.execute(query_indexes.format(table_name=table_name))
        for row in cursor.fetchall():
            print(row)

    except Exception as e:
        print(f"[{db_name}] 查询存储效率时发生错误:", e)
    finally:
        if conn:
            conn.close()

# 主函数
def main():
    table_name = "test_table"  # 替换为需要测试的表名
    index_name = "idx_value"  # 索引名称

    # 为 PostgreSQL 创建索引并测试存储效率
    print("\nPostgreSQL 存储效率测试:")
    create_index(config_postgres, table_name, index_name, "PostgreSQL")
    check_storage_efficiency(config_postgres, table_name, "PostgreSQL")

    # 为 OpenGauss 创建索引并测试存储效率
    print("\nOpenGauss 存储效率测试:")
    create_index(config_opengauss, table_name, index_name, "OpenGauss")
    check_storage_efficiency(config_opengauss, table_name, "OpenGauss")

if __name__ == "__main__":
    main()
