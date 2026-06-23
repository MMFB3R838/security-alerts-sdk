"""
Basic usage examples for Security Alerts SDK
"""
from security_alerts import SecurityAlerts, check_domain


def example_domain_check():
    """Example: Check a domain for breaches"""
    print("=" * 60)
    print("Example 1: Domain Breach Check")
    print("=" * 60)
    
    alerts = SecurityAlerts()
    result = alerts.monitor_domain('adobe.com')
    
    if result['status'] == 'success':
        print(f"✓ Found {result['breaches_found']} breaches for {result['domain']}")
        
        if result['breaches_found'] > 0:
            print("\nRecent breaches:")
            for breach in result['breaches'][:3]:  # Show first 3
                print(f"  - {breach['Name']}")
                print(f"    Date: {breach['BreachDate']}")
                print(f"    Compromised accounts: {breach['PwnCount']:,}")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
    
    print()


def example_github_scan():
    """Example: Scan GitHub organization for secrets"""
    print("=" * 60)
    print("Example 2: GitHub Secret Scanning")
    print("=" * 60)
    
    alerts = SecurityAlerts()
    result = alerts.monitor_github('netflix', max_repos=5)
    
    if result['status'] == 'success':
        print(f"✓ Scanned {result['repos_scanned']} repositories")
        print(f"✓ Found {result['findings_count']} potential issues")
        
        if result['findings_count'] > 0:
            print("\nFindings:")
            for finding in result['findings']:
                print(f"  ⚠️  {finding['type']} in {finding['repo']}/{finding['file']}")
                print(f"     Severity: {finding['severity']}")
        else:
            print("\n✓ No obvious secrets found in scanned repositories")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
    
    print()


def example_email_check():
    """Example: Check email for breaches (requires API key)"""
    print("=" * 60)
    print("Example 3: Email Breach Check")
    print("=" * 60)
    
    alerts = SecurityAlerts()
    result = alerts.monitor_email('test@example.com')
    
    # This will fail without API key, demonstrating the requirement
    if result['status'] == 'error':
        print(f"ℹ️  Note: {result['error']}")
        print(f"   {result.get('note', '')}")
    else:
        print(f"✓ Found {result['breaches_found']} breaches for email")
    
    print()


def example_opt_out_analytics():
    """Example: Disable analytics collection"""
    print("=" * 60)
    print("Example 4: Opt-out of Analytics")
    print("=" * 60)
    
    # Method 1: Disable at initialization
    alerts = SecurityAlerts(analytics=False)
    print("✓ Created SecurityAlerts instance with analytics disabled")
    
    # Method 2: Disable after initialization
    alerts2 = SecurityAlerts()
    alerts2.disable_analytics()
    print("✓ Disabled analytics on existing instance")
    
    # Method 3: Use convenience function with analytics disabled
    result = check_domain('example.com', analytics=False)
    print("✓ Used convenience function without analytics")
    
    print()


def example_quick_check():
    """Example: Quick domain check using convenience function"""
    print("=" * 60)
    print("Example 5: Quick Domain Check")
    print("=" * 60)
    
    # Simple one-liner for quick checks
    result = check_domain('linkedin.com')
    
    if result['status'] == 'success':
        print(f"✓ Quick check complete: {result['breaches_found']} breaches found")
    
    print()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Security Alerts SDK - Usage Examples")
    print("=" * 60 + "\n")
    
    # Run all examples
    example_domain_check()
    example_github_scan()
    example_email_check()
    example_opt_out_analytics()
    example_quick_check()
    
    print("=" * 60)
    print("Examples complete!")
    print("=" * 60)
    print("\nFor more information, visit:")
    print("https://github.com/davidchen-sec/security-alerts-sdk")
    print()
