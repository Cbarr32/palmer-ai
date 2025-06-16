"""Initialize Palmer AI Database"""
import os
import sys
sys.path.insert(0, 'src')

from sqlalchemy import create_engine, text

# Database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/postgres')

try:
    # Connect to default database
    engine = create_engine(DATABASE_URL)
    
    # Create palmer_ai database if it doesn't exist
    with engine.connect() as conn:
        conn.execute(text("COMMIT"))  # Close any transaction
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'palmer_ai'")
        ).fetchone()
        
        if not exists:
            conn.execute(text("CREATE DATABASE palmer_ai"))
            print("✅ Created palmer_ai database")
        else:
            print("ℹ️  Database palmer_ai already exists")
            
except Exception as e:
    print(f"⚠️  Database setup skipped: {e}")
    print("   Run PostgreSQL and try again")
