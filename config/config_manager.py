# config/config_manager.py
import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import logging
from dotenv import load_dotenv
load_dotenv()


@dataclass
class DatabaseConfig:
    host: str
    port: int
    service_name: str
    username: str
    password: str

@dataclass
class AIConfig:
    gemini_api_key: str
    model_name: str = "models/gemini-2.0-flash"

@dataclass
class AppConfig:
    database: DatabaseConfig
    ai: AIConfig
    debug: bool = False
    log_level: str = "INFO"

class ConfigManager:
    """Manage application configuration"""
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self._config: Optional[AppConfig] = None
    
    def load_config(self) -> AppConfig:
        """Load configuration from file or environment variables"""
        if self._config:
            return self._config
        
        try:
            # Try to load from file first
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config_data = json.load(f)
                    self._config = self._dict_to_config(config_data)
            else:
                # Load from environment variables
                self._config = self._load_from_env()
                
            return self._config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            raise
    
    def _load_from_env(self) -> AppConfig:
        """Load configuration from environment variables"""
        return AppConfig(
            database=DatabaseConfig(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', '1521')),
                service_name=os.getenv('DB_SERVICE_NAME', 'XE'),
                username=os.getenv('DB_USERNAME', 'hr'),
                password=os.getenv('DB_PASSWORD', 'password')
            ),
            ai=AIConfig(
                gemini_api_key=os.getenv('GEMINI_API_KEY', ''),
                model_name=os.getenv('GEMINI_MODEL', 'models/gemini-2.0-flash')
            ),
            debug=os.getenv('DEBUG', 'False').lower() == 'true',
            log_level=os.getenv('LOG_LEVEL', 'INFO')
        )
    
    def _dict_to_config(self, config_dict: Dict[str, Any]) -> AppConfig:
        """Convert dictionary to AppConfig object"""
        return AppConfig(
            database=DatabaseConfig(**config_dict['database']),
            ai=AIConfig(**config_dict['ai']),
            debug=config_dict.get('debug', False),
            log_level=config_dict.get('log_level', 'INFO')
        )
    
    def save_config(self, config: AppConfig):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            config_dict = {
                'database': asdict(config.database),
                'ai': asdict(config.ai),
                'debug': config.debug,
                'log_level': config.log_level
            }
            
            with open(self.config_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
                
            self._config = config
            self.logger.info("Configuration saved successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            raise
    
    def get_config(self) -> AppConfig:
        """Get current configuration"""
        if not self._config:
            self._config = self.load_config()
        return self._config
    
    def update_database_config(self, **kwargs):
        """Update database configuration"""
        config = self.get_config()
        for key, value in kwargs.items():
            if hasattr(config.database, key):
                setattr(config.database, key, value)
        self.save_config(config)
    
    def update_ai_config(self, **kwargs):
        """Update AI configuration"""
        config = self.get_config()
        for key, value in kwargs.items():
            if hasattr(config.ai, key):
                setattr(config.ai, key, value)
        self.save_config(config)

# Create sample configuration file
def create_sample_config():
    """Create a sample configuration file"""
    sample_config = {
        "database": {
            "host": "your-vm-ip-address",
            "port": 1521,
            "service_name": "XE",
            "username": "your_username",
            "password": "your_password"
        },
        "ai": {
            "gemini_api_key": "your_gemini_api_key",
            "model_name": "models/gemini-2.0-flash"
        },
        "debug": True,
        "log_level": "DEBUG"
    }
    
    os.makedirs("config", exist_ok=True)
    with open("config/config.json", "w") as f:
        json.dump(sample_config, f, indent=2)
    
    print("Sample configuration created at config/config.json")
    print("Please update with your actual database and API credentials")

if __name__ == "__main__":
    create_sample_config()