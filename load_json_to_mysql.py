import json
import mysql.connector
from collections import defaultdict, Counter

# MySQL-ra konexioa sortzeko
conn = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root",
    database="mbtidb",
    charset='utf8mb4'
)
cursor = conn.cursor()

# users taula sortu
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    screen_name VARCHAR(255),
    location TEXT,
    verified BOOLEAN,
    statuses_count INT,
    total_retweet_count INT,
    total_favorite_count INT,
    total_hashtag_count INT,
    total_mentions_count INT,
    total_media_count INT
) CHARACTER SET utf8mb4;
""")

# edges taula sortu
cursor.execute("""
CREATE TABLE IF NOT EXISTS edges (
    id BIGINT PRIMARY KEY,
    follows JSON,
    is_followed_by JSON
) CHARACTER SET utf8mb4;
""")

# users taula datuz bete
with open("users1.json") as f:
    users = json.load(f)
    for user in users:
        cursor.execute("""
        INSERT INTO users (
            id, screen_name, location, verified, statuses_count,
            total_retweet_count, total_favorite_count, total_hashtag_count,
            total_mentions_count, total_media_count
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE id=id;
        """, (
            user["id"], user["screen_name"], user["location"], user["verified"],
            user["statuses_count"], user["total_retweet_count"], user["total_favorite_count"],
            user["total_hashtag_count"], user["total_mentions_count"], user["total_media_count"]
        ))

# edges taula datuz bete
with open("edges1.json") as f:
    edges = json.load(f)
    for edge in edges:
        cursor.execute("""
        INSERT INTO edges (id, follows, is_followed_by)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE id=id;
        """, (
            edge["id"], json.dumps(edge["follows"]), json.dumps(edge["is_followed_by"])
        ))


cursor = conn.cursor()

# sortu followers_count taula
cursor.execute("""
    CREATE TABLE IF NOT EXISTS followers_count (
        user_id BIGINT PRIMARY KEY,
        num_followers INT
    )
""")

# irakurri edges
cursor.execute("SELECT id, is_followed_by FROM edges")
rows = cursor.fetchall()

# followers_count bete datuz
for user_id, followers_json in rows:
    try:
        followers = json.loads(followers_json)
        num_followers = len(followers)
        cursor.execute(
            "INSERT INTO followers_count (user_id, num_followers) VALUES (%s, %s)",
            (user_id, num_followers)
        )
    except Exception as e:
        print(f"Error en user_id {user_id}: {e}")
        
        

conn.commit()
cursor.close()
conn.close()

