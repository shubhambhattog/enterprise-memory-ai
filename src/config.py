"""
Configuration management for the Enterprise Memory AI system
"""

import os
from typing import Dict, Any


def get_config() -> Dict[str, Any]:
    """Get application configuration"""
    
    # OpenAI configuration
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    # Database URLs
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    neo4j_url = os.getenv("NEO4J_URL", "bolt://localhost:7687")
    neo4j_username = os.getenv("NEO4J_USERNAME", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
    
    # Langfuse configuration (optional)
    langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    
    config = {
        "version": "v1.1",
        
        # OpenAI configuration
        "openai": {
            "api_key": openai_api_key,
            "model": os.getenv("OPENAI_MODEL", "gpt-4")
        },
        
        # Memory configuration for Mem0
        "memory": {
            "embedder": {
                "provider": "openai",
                "config": {
                    "api_key": openai_api_key,
                    "model": "text-embedding-3-small"
                }
            },
            "llm": {
                "provider": "openai",
                "config": {
                    "api_key": openai_api_key,
                    "model": "gpt-4"
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "url": qdrant_url,
                    "collection_name": os.getenv("QDRANT_COLLECTION", "memory_vectors")
                }
            },
            "graph_store": {
                "provider": "neo4j",
                "config": {
                    "url": neo4j_url,
                    "username": neo4j_username,
                    "password": neo4j_password
                }
            }
        },
        
        # Application settings
        "app": {
            "host": os.getenv("APP_HOST", "0.0.0.0"),
            "port": int(os.getenv("APP_PORT", 8000)),
            "debug": os.getenv("DEBUG", "false").lower() == "true"
        }
    }
    
    # Add Langfuse configuration if keys are provided
    if langfuse_public_key and langfuse_secret_key:
        config["memory"]["observability"] = {
            "provider": "langfuse",
            "config": {
                "public_key": langfuse_public_key,
                "secret_key": langfuse_secret_key,
                "host": langfuse_host
            }
        }
    
    return config


def get_database_urls() -> Dict[str, str]:
    """Get database connection URLs"""
    return {
        "qdrant": os.getenv("QDRANT_URL", "http://localhost:6333"),
        "neo4j": os.getenv("NEO4J_URL", "bolt://localhost:7687"),
        "redis": os.getenv("REDIS_URL", "redis://localhost:6379")
    }


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration"""
    required_keys = [
        "openai.api_key",
        "memory.vector_store.config.url",
        "memory.graph_store.config.url"
    ]
    
    for key_path in required_keys:
        keys = key_path.split(".")
        current = config
        
        try:
            for key in keys:
                current = current[key]
            
            if not current:
                print(f"Missing required configuration: {key_path}")
                return False
                
        except KeyError:
            print(f"Missing required configuration: {key_path}")
            return False
    
    return True
