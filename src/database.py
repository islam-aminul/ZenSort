import duckdb
from pathlib import Path


class FileHashDB:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.conn = None
        
    def connect(self):
        """Connect to DuckDB database."""
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.conn = duckdb.connect(str(self.db_path))
            self._create_tables()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def _create_tables(self):
        """Create file hash table with indexes for performance."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS file_hashes (
                id INTEGER PRIMARY KEY,
                file_path VARCHAR,
                file_hash VARCHAR NOT NULL,
                file_size BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_hash ON file_hashes(file_hash)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_path ON file_hashes(file_path)")
    
    def add_hash(self, file_path, file_hash, file_size):
        """Add file hash to database."""
        try:
            self.conn.execute(
                "INSERT INTO file_hashes (file_path, file_hash, file_size) VALUES (?, ?, ?)",
                [str(file_path), file_hash, file_size]
            )
            return True
        except Exception as e:
            print(f"Error adding hash: {e}")
            return False
    
    def check_duplicate(self, file_hash):
        """Check if hash exists and return matching file path."""
        try:
            result = self.conn.execute(
                "SELECT file_path FROM file_hashes WHERE file_hash = ? LIMIT 1",
                [file_hash]
            ).fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error checking duplicate: {e}")
            return None
    
    def get_stats(self):
        """Get database statistics."""
        try:
            result = self.conn.execute("SELECT COUNT(*) FROM file_hashes").fetchone()
            return {"total_files": result[0] if result else 0}
        except Exception:
            return {"total_files": 0}
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None