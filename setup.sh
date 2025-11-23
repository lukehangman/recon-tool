#!/bin/bash

# Recon Automation Tool - Installation Script
# Version 1.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╦═╗╔═╗╔═╗╔═╗╔╗╔  ╔╦╗╔═╗╔═╗╦  "
echo "╠╦╝║╣ ║  ║ ║║║║   ║ ║ ║║ ║║  "
echo "╩╚═╚═╝╚═╝╚═╝╝╚╝   ╩ ╚═╝╚═╝╩═╝"
echo -e "${NC}"
echo -e "${GREEN}Recon Automation Tool - Setup Script v1.0.0${NC}"
echo "=================================================="
echo ""

# Check if running as root for system-wide installation
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}[!] Running as root. Will install system-wide.${NC}"
    SUDO=""
else
    echo -e "${YELLOW}[!] Running as user. May need sudo for some operations.${NC}"
    SUDO="sudo"
fi

# Detect OS
echo -e "${BLUE}[*] Detecting operating system...${NC}"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
    echo -e "${GREEN}[+] Detected: $OS $VER${NC}"
else
    echo -e "${RED}[!] Cannot detect OS. Assuming Debian/Ubuntu-based system.${NC}"
    OS="Linux"
fi

# Check Python version
echo ""
echo -e "${BLUE}[*] Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}[+] Python 3 is installed: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}[!] Python 3 is not installed!${NC}"
    echo -e "${YELLOW}[*] Installing Python 3...${NC}"
    
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Kali"* ]]; then
        $SUDO apt-get update
        $SUDO apt-get install -y python3 python3-pip python3-dev
    elif [[ "$OS" == *"Fedora"* ]] || [[ "$OS" == *"Red Hat"* ]] || [[ "$OS" == *"CentOS"* ]]; then
        $SUDO dnf install -y python3 python3-pip python3-devel
    elif [[ "$OS" == *"Arch"* ]]; then
        $SUDO pacman -S --noconfirm python python-pip
    else
        echo -e "${RED}[!] Please install Python 3 manually${NC}"
        exit 1
    fi
fi

# Check pip
echo ""
echo -e "${BLUE}[*] Checking pip installation...${NC}"
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    echo -e "${GREEN}[+] pip3 is installed: $PIP_VERSION${NC}"
else
    echo -e "${YELLOW}[*] Installing pip3...${NC}"
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Kali"* ]]; then
        $SUDO apt-get install -y python3-pip
    else
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    fi
fi

# Install system dependencies
echo ""
echo -e "${BLUE}[*] Installing system dependencies...${NC}"

if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Kali"* ]]; then
    $SUDO apt-get update
    $SUDO apt-get install -y \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        whois \
        dnsutils \
        nmap \
        git
elif [[ "$OS" == *"Fedora"* ]] || [[ "$OS" == *"Red Hat"* ]] || [[ "$OS" == *"CentOS"* ]]; then
    $SUDO dnf install -y \
        gcc \
        openssl-devel \
        libffi-devel \
        python3-devel \
        whois \
        bind-utils \
        nmap \
        git
elif [[ "$OS" == *"Arch"* ]]; then
    $SUDO pacman -S --noconfirm \
        base-devel \
        openssl \
        libffi \
        whois \
        dnsutils \
        nmap \
        git
fi

# Upgrade pip
echo ""
echo -e "${BLUE}[*] Upgrading pip...${NC}"
pip3 install --upgrade pip

# Install Python dependencies
echo ""
echo -e "${BLUE}[*] Installing Python dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
    echo -e "${GREEN}[+] Python dependencies installed successfully${NC}"
else
    echo -e "${RED}[!] requirements.txt not found!${NC}"
    exit 1
fi

# Create necessary directories
echo ""
echo -e "${BLUE}[*] Creating project directories...${NC}"
mkdir -p reports
mkdir -p wordlists
echo -e "${GREEN}[+] Directories created${NC}"

# Check if wordlist exists
if [ ! -f "wordlists/subdomains.txt" ]; then
    echo -e "${YELLOW}[!] Subdomain wordlist not found${NC}"
    echo -e "${BLUE}[*] Creating sample wordlist...${NC}"
    # The wordlist will be created separately
fi

# Make recon.py executable
echo ""
echo -e "${BLUE}[*] Setting executable permissions...${NC}"
chmod +x recon.py
echo -e "${GREEN}[+] Permissions set${NC}"

# Test installation
echo ""
echo -e "${BLUE}[*] Testing installation...${NC}"
if python3 -c "import dns.resolver, requests, whois" 2>/dev/null; then
    echo -e "${GREEN}[+] All dependencies are working correctly${NC}"
else
    echo -e "${RED}[!] Some dependencies failed to import${NC}"
    echo -e "${YELLOW}[*] Try running: pip3 install -r requirements.txt${NC}"
    exit 1
fi

# Create symbolic link (optional)
echo ""
read -p "$(echo -e ${YELLOW}"Do you want to install recon.py system-wide? (y/n): "${NC})" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    $SUDO cp recon.py /usr/local/bin/recon
    $SUDO chmod +x /usr/local/bin/recon
    echo -e "${GREEN}[+] Installed to /usr/local/bin/recon${NC}"
    echo -e "${GREEN}[+] You can now run: recon -u example.com${NC}"
fi

# Print completion message
echo ""
echo -e "${GREEN}=================================================="
echo -e "✓ Installation Complete!"
echo -e "==================================================${NC}"
echo ""
echo -e "${BLUE}Usage Examples:${NC}"
echo "  python3 recon.py -u example.com"
echo "  python3 recon.py -u example.com -p 1-1000"
echo "  python3 recon.py -u example.com -f json"
echo ""
echo -e "${BLUE}For more information:${NC}"
echo "  python3 recon.py --help"
echo "  cat README.md"
echo ""
echo -e "${YELLOW}[!] Disclaimer: Use this tool responsibly and only on systems you have permission to test.${NC}"
echo ""
