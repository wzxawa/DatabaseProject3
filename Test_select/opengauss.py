import psycopg2
import time

# PostgreSQL 配置
config_opengauss = {
    "dbname": "postgres",
    "user": "gaussdb",
    "password": "@Wzxyyds123",
    "host": "localhost",
    "port": 15432  # docker port        
}

# 创建表结构
def create_tables(conn):
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            age INT,
            city VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INT,
            order_date DATE,
            amount DECIMAL(10, 2),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            price DECIMAL(10, 2),
            stock INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INT,
            product_id INT,
            quantity INT,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        """
    ]
    with conn.cursor() as cursor:
        for query in queries:
            cursor.execute(query)
        conn.commit()

# 插入测试数据
def insert_data(conn, num_users=100000, num_orders=300000, num_products=5000):
    with conn.cursor() as cursor:
        # 插入 users 数据
        for i in range(1, num_users + 1):
            cursor.execute("INSERT INTO users (name, age, city) VALUES (%s, %s, %s)", 
                           (f"User{i}", i % 100, f"City{i % 100}"))
        conn.commit()
        
        # 插入 products 数据
        for i in range(1, num_products + 1):
            cursor.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", 
                           (f"Product{i}", i * 1.23, i * 10))
        conn.commit()
        
        # 插入 orders 数据
        for i in range(1, num_orders + 1):
            cursor.execute("INSERT INTO orders (user_id, order_date, amount) VALUES (%s, %s, %s)", 
                           (i % num_users + 1, f"2023-{(i % 12) + 1}-01", i * 0.1))
        conn.commit()
        
        # 插入 order_items 数据
        for i in range(1, num_orders + 1):
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)", 
                           (i, i % num_products + 1, i % 10 + 1))
        conn.commit()

# 测试查询性能
def test_queries(conn):
    with conn.cursor() as cursor:
        # 测试 1: 简单 SELECT 查询
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM users WHERE age > 50")
        print("简单 SELECT 查询结果:", cursor.fetchone()[0])
        print("查询耗时:", time.time() - start_time, "秒")

        # 测试 2: 复杂 JOIN 查询
        start_time = time.time()
        cursor.execute("""
        SELECT u.name, SUM(o.amount) 
        FROM users u 
        JOIN orders o ON u.id = o.user_id 
        JOIN order_items oi ON o.id = oi.order_id 
        JOIN products p ON oi.product_id = p.id 
        WHERE p.price > 100 
        GROUP BY u.name 
        ORDER BY SUM(o.amount) DESC 
        LIMIT 10
        """)
        print("复杂 JOIN 查询结果:", cursor.fetchall())
        print("查询耗时:", time.time() - start_time, "秒")

        # 测试 3: 分页查询
        start_time = time.time()
        cursor.execute("SELECT * FROM users ORDER BY id LIMIT 50 OFFSET 1000")
        print("分页查询结果:", len(cursor.fetchall()))
        print("查询耗时:", time.time() - start_time, "秒")

# 主函数
def main():
    try:
        conn = psycopg2.connect(**config_opengauss)
        print("OpenGauss 数据库连接成功")
        
        create_tables(conn)
        print("表结构创建完成")
        
        # 插入数据（如果数据已经插入过，可以注释掉此行）
        insert_data(conn)
        print("数据插入完成")
        
        test_queries(conn)
        print("查询测试完成")
    
    except Exception as e:
        print("发生错误:", e)
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
