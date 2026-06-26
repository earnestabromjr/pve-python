import ipaddress
import os
import subprocess
import sys
from typing import Optional


def _import_nmap():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    saved = sys.path[:]
    sys.path = [p for p in sys.path if os.path.abspath(p) != this_dir]
    if "nmap" in sys.modules:
        del sys.modules["nmap"]
    try:
        import my_nmap as _nmap

        return _nmap
    finally:
        sys.path[:] = saved


def scan_network(
    network: str = "192.168.1.0/24",
    *,
    timeout: int = 1,
    ports: Optional[str] = None,
    arguments: str = "-sn",
) -> list[str]:
    try:
        nmap = _import_nmap()
        nm = nmap.PortScanner()
        args = arguments
        if ports:
            args = f"-sT -p {ports}"
        nm.scan(hosts=network, arguments=args)
        return nm.all_hosts()
    except (ImportError, OSError):
        return _ping_sweep(network, timeout)


def _ping_sweep(network: str, timeout: int) -> list[str]:
    online: list[str] = []
    for ip in ipaddress.IPv4Network(network, strict=False).hosts():
        ip_str = str(ip)
        result = subprocess.run(
            ["ping", "-c1", f"-W{timeout}", ip_str],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            online.append(ip_str)
    return online


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Scan a network for live hosts and return their IPs."
    )
    parser.add_argument(
        "network",
        nargs="?",
        default="192.168.1.0/24",
        help="CIDR network range (e.g. 192.168.1.0/24)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1,
        help="Ping timeout in seconds (fallback only, default: 1)",
    )
    parser.add_argument(
        "-p",
        "--ports",
        help="TCP ports to scan (e.g. '22,80,443')",
    )
    args = parser.parse_args()

    hosts = scan_network(args.network, timeout=args.timeout, ports=args.ports)
    for ip in hosts:
        print(ip)
