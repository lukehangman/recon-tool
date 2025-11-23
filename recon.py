#!/usr/bin/env python3
"""
Recon Automation Tool v1.0.0
A comprehensive reconnaissance tool for cybersecurity professionals
"""

import argparse
import socket
import ssl
import sys
import json
import dns.resolver
import requests
import whois
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import subprocess
import re
import os

# ANSI Color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ReconTool:
    def __init__(self, target, ports=None, timeout=3, threads=10, wordlist=None):
        """
        Initialize the reconnaissance tool
        
        Args:
            target (str): Target domain or IP address
            ports (list): List of ports to scan
            timeout (int): Connection timeout in seconds
            threads (int): Number of concurrent threads
            wordlist (str): Path to subdomain wordlist
        """
        self.target = target
        self.ports = ports or [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080, 8443]
        self.timeout = timeout
        self.threads = threads
        self.wordlist = wordlist or "wordlists/subdomains.txt"
        self.results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'dns_records': {},
            'subdomains': [],
            'open_ports': [],
            'http_headers': {},
            'technologies': [],
            'whois_info': {},
            'banners': {}
        }

    def print_banner(self):
        """Display tool banner"""
        banner = f"""
{Colors.OKCYAN}
╦═╗╔═╗╔═╗╔═╗╔╗╔  ╔╦╗╔═╗╔═╗╦  
╠╦╝║╣ ║  ║ ║║║║   ║ ║ ║║ ║║  
╩╚═╚═╝╚═╝╚═╝╝╚╝   ╩ ╚═╝╚═╝╩═╝
{Colors.ENDC}
{Colors.BOLD}Recon Automation Tool v1.0.0{Colors.ENDC}
{Colors.OKBLUE}Target: {self.target}{Colors.ENDC}
{Colors.OKBLUE}Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}
{"=" * 50}
"""
        print(banner)

    def dns_lookup(self):
        """Perform comprehensive DNS lookups"""
        print(f"\n{Colors.HEADER}[*] Starting DNS Enumeration...{Colors.ENDC}")
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(self.target, record_type)
                records = [str(rdata) for rdata in answers]
                self.results['dns_records'][record_type] = records
                
                print(f"{Colors.OKGREEN}[+] {record_type} Records:{Colors.ENDC}")
                for record in records:
                    print(f"    {record}")
            except dns.resolver.NoAnswer:
                print(f"{Colors.WARNING}[-] No {record_type} records found{Colors.ENDC}")
            except dns.resolver.NXDOMAIN:
                print(f"{Colors.FAIL}[!] Domain does not exist{Colors.ENDC}")
                return
            except Exception as e:
                print(f"{Colors.WARNING}[-] Error querying {record_type}: {str(e)}{Colors.ENDC}")

        # PTR (Reverse DNS) lookup
        try:
            ip = socket.gethostbyname(self.target)
            reversed_ip = '.'.join(reversed(ip.split('.')))
            ptr_query = f"{reversed_ip}.in-addr.arpa"
            answers = dns.resolver.resolve(ptr_query, 'PTR')
            ptr_records = [str(rdata) for rdata in answers]
            self.results['dns_records']['PTR'] = ptr_records
            print(f"{Colors.OKGREEN}[+] PTR Records:{Colors.ENDC}")
            for record in ptr_records:
                print(f"    {record}")
        except Exception as e:
            print(f"{Colors.WARNING}[-] PTR lookup failed: {str(e)}{Colors.ENDC}")

    def subdomain_enumeration(self):
        """Enumerate subdomains using wordlist"""
        print(f"\n{Colors.HEADER}[*] Starting Subdomain Enumeration...{Colors.ENDC}")
        
        if not os.path.exists(self.wordlist):
            print(f"{Colors.WARNING}[-] Wordlist not found: {self.wordlist}{Colors.ENDC}")
            return

        try:
            with open(self.wordlist, 'r') as f:
                subdomains = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error reading wordlist: {str(e)}{Colors.ENDC}")
            return

        print(f"{Colors.OKBLUE}[*] Testing {len(subdomains)} subdomains...{Colors.ENDC}")
        
        found_subdomains = []
        
        def check_subdomain(subdomain):
            full_domain = f"{subdomain}.{self.target}"
            try:
                socket.gethostbyname(full_domain)
                return full_domain
            except socket.gaierror:
                return None

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(check_subdomain, sub): sub for sub in subdomains}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found_subdomains.append(result)
                    print(f"{Colors.OKGREEN}[+] Found: {result}{Colors.ENDC}")

        self.results['subdomains'] = found_subdomains
        print(f"\n{Colors.OKGREEN}[+] Total subdomains found: {len(found_subdomains)}{Colors.ENDC}")

    def port_scan(self):
        """Scan common ports on target"""
        print(f"\n{Colors.HEADER}[*] Starting Port Scan...{Colors.ENDC}")
        
        try:
            target_ip = socket.gethostbyname(self.target)
            print(f"{Colors.OKBLUE}[*] Target IP: {target_ip}{Colors.ENDC}")
        except socket.gaierror:
            print(f"{Colors.FAIL}[!] Could not resolve hostname{Colors.ENDC}")
            return

        open_ports = []

        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                result = sock.connect_ex((target_ip, port))
                sock.close()
                
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    return {'port': port, 'service': service}
            except Exception as e:
                pass
            return None

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(scan_port, port): port for port in self.ports}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
                    print(f"{Colors.OKGREEN}[+] Port {result['port']} ({result['service']}) - OPEN{Colors.ENDC}")

        self.results['open_ports'] = open_ports
        print(f"\n{Colors.OKGREEN}[+] Total open ports: {len(open_ports)}{Colors.ENDC}")

    def banner_grabbing(self):
        """Grab banners from open ports"""
        print(f"\n{Colors.HEADER}[*] Starting Banner Grabbing...{Colors.ENDC}")
        
        if not self.results['open_ports']:
            print(f"{Colors.WARNING}[-] No open ports to grab banners from{Colors.ENDC}")
            return

        try:
            target_ip = socket.gethostbyname(self.target)
        except socket.gaierror:
            return

        for port_info in self.results['open_ports']:
            port = port_info['port']
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                sock.connect((target_ip, port))
                
                # Send HTTP request for web ports
                if port in [80, 443, 8080, 8443]:
                    sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
                
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                sock.close()
                
                if banner:
                    self.results['banners'][port] = banner
                    print(f"{Colors.OKGREEN}[+] Port {port} Banner:{Colors.ENDC}")
                    print(f"    {banner[:200]}...")
            except Exception as e:
                pass

    def http_headers(self):
        """Retrieve HTTP/HTTPS headers"""
        print(f"\n{Colors.HEADER}[*] Retrieving HTTP Headers...{Colors.ENDC}")
        
        protocols = ['http', 'https']
        
        for protocol in protocols:
            url = f"{protocol}://{self.target}"
            try:
                response = requests.get(url, timeout=self.timeout, verify=False, allow_redirects=True)
                self.results['http_headers'][protocol] = dict(response.headers)
                
                print(f"{Colors.OKGREEN}[+] {protocol.upper()} Headers:{Colors.ENDC}")
                for key, value in response.headers.items():
                    print(f"    {key}: {value}")
                
                # Check for security headers
                security_headers = ['Strict-Transport-Security', 'X-Frame-Options', 
                                  'X-Content-Type-Options', 'Content-Security-Policy']
                missing_headers = [h for h in security_headers if h not in response.headers]
                
                if missing_headers:
                    print(f"{Colors.WARNING}[!] Missing security headers: {', '.join(missing_headers)}{Colors.ENDC}")
                    
            except requests.exceptions.SSLError:
                print(f"{Colors.WARNING}[-] SSL Error for {protocol}://{self.target}{Colors.ENDC}")
            except requests.exceptions.ConnectionError:
                print(f"{Colors.WARNING}[-] Connection failed for {protocol}://{self.target}{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.WARNING}[-] Error accessing {protocol}://{self.target}: {str(e)}{Colors.ENDC}")

    def technology_detection(self):
        """Detect web technologies"""
        print(f"\n{Colors.HEADER}[*] Detecting Technologies...{Colors.ENDC}")
        
        technologies = []
        
        # Check from HTTP headers
        for protocol, headers in self.results['http_headers'].items():
            if 'Server' in headers:
                technologies.append(f"Web Server: {headers['Server']}")
            if 'X-Powered-By' in headers:
                technologies.append(f"Powered By: {headers['X-Powered-By']}")
            if 'X-AspNet-Version' in headers:
                technologies.append(f"ASP.NET: {headers['X-AspNet-Version']}")

        # Try to detect from page content
        try:
            response = requests.get(f"http://{self.target}", timeout=self.timeout, verify=False)
            content = response.text.lower()
            
            # Common technology patterns
            tech_patterns = {
                'WordPress': r'wp-content|wordpress',
                'Joomla': r'joomla',
                'Drupal': r'drupal',
                'React': r'react',
                'Angular': r'ng-|angular',
                'Vue.js': r'vue\.js|__vue',
                'jQuery': r'jquery',
                'Bootstrap': r'bootstrap',
                'PHP': r'\.php',
            }
            
            for tech, pattern in tech_patterns.items():
                if re.search(pattern, content):
                    technologies.append(tech)
        except:
            pass

        self.results['technologies'] = list(set(technologies))
        
        if technologies:
            print(f"{Colors.OKGREEN}[+] Detected Technologies:{Colors.ENDC}")
            for tech in technologies:
                print(f"    {tech}")
        else:
            print(f"{Colors.WARNING}[-] No technologies detected{Colors.ENDC}")

    def whois_lookup(self):
        """Perform WHOIS lookup"""
        print(f"\n{Colors.HEADER}[*] Performing WHOIS Lookup...{Colors.ENDC}")
        
        try:
            w = whois.whois(self.target)
            
            # Extract relevant information
            whois_data = {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'name_servers': w.name_servers,
                'status': w.status,
                'emails': w.emails,
                'country': w.country
            }
            
            self.results['whois_info'] = whois_data
            
            print(f"{Colors.OKGREEN}[+] WHOIS Information:{Colors.ENDC}")
            for key, value in whois_data.items():
                if value:
                    print(f"    {key}: {value}")
                    
        except Exception as e:
            print(f"{Colors.WARNING}[-] WHOIS lookup failed: {str(e)}{Colors.ENDC}")

    def generate_report(self, output_format='text'):
        """Generate reconnaissance report"""
        print(f"\n{Colors.HEADER}[*] Generating Report...{Colors.ENDC}")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"reports/recon_{self.target}_{timestamp}"
        
        # Ensure reports directory exists
        os.makedirs('reports', exist_ok=True)
        
        if output_format == 'json':
            filename = f"{base_filename}.json"
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=4)
            print(f"{Colors.OKGREEN}[+] JSON report saved: {filename}{Colors.ENDC}")
        
        elif output_format == 'html':
            filename = f"{base_filename}.html"
            html_content = self._generate_html_report()
            with open(filename, 'w') as f:
                f.write(html_content)
            print(f"{Colors.OKGREEN}[+] HTML report saved: {filename}{Colors.ENDC}")
        
        else:  # text format
            filename = f"{base_filename}.txt"
            with open(filename, 'w') as f:
                f.write(f"Reconnaissance Report\n")
                f.write(f"Target: {self.target}\n")
                f.write(f"Timestamp: {self.results['timestamp']}\n")
                f.write("=" * 60 + "\n\n")
                
                # DNS Records
                f.write("DNS RECORDS\n")
                f.write("-" * 60 + "\n")
                for record_type, records in self.results['dns_records'].items():
                    f.write(f"{record_type}: {', '.join(records)}\n")
                f.write("\n")
                
                # Subdomains
                f.write("SUBDOMAINS\n")
                f.write("-" * 60 + "\n")
                for subdomain in self.results['subdomains']:
                    f.write(f"{subdomain}\n")
                f.write("\n")
                
                # Open Ports
                f.write("OPEN PORTS\n")
                f.write("-" * 60 + "\n")
                for port in self.results['open_ports']:
                    f.write(f"Port {port['port']} ({port['service']})\n")
                f.write("\n")
                
                # Technologies
                f.write("TECHNOLOGIES\n")
                f.write("-" * 60 + "\n")
                for tech in self.results['technologies']:
                    f.write(f"{tech}\n")
                
            print(f"{Colors.OKGREEN}[+] Text report saved: {filename}{Colors.ENDC}")

    def _generate_html_report(self):
        """Generate HTML report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Recon Report - {self.target}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f4f4f4; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #4CAF50; margin-top: 30px; }}
        .info {{ background: #e8f5e9; padding: 15px; border-left: 4px solid #4CAF50; margin: 10px 0; }}
        .warning {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 10px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #4CAF50; color: white; }}
        .port {{ display: inline-block; background: #4CAF50; color: white; padding: 5px 10px; margin: 5px; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Reconnaissance Report</h1>
        <div class="info">
            <strong>Target:</strong> {self.target}<br>
            <strong>Scan Date:</strong> {self.results['timestamp']}<br>
        </div>
        
        <h2>DNS Records</h2>
        <table>
            <tr><th>Record Type</th><th>Values</th></tr>
"""
        
        for record_type, records in self.results['dns_records'].items():
            html += f"<tr><td>{record_type}</td><td>{', '.join(records)}</td></tr>\n"
        
        html += """
        </table>
        
        <h2>Subdomains</h2>
        <div class="info">
"""
        for subdomain in self.results['subdomains']:
            html += f"{subdomain}<br>\n"
        
        html += """
        </div>
        
        <h2>Open Ports</h2>
        <div>
"""
        for port in self.results['open_ports']:
            html += f'<span class="port">{port["port"]} ({port["service"]})</span>\n'
        
        html += """
        </div>
        
        <h2>Technologies</h2>
        <div class="info">
"""
        for tech in self.results['technologies']:
            html += f"{tech}<br>\n"
        
        html += """
        </div>
    </div>
</body>
</html>
"""
        return html

    def run(self, enable_dns=True, enable_subdomains=True, enable_ports=True, 
            enable_banners=True, enable_http=True, enable_tech=True, 
            enable_whois=True, report_format='text'):
        """
        Run the complete reconnaissance
        
        Args:
            enable_dns (bool): Enable DNS enumeration
            enable_subdomains (bool): Enable subdomain enumeration
            enable_ports (bool): Enable port scanning
            enable_banners (bool): Enable banner grabbing
            enable_http (bool): Enable HTTP header retrieval
            enable_tech (bool): Enable technology detection
            enable_whois (bool): Enable WHOIS lookup
            report_format (str): Report format (text, json, html)
        """
        self.print_banner()
        
        try:
            if enable_dns:
                self.dns_lookup()
            
            if enable_subdomains:
                self.subdomain_enumeration()
            
            if enable_ports:
                self.port_scan()
            
            if enable_banners and self.results['open_ports']:
                self.banner_grabbing()
            
            if enable_http:
                self.http_headers()
            
            if enable_tech:
                self.technology_detection()
            
            if enable_whois:
                self.whois_lookup()
            
            self.generate_report(report_format)
            
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}[✓] Reconnaissance Complete!{Colors.ENDC}")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}[!] Scan interrupted by user{Colors.ENDC}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.FAIL}[!] Error: {str(e)}{Colors.ENDC}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Recon Automation Tool - Comprehensive reconnaissance for cybersecurity professionals',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 recon.py -u example.com
  python3 recon.py -u example.com -p 1-1000 -t 20
  python3 recon.py -u example.com --no-subdomains -f json
  python3 recon.py -u example.com -w custom_wordlist.txt
        """
    )
    
    parser.add_argument('-u', '--url', required=True, help='Target domain or IP address')
    parser.add_argument('-p', '--ports', help='Port range (e.g., 1-1000) or comma-separated ports (e.g., 80,443,8080)')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('-w', '--wordlist', help='Custom wordlist for subdomain enumeration')
    parser.add_argument('--timeout', type=int, default=3, help='Connection timeout in seconds (default: 3)')
    parser.add_argument('-f', '--format', choices=['text', 'json', 'html'], default='text', help='Report format')
    
    # Module toggles
    parser.add_argument('--no-dns', action='store_true', help='Disable DNS enumeration')
    parser.add_argument('--no-subdomains', action='store_true', help='Disable subdomain enumeration')
    parser.add_argument('--no-ports', action='store_true', help='Disable port scanning')
    parser.add_argument('--no-banners', action='store_true', help='Disable banner grabbing')
    parser.add_argument('--no-http', action='store_true', help='Disable HTTP header retrieval')
    parser.add_argument('--no-tech', action='store_true', help='Disable technology detection')
    parser.add_argument('--no-whois', action='store_true', help='Disable WHOIS lookup')
    
    args = parser.parse_args()
    
    # Parse ports
    ports = None
    if args.ports:
        if '-' in args.ports:
            start, end = map(int, args.ports.split('-'))
            ports = list(range(start, end + 1))
        else:
            ports = [int(p) for p in args.ports.split(',')]
    
    # Initialize and run
    recon = ReconTool(
        target=args.url,
        ports=ports,
        timeout=args.timeout,
        threads=args.threads,
        wordlist=args.wordlist
    )
    
    recon.run(
        enable_dns=not args.no_dns,
        enable_subdomains=not args.no_subdomains,
        enable_ports=not args.no_ports,
        enable_banners=not args.no_banners,
        enable_http=not args.no_http,
        enable_tech=not args.no_tech,
        enable_whois=not args.no_whois,
        report_format=args.format
    )


if __name__ == '__main__':
    main()
