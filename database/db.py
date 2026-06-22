import os
import shutil
import sqlite3
from datetime import datetime
from threading import Timer
from config import logger, DB_NAME, BACKUP_DIR, BACKUP_INTERVAL

class Database:
    def __init__(self, db_path=None, backup_dir=None, backup_interval=None, start_backup=True):
        self.db_path = db_path or DB_NAME
        self.backup_dir = backup_dir or BACKUP_DIR
        self.backup_interval = backup_interval or BACKUP_INTERVAL
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        
        if start_backup and self.db_path != ":memory:":
            self.start_backup_timer()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                         (user_id INTEGER PRIMARY KEY,
                          code TEXT,
                          verified INTEGER DEFAULT 0,
                          attempts INTEGER DEFAULT 3,
                          lang TEXT DEFAULT 'en',
                          filter TEXT DEFAULT 'filter_bw',
                          quality INTEGER DEFAULT 95,
                          pdf_format TEXT DEFAULT 'standard',
                          notifications INTEGER DEFAULT 1,
                          text_format TEXT DEFAULT 'pdf')''')
        # Migration for existing databases
        cursor.execute("PRAGMA table_info(users)")
        cols = [row[1] for row in cursor.fetchall()]
        if 'text_format' not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN text_format TEXT DEFAULT 'pdf'")
        self.conn.commit()

    def get_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

    def update_user(self, user_id, **kwargs):
        if not kwargs:
            return
        cursor = self.conn.cursor()
        set_clause = ', '.join([f"{key} = ?" for key in kwargs])
        values = list(kwargs.values())
        values.append(user_id)
        cursor.execute(f'UPDATE users SET {set_clause} WHERE user_id = ?', values)
        self.conn.commit()

    def create_user(self, user_id, code, lang='en'):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_id, code, lang) 
                          VALUES (?, ?, ?)''',
                       (user_id, code, lang))
        self.conn.commit()

    def start_backup_timer(self):
        t = Timer(self.backup_interval, self._run_backup)
        t.daemon = True
        t.start()

    def _run_backup(self):
        try:
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)

            backup_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copyfile(self.db_path, os.path.join(self.backup_dir, backup_name))
            logger.info(f"Created backup: {backup_name}")
        except Exception as e:
            logger.error(f"Error creating database backup: {e}")
        finally:
            self.start_backup_timer()

    def close(self):
        self.conn.close()

# Singleton instance for the main application
db = Database()
