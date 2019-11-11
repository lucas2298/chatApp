# Database
import sqlite3
conn = sqlite3.connect('./Server/database/chatbot.db')
table = conn.cursor()
table.execute(
    """update alltag
    set response = :r
    where tag = :t""", {'r': 'Mình có thể giúp gì cho bạn?', 't': 'greeting'}
)

conn.commit()