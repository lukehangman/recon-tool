# 🔍 Recon Automation Tool

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/recon-tool)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

A comprehensive reconnaissance automation tool designed for cybersecurity professionals and penetration testers. This tool performs various information gathering techniques to help assess the security posture of target domains.

## ⚠️ Disclaimer

**IMPORTANT:** This tool is intended for educational purposes and authorized security testing only. Always ensure you have explicit permission before scanning any target. Unauthorized access to computer systems is illegal. The developers assume no liability for misuse of this tool.

## ✨ Features

- **DNS Enumeration**
  - A, AAAA, MX, NS, TXT, SOA, CNAME records
  - PTR (Reverse DNS) lookups
  - Comprehensive DNS record collection

- **Subdomain Discovery**
  - Wordlist-based subdomain enumeration
  - Multi-threaded scanning for speed
  - Customizable wordlist support

- **Port Scanning**
  - TCP port scanning with service detection
  - Configurable port ranges
  - Multi-threaded scanning engine

- **Banner Grabbing**
  - Service version detection
  - Banner collection from open ports
  - HTTP/HTTPS banner analysis

- **HTTP/HTTPS Analysis**
  - Header collection and analysis
  - Security header detection
  - SSL/TLS certificate information

- **Technology Detection**
  - Web server identification
  - Framework detection (WordPress, Joomla, Drupal, etc.)
  - JavaScript library identification
  - CMS fingerprinting

- **WHOIS Lookup**
  - Domain registration information
  - Registrar details
  - Name server information
  - Expiration dates

- **Report Generation**
  - Multiple output formats (Text, JSON, HTML)
  - Timestamped reports
  - Organized report storage

- **User Experience**
  - Colorized terminal output
  - Progress indicators
  - Modular design (enable/disable specific modules)
  - Comprehensive error handling

## 📋 Requirements

- Python 3.7 or higher
- Linux OS (Ubuntu, Debian, Kali Linux, Parrot OS)
- Internet connection
- Root/sudo access (recommended for some features)

### Python Dependencies

- dnspython
- requests
- python-whois
- urllib3

## 🚀 Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/recon-tool.git
cd recon-tool

# Run the setup script
chmod +x setup.sh
./setup.sh
```

### Manual Installation

```bash
# Install system dependencies (Ubuntu/Debian/Kali)
sudo apt-get update
sudo apt-get install -y python3 python3-pip whois dnsutils

# Install Python dependencies
pip3 install -r requirements.txt

# Make the script executable
chmod +x recon.py

# Create necessary directories
mkdir -p reports wordlists
```

### Verify Installation

```bash
python3 recon.py --help
```

## 📖 Usage

### Basic Usage

```bash
# Basic scan with default settings
python3 recon.py -u example.com

# Scan with custom port range
python3 recon.py -u example.com -p 1-1000

# Generate JSON report
python3 recon.py -u example.com -f json

# Generate HTML report
python3 recon.py -u example.com -f html
```

### Advanced Usage

```bash
# Custom wordlist for subdomain enumeration
python3 recon.py -u example.com -w /path/to/wordlist.txt

# Increase thread count for faster scanning
python3 recon.py -u example.com -t 50

# Scan specific ports
python3 recon.py -u example.com -p 80,443,8080,8443

# Disable specific modules
python3 recon.py -u example.com --no-subdomains --no-whois

# Adjust timeout for slow connections
python3 recon.py -u example.com --timeout 10
```

### Command-Line Options

```
Required Arguments:
  -u, --url URL              Target domain or IP address

Optional Arguments:
  -h, --help                 Show help message and exit
  -p, --ports PORTS          Port range (1-1000) or comma-separated (80,443)
  -t, --threads NUM          Number of threads (default: 10)
  -w, --wordlist FILE        Custom subdomain wordlist
  --timeout SECONDS          Connection timeout in seconds (default: 3)
  -f, --format FORMAT        Report format: text, json, html (default: text)

Module Toggles:
  --no-dns                   Disable DNS enumeration
  --no-subdomains            Disable subdomain enumeration
  --no-ports                 Disable port scanning
  --no-banners               Disable banner grabbing
  --no-http                  Disable HTTP header retrieval
  --no-tech                  Disable technology detection
  --no-whois                 Disable WHOIS lookup
```

## 📁 Project Structure

```
recon-tool/
├── recon.py                 # Main reconnaissance tool
├── setup.sh                 # Installation script
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
├── CONTRIBUTING.md          # Contribution guidelines
├── CHANGELOG.md             # Version history
├── examples/
│   └── EXAMPLE_OUTPUT.md    # Sample scan outputs
├── wordlists/
│   ├── subdomains.txt       # Default subdomain wordlist
│   └── README.md            # Wordlist documentation
└── reports/                 # Generated reports directory
    └── .gitkeep
```

## 📊 Output Examples

### Text Output (Console)

```
╦═╗╔═╗╔═╗╔═╗╔╗╔  ╔╦╗╔═╗╔═╗╦  
╠╦╝║╣ ║  ║ ║║║║   ║ ║ ║║ ║║  
╩╚═╚═╝╚═╝╚═╝╝╚╝   ╩ ╚═╝╚═╝╩═╝

Recon Automation Tool v1.0.0
Target: example.com
Started: 2024-01-15 10:30:45
==================================================

[*] Starting DNS Enumeration...
[+] A Records:
    93.184.216.34
[+] MX Records:
    0 mail.example.com
[+] NS Records:
    ns1.example.com
    ns2.example.com

[*] Starting Port Scan...
[*] Target IP: 93.184.216.34
[+] Port 80 (http) - OPEN
[+] Port 443 (https) - OPEN

[✓] Reconnaissance Complete!
[+] Text report saved: reports/recon_example.com_20240115_103045.txt
```

### Generated Reports

Reports are automatically saved in the `reports/` directory with timestamps:

- **Text Report**: Human-readable format
- **JSON Report**: Machine-parseable format for automation
- **HTML Report**: Visual report with formatted tables and styling

## 🛠️ Configuration

### Custom Wordlists

Create your own subdomain wordlist:

```bash
# Create a custom wordlist
cat > custom_subs.txt << EOF
www
mail
ftp
admin
api
dev
staging
EOF

# Use it with the tool
python3 recon.py -u example.com -w custom_subs.txt
```

### Performance Tuning

```bash
# For fast networks
python3 recon.py -u example.com -t 50 --timeout 2

# For slow/unstable networks
python3 recon.py -u example.com -t 5 --timeout 10
```

## 🔒 Security Considerations

1. **Legal Authorization**: Always obtain written permission before scanning
2. **Rate Limiting**: Be mindful of target server resources
3. **Stealth**: Consider using lower thread counts to avoid detection
4. **Logs**: Be aware that your scanning activity will be logged
5. **VPN/Proxy**: Consider using VPN for privacy (where legal)

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'dns'`
```bash
Solution: pip3 install -r requirements.txt --break-system-packages
```

**Issue**: Permission denied errors
```bash
Solution: Run with sudo or adjust file permissions
sudo python3 recon.py -u example.com
```

**Issue**: DNS resolution failures
```bash
Solution: Check network connectivity and DNS settings
ping example.com
nslookup example.com
```

**Issue**: Timeout errors on port scanning
```bash
Solution: Increase timeout value
python3 recon.py -u example.com --timeout 10
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/recon-tool.git
cd recon-tool

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python3 recon.py -u example.com

# Commit and push
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name
```

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Thanks to the open-source community
- Inspired by various reconnaissance tools (nmap, subfinder, dnsenum)
- Built for educational and authorized security testing purposes

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/recon-tool/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/recon-tool/discussions)
- **Email**: your.email@example.com

## 🔗 Related Projects

- [Nmap](https://nmap.org/) - Network exploration tool
- [Subfinder](https://github.com/projectdiscovery/subfinder) - Subdomain discovery
- [DNSEnum](https://github.com/fwaeytens/dnsenum) - DNS enumeration
- [theHarvester](https://github.com/laramies/theHarvester) - OSINT gathering

## ⭐ Star History

If you find this tool useful, please consider giving it a star on GitHub!

---

**Made with ❤️ for the cybersecurity community**

**Remember: With great power comes great responsibility. Use ethically!**
