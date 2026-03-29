import asyncio
import socket
import time
import argparse
from rich.console import Console
from rich.table import Table
from rich.progress import track

# Initialize Rich Console for beautiful terminal output
console = Console()

# Dictionary of common ports and their typical services
COMMON_PORTS = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
    80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS',
    3306: 'MySQL', 3389: 'RDP', 5900: 'VNC', 8080: 'HTTP-Alt'
}

async def grab_banner(ip, port, timeout=1.5):
    """Attempts to grab the service banner from an open port."""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), 
            timeout=timeout
        )
        # Send a dummy HTTP request in case it's a web server
        writer.write(b"GET / HTTP/1.1\r\nHost: target\r\n\r\n")
        await writer.drain()
        
        banner = await asyncio.wait_for(reader.read(1024), timeout=timeout)
        writer.close()
        await writer.wait_closed()
        
        return banner.decode('utf-8', errors='ignore').strip().split('\n')[0][:50]
    except Exception:
        return "No Banner Found"

async def scan_port(ip, port, timeout=1.0):
    """Scans a single port asynchronously."""
    try:
        # Attempt TCP connection
        future = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(future, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        
        # If connection succeeds, grab the banner
        banner = await grab_banner(ip, port)
        service = COMMON_PORTS.get(port, 'Unknown')
        
        return port, service, banner
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None

async def main(target, start_port, end_port):
    console.print(f"\n[bold blue][*] Starting AsyncNet-Scanner against {target}[/bold blue]")
    console.print(f"[*] Scanning ports {start_port} to {end_port}...\n")
    
    start_time = time.time()
    
    # Create scan tasks for all ports in range
    tasks = [scan_port(target, port) for port in range(start_port, end_port + 1)]
    
    # Execute tasks concurrently
    results = await asyncio.gather(*tasks)
    
    # Filter out closed ports
    open_ports = [res for res in results if res is not None]
    
    elapsed_time = time.time() - start_time
    
    # Display results in a beautiful table
    if open_ports:
        table = Table(show_header=True, header_style="bold green")
        table.add_column("PORT", style="dim", width=8)
        table.add_column("STATE", width=10)
        table.add_column("SERVICE", width=15)
        table.add_column("BANNER (Version Info)", width=40)
        
        for port, service, banner in sorted(open_ports):
            table.add_row(str(port), "[green]Open[/green]", service, banner)
            
        console.print(table)
    else:
        console.print("[bold red][-] No open ports found in the specified range.[/bold red]")
        
    console.print(f"\n[bold blue][*] Scan completed in {elapsed_time:.2f} seconds.[/bold blue]\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Asynchronous Network Port Scanner with Banner Grabbing")
    parser.add_argument("target", help="Target IP address or hostname (e.g., 127.0.0.1 or scanme.nmap.org)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    
    args = parser.parse_args()
    
    try:
        # Run the async event loop
        asyncio.run(main(args.target, args.start, args.end))
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Scan aborted by user.[/bold red]")