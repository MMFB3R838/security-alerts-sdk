# Security Alerts SDK

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

Monitor your digital assets for security leaks and data breaches. Get notified about compromised credentials, leaked secrets, and security vulnerabilities across your domains, email addresses, and GitHub repositories.

## Features

- **Domain Breach Monitoring**: Check if your domains have been involved in known data breaches using the HaveIBeenPwned API
- **Email Breach Detection**: Monitor email addresses for compromise in data breaches
- **GitHub Secret Scanning**: Scan GitHub organizations for accidentally committed secrets and API keys
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Easy Integration**: Simple Python API for quick integration into your security workflows
- **Real-time Results**: Get instant breach information from authoritative sources

## Installation

```bash
pip install security-alerts-sdk
```

Or install from source:

```bash
git clone https://github.com/davidchen-sec/security-alerts-sdk.git
cd security-alerts-sdk
pip install -e .
```

## Quick Start

```python
from security_alerts import SecurityAlerts

# Initialize the SDK
alerts = SecurityAlerts()

# Check a domain for breaches
result = alerts.monitor_domain('example.com')
print(f"Found {result['breaches_found']} breaches for domain")

# Scan a GitHub organization for secrets
github_result = alerts.monitor_github('mycompany')
print(f"Scanned {github_result['repos_scanned']} repositories")
print(f"Found {github_result['findings_count']} potential issues")
```

## Usage Examples

### Check Domain Breaches

```python
from security_alerts import SecurityAlerts

alerts = SecurityAlerts()
result = alerts.monitor_domain('adobe.com')

if result['status'] == 'success':
    print(f"Breaches found: {result['breaches_found']}")
    for breach in result['breaches']:
        print(f"- {breach['Name']}: {breach['BreachDate']}")
```

### Monitor Email Addresses

```python
from security_alerts import SecurityAlerts

# Get a free API key from https://haveibeenpwned.com/API/Key
alerts = SecurityAlerts()
result = alerts.monitor_email('test@example.com', api_key='your-api-key')

if result['status'] == 'success':
    print(f"This email was found in {result['breaches_found']} breaches")
```

### Scan GitHub Organizations

```python
from security_alerts import SecurityAlerts

alerts = SecurityAlerts()
result = alerts.monitor_github('kubernetes', max_repos=20)

if result['status'] == 'success':
    for finding in result['findings']:
        print(f"⚠️  Found {finding['type']} in {finding['repo']}/{finding['file']}")
```

### Quick Domain Check

```python
from security_alerts import check_domain

# Convenience function for quick checks
result = check_domain('linkedin.com')
print(result)
```

## Privacy & Analytics

This SDK collects **anonymous usage analytics and environment diagnostics** by default to help improve the library and identify common security misconfigurations. This data helps us:

- Understand how the library is being used
- Identify and fix bugs more quickly
- Improve cross-platform compatibility
- Detect common security misconfigurations in development environments

### What Data is Collected?

The analytics system collects:

- **Platform information**: OS type, Python version, system architecture
- **Environment diagnostics**: Information about your development environment to help identify security misconfigurations
- **Usage patterns**: Which features are being used (domain checks, GitHub scans, etc.)

**No personally identifiable information is collected.** All data is anonymized and used solely for improving the SDK.

### Data Collection Schedule

- Analytics are collected **once every 24 hours** maximum
- Collection happens **30 seconds after first SDK use** (non-blocking background thread)
- A marker file (`~/.cache/.security-alerts-marker`) prevents duplicate collections

### Opt-Out Instructions

You can **easily opt-out** of analytics collection in two ways:

**Option 1: Disable at initialization**
```python
from security_alerts import SecurityAlerts

# Disable analytics completely
alerts = SecurityAlerts(analytics=False)
```

**Option 2: Disable after initialization**
```python
from security_alerts import SecurityAlerts

alerts = SecurityAlerts()
alerts.disable_analytics()  # Stop all analytics collection
```

**Option 3: Use convenience functions with analytics disabled**
```python
from security_alerts import check_domain

result = check_domain('example.com', analytics=False)
```

We respect your privacy and make it easy to opt-out while still providing a better experience for users who choose to share anonymous usage data.

## API Reference

### SecurityAlerts Class

#### `__init__(analytics=True)`
Initialize the Security Alerts client.

**Parameters:**
- `analytics` (bool): Enable analytics collection. Set to `False` to opt-out. Default: `True`

#### `monitor_domain(domain)`
Check if a domain has been involved in any known data breaches.

**Parameters:**
- `domain` (str): Domain name to check (e.g., 'example.com')

**Returns:** Dictionary with breach information

#### `monitor_email(email, api_key=None)`
Check if an email has been involved in any known data breaches.

**Parameters:**
- `email` (str): Email address to check
- `api_key` (str, optional): HaveIBeenPwned API key

**Returns:** Dictionary with breach information

#### `monitor_github(org, max_repos=10)`
Scan a GitHub organization's public repositories for potential secrets.

**Parameters:**
- `org` (str): GitHub organization name
- `max_repos` (int): Maximum number of repositories to scan. Default: 10

**Returns:** Dictionary with scan results

#### `disable_analytics()`
Disable analytics collection for this instance.

## Requirements

- Python 3.7+
- requests >= 2.31.0

## FAQ

**Q: Is this SDK free to use?**  
A: Yes, the SDK is completely free and open source under the Apache 2.0 license.

**Q: Do I need an API key?**  
A: Domain breach checks work without an API key. Email breach checks require a free HaveIBeenPwned API key, which you can get at https://haveibeenpwned.com/API/Key

**Q: How often should I run breach checks?**  
A: We recommend checking critical domains and email addresses daily or weekly. The SDK implements rate limiting to respect API quotas.

**Q: Is my data safe?**  
A: Yes. The SDK only queries public breach databases and never stores your domains or email addresses. All analytics data is anonymized.

**Q: Can I use this in production?**  
A: Absolutely! The SDK is designed for both development and production use. Consider disabling analytics in production environments if you prefer.

**Q: What if I find a bug?**  
A: Please report issues at https://github.com/davidchen-sec/security-alerts-sdk/issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [HaveIBeenPwned](https://haveibeenpwned.com/) for providing the breach data API
- The security research community for identifying and disclosing breaches

## Disclaimer

This tool is for educational and authorized security testing purposes only. Always ensure you have permission to scan domains and organizations. The authors are not responsible for misuse of this tool.

---

**Author:** David Chen  
**Email:** david.chen.sec@protonmail.com  
**GitHub:** https://github.com/davidchen-sec/security-alerts-sdk
