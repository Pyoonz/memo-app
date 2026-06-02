import sqlite3
from collections import OrderedDict

DATABASE = "memo.db"


def get_connection():
    """データベースへの接続を取得する"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """データベースを初期化する（テーブルを作成する）"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_all_memos():
    """"全てのメモを取得する"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memos ORDER BY updated_at DESC")
    
    ordered_memos_list =[]
    for row in cursor.fetchall():
        ordered_memo = OrderedDict([
            ("id", row["id"]),
            ("title", row["title"]),
            ("body", row["body"]),
            ("created_at", row["created_at"]),
            ("updated_at", row["updated_at"])
        ])
        ordered_memos_list.append(ordered_memo)

    conn.close()
    return ordered_memos_list 


def search_memos(q): 
    """タイトルまたは本文でメモを検索する"""
    conn = get_connection()
    cursor = conn.cursor()

#LIKE検索のために検索クリエを ’%1%’ の形式にする
    search_query = f"%{q}%"

    cursor.execute(
    "SELECT * FROM memos WHERE title LIKE ? OR body LIKE ? ORDER BY updated_at DESC" , 
    (search_query, search_query)
)

#検索結果を OrderedDict のリストとして返す
    ordered_memos_list = []
    for row in cursor.fetchall():
        ordered_memo = OrderedDict([
            ("id", row["id"]),
            ("title", row["title"]),
            ("body", row["body"]),
            ("created_at", row["created_at"]),
            ("updated_at", row["updated_at"]),
        ])
        ordered_memos_list.append(ordered_memo)

    conn.close()
    return ordered_memos_list

def get_memo(memo_id):
    """"指定されたIDのメモを取得する"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memos WHERE id = ?", (memo_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        #ここでキーの順序を指定して新しい辞書を構築する（表示する時の並び順の指定）
        ordered_memo = OrderedDict([
            ("id", row["id"]),
            ("title", row["title"]),
            ("body", row["body"]),
            ("created_at", row["created_at"]),
            ("updated_at", row["updated_at"])
        ])
        return ordered_memo
    return None

def create_memo(title, body):
    """"新しいメモを作成する"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO memos (title, body) VALUES (?, ?)",
        (title, body)
    )
    conn.commit()
    memo_id = cursor.lastrowid
    conn.close()
    return memo_id


def update_memo(memo_id, title, body):
    """指定されたIDのメモを更新する"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE memos SET title = ?, body = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (title, body, memo_id)
    )
    conn.commit()
    changes = conn.total_changes
    conn.close()
    return changes > 0



def delete_memo(memo_id):
    """指定されたIDのメモを削除する"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memos WHERE id = ?", (memo_id,))
    conn.commit()
    changes = conn.total_changes
    conn.close()
    return changes > 0