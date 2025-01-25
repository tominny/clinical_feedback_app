# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 10:58:02 2025

@author: f006q7g
"""

# db_manager.py

import psycopg2
import psycopg2.extras

class DBManager:
    def __init__(self, host, database, user, password, port=5432):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
    
    def connect(self):
        if not self.conn:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
        return self.conn

    def create_tables(self):
        conn = self.connect()
        cur = conn.cursor()
        # Create a 'users' table if it doesn't already exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            );
        """)
        # Create a 'uploads' table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                upload_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                file1_text TEXT,
                file2_text TEXT,
                file3_text TEXT,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        """)
        conn.commit()
        cur.close()
    
    def insert_user(self, username, hashed_password):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, hashed_password)
            VALUES (%s, %s) RETURNING user_id;
        """, (username, hashed_password))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return user_id

    def get_user_by_username(self, username):
        conn = self.connect()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            SELECT * FROM users WHERE username = %s;
        """, (username,))
        user = cur.fetchone()
        cur.close()
        return user

    def save_upload_and_feedback(self, user_id, file1_text, file2_text, file3_text, feedback):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO uploads (user_id, file1_text, file2_text, file3_text, feedback)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING upload_id;
        """, (user_id, file1_text, file2_text, file3_text, feedback))
        upload_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return upload_id

    def get_user_uploads(self, user_id):
        conn = self.connect()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            SELECT * FROM uploads WHERE user_id = %s ORDER BY created_at DESC;
        """, (user_id,))
        uploads = cur.fetchall()
        cur.close()
        return uploads
