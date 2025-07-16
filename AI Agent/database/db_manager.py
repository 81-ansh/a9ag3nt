# database/db_manager.py
import oracledb as cx_Oracle
import logging
from typing import Optional, Dict, Any, List
import threading
from contextlib import contextmanager
from dataclasses import dataclass
import pandas as pd

@dataclass
class DatabaseConfig:
    host: str
    port: int
    service_name: str
    username: str
    password: str
    
    def get_dsn(self) -> str:
        return cx_Oracle.makedsn(self.host, self.port, service_name=self.service_name)

class DatabaseManager:
    """Singleton Database Manager for Oracle connections"""
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config: Optional[DatabaseConfig] = None
            self.connection_pool: Optional[cx_Oracle.SessionPool] = None
            self.logger = logging.getLogger(__name__)
            self.initialized = True
    
    def configure(self, config: DatabaseConfig, pool_size: int = 5):
        """Configure database connection with connection pooling"""
        self.config = config
        try:
            # Create connection pool
            self.connection_pool = cx_Oracle.SessionPool(
                user=config.username,
                password=config.password,
                dsn=config.get_dsn(),
                min=2,
                max=pool_size,
                increment=1,
                threaded=True,
                getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT
            )
            self.logger.info("Database connection pool created successfully")
            return True
        except cx_Oracle.Error as e:
            self.logger.error(f"Database connection failed: {e}")
            return False
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        if not self.connection_pool:
            raise Exception("Database not configured. Call configure() first.")
        
        connection = None
        try:
            connection = self.connection_pool.acquire()
            yield connection
        except cx_Oracle.Error as e:
            self.logger.error(f"Database operation failed: {e}")
            raise
        finally:
            if connection:
                self.connection_pool.release(connection)
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Execute SELECT query and return results as list of dictionaries"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params or {})
                columns = [desc[0] for desc in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            finally:
                cursor.close()
    
    def execute_non_query(self, query: str, params: Optional[Dict] = None) -> int:
        """Execute INSERT, UPDATE, DELETE queries"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params or {})
                conn.commit()
                return cursor.rowcount
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
    
    def execute_many(self, query: str, params_list: List[Dict]) -> int:
        """Execute query with multiple parameter sets"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.executemany(query, params_list)
                conn.commit()
                return cursor.rowcount
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
    
    def get_dataframe(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """Execute query and return results as pandas DataFrame"""
        with self.get_connection() as conn:
            return pd.read_sql(query, conn, params=params)
    
    def get_table_info(self, table_name: str) -> List[Dict]:
        """Get table structure information"""
        query = """
        SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, NULLABLE, DATA_DEFAULT
        FROM USER_TAB_COLUMNS 
        WHERE TABLE_NAME = UPPER(:table_name)
        ORDER BY COLUMN_ID
        """
        return self.execute_query(query, {'table_name': table_name})
    
    def get_all_tables(self) -> List[str]:
        """Get all table names in the current schema"""
        query = "SELECT TABLE_NAME FROM USER_TABLES ORDER BY TABLE_NAME"
        results = self.execute_query(query)
        return [row['TABLE_NAME'] for row in results]
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM DUAL")
                cursor.fetchone()
                cursor.close()
                return True
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def close_pool(self):
        """Close connection pool"""
        if self.connection_pool:
            self.connection_pool.close()
            self.connection_pool = None