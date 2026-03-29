# Network-Port-Scanner-KD

An asynchronous network port scanner written in Python that efficiently scans ports on a target host and attempts to grab service banners for open ports. This tool uses asyncio for concurrent scanning and Rich for beautiful terminal output.

## Features

- **Asynchronous Scanning**: Utilizes asyncio for fast, concurrent port scanning.
- **Banner Grabbing**: Attempts to retrieve service banners from open ports to identify running services.
- **Rich Console Output**: Displays results in a formatted table with colors and styles.
- **Customizable Port Range**: Specify start and end ports for scanning.
- **Common Ports Dictionary**: Recognizes common services on standard ports.
- **Progress Tracking**: Shows scanning progress (via Rich's progress bars).
- **Keyboard Interrupt Handling**: Gracefully handles user interruption.

## Requirements

- Python 3.7+
- `rich` library (for console formatting)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Network-Port-Scanner-KD.git
   cd Network-Port-Scanner-KD
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the scanner with the target IP address or hostname:

```bash
python async_scanner.py <target> [options]
```

### Arguments

- `target`: Target IP address or hostname (required)
- `-s, --start`: Start port (default: 1)
- `-e, --end`: End port (default: 1024)

### Examples

Scan ports 1-1024 on localhost:
```bash
python async_scanner.py 127.0.0.1
```

Scan ports 20-100 on a specific host:
```bash
python async_scanner.py scanme.nmap.org -s 20 -e 100
```

Scan common ports (1-1024) on a remote host:
```bash
python async_scanner.py example.com
```

## Output

The tool displays:
- Open ports with their state, service name, and banner information.
- Scan completion time.
- A message if no open ports are found.

Example output:
```
[*] Starting AsyncNet-Scanner against 127.0.0.1
[*] Scanning ports 1 to 1024...

┏━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ PORT  ┃ STATE    ┃ SERVICE       ┃ BANNER (Version Info)            ┃
┡━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 22    │ Open     │ SSH           │ SSH-2.0-OpenSSH_8.2p1 Ubuntu-4   │
│ 80    │ Open     │ HTTP          │ HTTP/1.1 200 OK                  │
│ 443   │ Open     │ HTTPS         │ HTTP/1.1 200 OK                  │
└───────┴──────────┴───────────────┴──────────────────────────────────┘

[*] Scan completed in 2.34 seconds.
```

## Disclaimer

🛡️ Disclaimer  
Educational Purposes Only. This tool was created for educational purposes as part of a cybersecurity internship. You should only scan networks, servers, and devices that you explicitly own or have documented permission to test. Unauthorized port scanning can be considered illegal depending on your jurisdiction.

## Author

👨‍💻 Author  
Krishna Dubey  

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
