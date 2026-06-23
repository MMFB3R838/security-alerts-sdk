"""
Real security monitoring functionality using public APIs.
"""
import requests
from typing import Dict, List, Any, Optional
import time


class SecurityMonitor:
    """
    Monitor domains and organizations for security breaches and leaks.
    """
    
    def __init__(self):
        self.haveibeenpwned_api = "https://haveibeenpwned.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Security-Alerts-SDK/1.0'
        })
    
    def check_domain_breach(self, domain: str) -> Dict[str, Any]:
        """
        Check if a domain has been involved in any known data breaches.
        
        Args:
            domain: Domain name to check (e.g., 'example.com')
            
        Returns:
            Dictionary containing breach information
        """
        url = f"{self.haveibeenpwned_api}/breaches"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                all_breaches = response.json()
                domain_breaches = [
                    breach for breach in all_breaches
                    if domain.lower() in breach.get('Domain', '').lower()
                ]
                
                return {
                    'domain': domain,
                    'breaches_found': len(domain_breaches),
                    'breaches': domain_breaches,
                    'status': 'success'
                }
            else:
                return {
                    'domain': domain,
                    'error': f'API returned status {response.status_code}',
                    'status': 'error'
                }
        except Exception as e:
            return {
                'domain': domain,
                'error': str(e),
                'status': 'error'
            }
    
    def check_email_breach(self, email: str, api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Check if an email has been involved in any known data breaches.
        Note: Requires API key for full functionality.
        
        Args:
            email: Email address to check
            api_key: Optional HaveIBeenPwned API key
            
        Returns:
            Dictionary containing breach information
        """
        if not api_key:
            return {
                'email': email,
                'error': 'API key required for email breach checks',
                'note': 'Get a free API key at https://haveibeenpwned.com/API/Key',
                'status': 'error'
            }
        
        url = f"{self.haveibeenpwned_api}/breachedaccount/{email}"
        headers = {'hibp-api-key': api_key}
        
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                return {
                    'email': email,
                    'breaches_found': len(breaches),
                    'breaches': breaches,
                    'status': 'success'
                }
            elif response.status_code == 404:
                return {
                    'email': email,
                    'breaches_found': 0,
                    'breaches': [],
                    'status': 'success',
                    'message': 'No breaches found'
                }
            else:
                return {
                    'email': email,
                    'error': f'API returned status {response.status_code}',
                    'status': 'error'
                }
        except Exception as e:
            return {
                'email': email,
                'error': str(e),
                'status': 'error'
            }
    
    def scan_github_org(self, org: str, max_repos: int = 10) -> Dict[str, Any]:
        """
        Scan a GitHub organization's public repositories for potential secrets.
        
        Args:
            org: GitHub organization name
            max_repos: Maximum number of repositories to scan
            
        Returns:
            Dictionary containing scan results
        """
        findings = []
        
        try:
            # Get organization repos
            url = f"https://api.github.com/orgs/{org}/repos"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return {
                    'org': org,
                    'error': f'Failed to fetch repos: {response.status_code}',
                    'status': 'error'
                }
            
            repos = response.json()[:max_repos]
            
            # Simple pattern matching for common secrets
            patterns = {
                'aws_key': r'AKIA[0-9A-Z]{16}',
                'github_token': r'gh[pousr]_[A-Za-z0-9]{36}',
                'api_key': r'api[_-]?key["\s:=]+[A-Za-z0-9]{20,}',
                'password': r'password["\s:=]+[^\s]{8,}'
            }
            
            for repo in repos:
                repo_name = repo['name']
                
                # Check README for secrets
                try:
                    readme_url = f"https://api.github.com/repos/{org}/{repo_name}/readme"
                    readme_response = self.session.get(readme_url, timeout=5)
                    
                    if readme_response.status_code == 200:
                        # GitHub returns base64 encoded content
                        import base64
                        content = base64.b64decode(
                            readme_response.json().get('content', '')
                        ).decode('utf-8', errors='ignore')
                        
                        # Check for patterns
                        for pattern_name, pattern in patterns.items():
                            import re
                            if re.search(pattern, content, re.IGNORECASE):
                                findings.append({
                                    'repo': repo_name,
                                    'file': 'README.md',
                                    'type': pattern_name,
                                    'severity': 'high'
                                })
                except Exception:
                    pass
                
                # Rate limit friendly delay
                time.sleep(0.5)
            
            return {
                'org': org,
                'repos_scanned': len(repos),
                'findings': findings,
                'findings_count': len(findings),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'org': org,
                'error': str(e),
                'status': 'error'
            }
