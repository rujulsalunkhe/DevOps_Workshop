import sqlite3
import logging
from datetime import datetime
from app.config import Config

logger = logging.getLogger(__name__)

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(Config().DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    try:
        conn = get_db_connection()
        
        # Create users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert sample data if table is empty
        count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        if count == 0:
            sample_users = [
                ('John Doe', 'john@example.com'),
                ('Jane Smith', 'jane@example.com'),
                ('Mike Johnson', 'mike@example.com')
            ]
            
            conn.executemany(
                'INSERT INTO users (name, email) VALUES (?, ?)',
                sample_users
            )
            
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def create_user(name, email):
    """Create a new user"""
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (name, email)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Created user: {name} ({email})")
        return user_id
        
    except sqlite3.IntegrityError:
        logger.warning(f"User creation failed - email already exists: {email}")
        raise ValueError("Email already exists")
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise

def get_all_users():
    """Get all users from database"""
    try:
        conn = get_db_connection()
        users = conn.execute(
            'SELECT id, name, email, created_at FROM users ORDER BY created_at DESC'
        ).fetchall()
        conn.close()
        
        return [dict(user) for user in users]
        
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise

def get_user_by_id(user_id):
    """Get user by ID"""
    try:
        conn = get_db_connection()
        user = conn.execute(
            'SELECT id, name, email, created_at FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()
        conn.close()
        
        return dict(user) if user else None
        
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {str(e)}")
        raise
