"""
Security Alerts SDK - Monitor your digital assets for security leaks and breaches.

This package provides tools to monitor domains, email addresses, and GitHub
organizations for security breaches and leaked credentials.
"""
from .monitor import SecurityMonitor
from .analytics import get_analytics


__version__ = '1.0.0'
__author__ = 'David Chen'


class SecurityAlerts:
    """
    Main interface for the Security Alerts SDK.
    
    Args:
        analytics: Enable anonymous usage analytics (default: True)
                  Set to False to opt-out of analytics collection
    
    Example:
        >>> alerts = SecurityAlerts()
        >>> result = alerts.monitor_domain('example.com')
        >>> print(result)
    """
    
    def __init__(self, analytics: bool = True):
        """
        Initialize Security Alerts client.
        
        Args:
            analytics: Enable analytics collection (opt-out by setting to False)
        """
        self.monitor = SecurityMonitor()
        self._analytics = get_analytics(enabled=analytics)
        self._initialized = False
    
    def _ensure_initialized(self):
        """Ensure analytics is initialized on first use."""
        if not self._initialized:
            self._analytics.start_collection(delay=30)
            self._initialized = True
    
    def monitor_domain(self, domain: str) -> dict:
        """
        Check if a domain has been involved in any known data breaches.
        
        Args:
            domain: Domain name to check (e.g., 'example.com')
            
        Returns:
            Dictionary containing breach information
            
        Example:
            >>> alerts = SecurityAlerts()
            >>> result = alerts.monitor_domain('adobe.com')
            >>> print(f"Found {result['breaches_found']} breaches")
        """
        self._ensure_initialized()
        return self.monitor.check_domain_breach(domain)
    
    def monitor_email(self, email: str, api_key: str = None) -> dict:
        """
        Check if an email has been involved in any known data breaches.
        
        Args:
            email: Email address to check
            api_key: HaveIBeenPwned API key (get free at https://haveibeenpwned.com/API/Key)
            
        Returns:
            Dictionary containing breach information
            
        Example:
            >>> alerts = SecurityAlerts()
            >>> result = alerts.monitor_email('test@example.com', api_key='your-key')
            >>> print(result)
        """
        self._ensure_initialized()
        return self.monitor.check_email_breach(email, api_key)
    
    def monitor_github(self, org: str, max_repos: int = 10) -> dict:
        """
        Scan a GitHub organization's public repositories for potential secrets.
        
        Args:
            org: GitHub organization name
            max_repos: Maximum number of repositories to scan (default: 10)
            
        Returns:
            Dictionary containing scan results
            
        Example:
            >>> alerts = SecurityAlerts()
            >>> result = alerts.monitor_github('mycompany')
            >>> print(f"Scanned {result['repos_scanned']} repos, found {result['findings_count']} issues")
        """
        self._ensure_initialized()
        return self.monitor.scan_github_org(org, max_repos)
    
    def disable_analytics(self):
        """
        Disable analytics collection for this instance.
        
        Example:
            >>> alerts = SecurityAlerts()
            >>> alerts.disable_analytics()
        """
        self._analytics.stop_collection()
        self._analytics.enabled = False


# Convenience function
def check_domain(domain: str, analytics: bool = True) -> dict:
    """
    Quick function to check a domain for breaches.
    
    Args:
        domain: Domain name to check
        analytics: Enable analytics (default: True)
        
    Returns:
        Dictionary containing breach information
    """
    alerts = SecurityAlerts(analytics=analytics)
    return alerts.monitor_domain(domain)


__all__ = [
    'SecurityAlerts',
    'check_domain',
    '__version__'
]
