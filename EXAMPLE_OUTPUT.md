# Example Output - Recon Automation Tool

This document showcases example outputs from the Recon Automation Tool to help you understand what to expect when running scans.

## 📋 Table of Contents

1. [Console Output](#console-output)
2. [Text Report](#text-report)
3. [JSON Report](#json-report)
4. [HTML Report](#html-report)

---

## Console Output

### Basic Scan Example

```
╦═╗╔═╗╔═╗╔═╗╔╗╔  ╔╦╗╔═╗╔═╗╦  
╠╦╝║╣ ║  ║ ║║║║   ║ ║ ║║ ║║  
╩╚═╚═╝╚═╝╚═╝╝╚╝   ╩ ╚═╝╚═╝╩═╝

Recon Automation Tool v1.0.0
Target: example.com
Started: 2024-01-15 14:30:45
==================================================

[*] Starting DNS Enumeration...
[+] A Records:
    93.184.216.34
[+] AAAA Records:
    2606:2800:220:1:248:1893:25c8:1946
[+] MX Records:
    0 mail.example.com
[+] NS Records:
    a.iana-servers.net
    b.iana-servers.net
[+] TXT Records:
    v=spf1 -all
    wgyf8z8cgvm2qmxpnbnldrcltvk4xqfn
[+] SOA Records:
    sns.dns.icann.org. noc.dns.icann.org. 2023011500 7200 3600 1209600 3600
[-] No CNAME records found
[+] PTR Records:
    example.com

[*] Starting Subdomain Enumeration...
[*] Testing 150 subdomains...
[+] Found: www.example.com
[+] Found: mail.example.com
[+] Found: ftp.example.com
[+] Found: api.example.com
[+] Found: dev.example.com

[+] Total subdomains found: 5

[*] Starting Port Scan...
[*] Target IP: 93.184.216.34
[+] Port 80 (http) - OPEN
[+] Port 443 (https) - OPEN

[+] Total open ports: 2

[*] Starting Banner Grabbing...
[+] Port 80 Banner:
    HTTP/1.1 200 OK
    Accept-Ranges: bytes
    Age: 409577
    Cache-Control: max-age=604800
    Content-Type: text/html; charset=UTF-8...
[+] Port 443 Banner:
    HTTP/1.1 200 OK
    Content-Type: text/html; charset=UTF-8
    Server: nginx/1.18.0...

[*] Retrieving HTTP Headers...
[+] HTTP Headers:
    Content-Encoding: gzip
    Accept-Ranges: bytes
    Age: 409577
    Cache-Control: max-age=604800
    Content-Type: text/html; charset=UTF-8
    Date: Mon, 15 Jan 2024 13:30:47 GMT
    Etag: "3147526947"
    Expires: Mon, 22 Jan 2024 13:30:47 GMT
    Last-Modified: Thu, 17 Oct 2023 07:18:26 GMT
    Server: ECS (dcb/7F82)
    X-Cache: HIT
    Content-Length: 1256
[!] Missing security headers: Strict-Transport-Security, X-Frame-Options, Content-Security-Policy
[+] HTTPS Headers:
    Content-Type: text/html; charset=UTF-8
    Server: nginx/1.18.0
    Date: Mon, 15 Jan 2024 13:30:48 GMT
    Strict-Transport-Security: max-age=31536000
    X-Frame-Options: SAMEORIGIN
    X-Content-Type-Options: nosniff
    Content-Security-Policy: default-src 'self'

[*] Detecting Technologies...
[+] Detected Technologies:
    Web Server: ECS (dcb/7F82)
    PHP
    jQuery
    Bootstrap
    WordPress

[*] Performing WHOIS Lookup...
[+] WHOIS Information:
    registrar: RESERVED-Internet Assigned Numbers Authority
    creation_date: 1995-08-14 04:00:00
    expiration_date: 2024-08-13 04:00:00
    name_servers: ['A.IANA-SERVERS.NET', 'B.IANA-SERVERS.NET']
    status: ['clientDeleteProhibited', 'clientTransferProhibited', 'clientUpdateProhibited']
    emails: None
    country: US

[*] Generating Report...
[+] Text report saved: reports/recon_example.com_20240115_143052.txt

[✓] Reconnaissance Complete!
```

---

## Text Report

### Sample Text Report Output

```
Reconnaissance Report
Target: example.com
Timestamp: 2024-01-15T14:30:52.123456
============================================================

DNS RECORDS
------------------------------------------------------------
A: 93.184.216.34
AAAA: 2606:2800:220:1:248:1893:25c8:1946
MX: 0 mail.example.com
NS: a.iana-servers.net, b.iana-servers.net
TXT: v=spf1 -all, wgyf8z8cgvm2qmxpnbnldrcltvk4xqfn
SOA: sns.dns.icann.org. noc.dns.icann.org. 2023011500 7200 3600 1209600 3600
PTR: example.com

SUBDOMAINS
------------------------------------------------------------
www.example.com
mail.example.com
ftp.example.com
api.example.com
dev.example.com

OPEN PORTS
------------------------------------------------------------
Port 80 (http)
Port 443 (https)

TECHNOLOGIES
------------------------------------------------------------
Web Server: ECS (dcb/7F82)
PHP
jQuery
Bootstrap
WordPress
```

---

## JSON Report

### Sample JSON Report Output

```json
{
    "target": "example.com",
    "timestamp": "2024-01-15T14:30:52.123456",
    "dns_records": {
        "A": [
            "93.184.216.34"
        ],
        "AAAA": [
            "2606:2800:220:1:248:1893:25c8:1946"
        ],
        "MX": [
            "0 mail.example.com"
        ],
        "NS": [
            "a.iana-servers.net",
            "b.iana-servers.net"
        ],
        "TXT": [
            "v=spf1 -all",
            "wgyf8z8cgvm2qmxpnbnldrcltvk4xqfn"
        ],
        "SOA": [
            "sns.dns.icann.org. noc.dns.icann.org. 2023011500 7200 3600 1209600 3600"
        ],
        "PTR": [
            "example.com"
        ]
    },
    "subdomains": [
        "www.example.com",
        "mail.example.com",
        "ftp.example.com",
        "api.example.com",
        "dev.example.com"
    ],
    "open_ports": [
        {
            "port": 80,
            "service": "http"
        },
        {
            "port": 443,
            "service": "https"
        }
    ],
    "http_headers": {
        "http": {
            "Content-Encoding": "gzip",
            "Accept-Ranges": "bytes",
            "Age": "409577",
            "Cache-Control": "max-age=604800",
            "Content-Type": "text/html; charset=UTF-8",
            "Date": "Mon, 15 Jan 2024 13:30:47 GMT",
            "Etag": "\"3147526947\"",
            "Expires": "Mon, 22 Jan 2024 13:30:47 GMT",
            "Last-Modified": "Thu, 17 Oct 2023 07:18:26 GMT",
            "Server": "ECS (dcb/7F82)",
            "X-Cache": "HIT",
            "Content-Length": "1256"
        },
        "https": {
            "Content-Type": "text/html; charset=UTF-8",
            "Server": "nginx/1.18.0",
            "Date": "Mon, 15 Jan 2024 13:30:48 GMT",
            "Strict-Transport-Security": "max-age=31536000",
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'self'"
        }
    },
    "technologies": [
        "Web Server: ECS (dcb/7F82)",
        "PHP",
        "jQuery",
        "Bootstrap",
        "WordPress"
    ],
    "whois_info": {
        "registrar": "RESERVED-Internet Assigned Numbers Authority",
        "creation_date": "1995-08-14 04:00:00",
        "expiration_date": "2024-08-13 04:00:00",
        "name_servers": [
            "A.IANA-SERVERS.NET",
            "B.IANA-SERVERS.NET"
        ],
        "status": [
            "clientDeleteProhibited",
            "clientTransferProhibited",
            "clientUpdateProhibited"
        ],
        "emails": null,
        "country": "US"
    },
    "banners": {
        "80": "HTTP/1.1 200 OK\r\nAccept-Ranges: bytes\r\nAge: 409577\r\nCache-Control: max-age=604800\r\nContent-Type: text/html; charset=UTF-8...",
        "443": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nServer: nginx/1.18.0..."
    }
}
```

---

## HTML Report

### Sample HTML Report Structure

The HTML report includes:

**Header Section:**
- Tool branding
- Target domain
- Scan timestamp
- Summary statistics

**DNS Records Table:**
```
┌─────────────┬───────────────────────────────────────┐
│ Record Type │ Values                                │
├─────────────┼───────────────────────────────────────┤
│ A           │ 93.184.216.34                         │
│ AAAA        │ 2606:2800:220:1:248:1893:25c8:1946    │
│ MX          │ 0 mail.example.com                    │
│ NS          │ a.iana-servers.net, b.iana-servers... │
└─────────────┴───────────────────────────────────────┘
```

**Subdomains Section:**
- List of discovered subdomains
- Color-coded by status
- Clickable links (in HTML)

**Open Ports Display:**
```
[80 (http)]  [443 (https)]
```
- Green badges for each open port
- Service names included
- Port numbers clearly visible

**Technologies Section:**
- Detected web servers
- Identified frameworks
- CMS platforms
- JavaScript libraries

**Visual Features:**
- Clean, modern design
- Color-coded sections
- Responsive layout
- Professional styling
- Print-friendly format

---

## Command Examples and Their Outputs

### Example 1: Quick Scan (Default Ports)

**Command:**
```bash
python3 recon.py -u example.com
```

**Expected Output:**
- DNS records (all types)
- 5-15 subdomains (depending on target)
- 0-5 open ports from default list
- HTTP headers if ports 80/443 are open
- 2-5 detected technologies
- WHOIS information

**Time:** ~30-60 seconds

---

### Example 2: Fast Scan (No Subdomains)

**Command:**
```bash
python3 recon.py -u example.com --no-subdomains
```

**Expected Output:**
- DNS records only
- Port scan results
- Quick completion

**Time:** ~10-20 seconds

---

### Example 3: Deep Port Scan

**Command:**
```bash
python3 recon.py -u example.com -p 1-1000 -t 50
```

**Expected Output:**
- DNS records
- Comprehensive port scan (1000 ports)
- More open ports discovered
- Longer banners
- Full technology stack

**Time:** ~2-3 minutes

---

### Example 4: JSON Output for Automation

**Command:**
```bash
python3 recon.py -u example.com -f json
```

**Expected Output:**
- All reconnaissance data in JSON format
- Machine-parseable structure
- Easy to integrate with other tools

**File:** `reports/recon_example.com_YYYYMMDD_HHMMSS.json`

---

### Example 5: Targeted Scan

**Command:**
```bash
python3 recon.py -u example.com -p 80,443,8080,8443 --no-whois
```

**Expected Output:**
- DNS records
- Specific port scan only
- HTTP/HTTPS analysis
- No WHOIS data (faster completion)

**Time:** ~15-25 seconds

---

## Report Locations

All reports are saved in the `reports/` directory with the following naming convention:

```
reports/recon_<target>_<timestamp>.<format>

Examples:
reports/recon_example.com_20240115_143052.txt
reports/recon_example.com_20240115_143052.json
reports/recon_example.com_20240115_143052.html
```

---

## Reading the Output

### Color Codes (Console)

- **🟢 Green `[+]`**: Successful operation or discovery
- **🟡 Yellow `[-]`**: Warning or no results found
- **🔴 Red `[!]`**: Error or critical issue
- **🔵 Blue `[*]`**: Informational message
- **🔷 Cyan**: Headers and sections

### Status Indicators

- `[*]` - Starting operation
- `[+]` - Success / Item found
- `[-]` - Not found / Skipped
- `[!]` - Error / Warning
- `[✓]` - Completion

---

## Performance Metrics

Typical scan times (example.com):

| Scan Type              | Time    | Data Points |
|------------------------|---------|-------------|
| DNS only               | 2-5s    | 10-20       |
| Default scan           | 30-60s  | 50-100      |
| With subdomains        | 1-2m    | 100-200     |
| Deep port scan (1-1000)| 2-5m    | 200-500     |
| Full comprehensive     | 3-7m    | 500+        |

*Times vary based on network speed, target responsiveness, and thread count.*

---

## Troubleshooting Output Issues

**Problem:** No output displayed
**Solution:** Check target connectivity, verify DNS resolution

**Problem:** Empty report files
**Solution:** Ensure `reports/` directory exists and is writable

**Problem:** Partial data in reports
**Solution:** Target may be blocking scans, try reducing thread count

**Problem:** Timeout errors
**Solution:** Increase timeout with `--timeout 10`

---

## Next Steps

After reviewing your scan results:

1. **Analyze DNS records** for misconfigurations
2. **Check subdomains** for forgotten or exposed services
3. **Review open ports** for unnecessary services
4. **Examine HTTP headers** for missing security headers
5. **Verify technologies** are up-to-date
6. **Check WHOIS data** for accuracy

**Remember:** Always use this tool ethically and with proper authorization!

---

*For more information, see the main [README.md](../README.md)*
