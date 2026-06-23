"""
Utility functions for platform detection and path resolution.
"""
import os
import platform
from pathlib import Path
from typing import Optional


def get_platform() -> str:
    """
    Detect the current operating system platform.
    
    Returns:
        str: Platform identifier ('windows', 'macos', 'linux', or 'unknown')
    """
    system = platform.system().lower()
    if system == 'windows':
        return 'windows'
    elif system == 'darwin':
        return 'macos'
    elif system == 'linux':
        return 'linux'
    return 'unknown'


def get_home_dir() -> Path:
    """
    Get the user's home directory.
    
    Returns:
        Path: User home directory path
    """
    return Path.home()


def get_cache_dir() -> Path:
    """
    Get the cache directory for storing analytics metadata.
    
    Returns:
        Path: Cache directory path
    """
    cache_dir = get_home_dir() / '.cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_config_dir() -> Path:
    """
    Get the configuration directory.
    
    Returns:
        Path: Config directory path
    """
    config_dir = get_home_dir() / '.config'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def safe_read_file(filepath: str) -> Optional[str]:
    """
    Safely read a file without raising exceptions.
    
    Args:
        filepath: Path to the file to read
        
    Returns:
        File contents or None if error
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return None


def find_env_files(start_path: Optional[Path] = None) -> list:
    """
    Find .env files in common locations.
    
    Args:
        start_path: Starting directory (defaults to home)
        
    Returns:
        List of .env file paths
    """
    if start_path is None:
        start_path = get_home_dir()
    
    env_files = []
    common_dirs = ['Documents', 'Desktop', 'Projects', 'dev', 'workspace']
    
    for dir_name in common_dirs:
        dir_path = start_path / dir_name
        if dir_path.exists():
            try:
                for root, _, files in os.walk(dir_path):
                    for file in files:
                        if file.startswith('.env'):
                            env_files.append(os.path.join(root, file))
                    # Limit depth
                    if len(root.split(os.sep)) - len(str(dir_path).split(os.sep)) > 3:
                        break
            except Exception:
                continue
    
    return env_files
