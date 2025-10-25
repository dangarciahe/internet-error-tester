import socket
import time
import csv
from datetime import datetime
import os
from typing import Optional, Sequence

from colorama import Fore, Style, init

## Colorama config
init(autoreset=True) 
RED_COLOR_THRESHOLD_MS = 150.0  # Latency threshold for red-colored output


def tcp_ping(
		host: str,
		port: int = 443,
		timeout: float = 2.0
	) -> Optional[float]:
	"""
	Attempts to open a TCP connection to measure latency.
	:param host: Target host or IP address.
	:param port: TCP port (default is 443).
	:param timeout: Connection timeout in seconds.
	:return: Latency in milliseconds if successful; None if it fails.
	"""
	start = time.perf_counter()
	
	try:
		with socket.create_connection((host, port), timeout=timeout):
			pass
		lat_ms = (time.perf_counter() - start) * 1000.0
		return round(lat_ms, 2)
	
	except Exception:
		return None


def ping_host(
	host: str,
	ports: Sequence[int] = (443, 80),
	timeout: float = 2.0,
	csv_file: str = "dat/ping_results.csv",
	fail_value_ms: float = 1000.0
) -> None:
	"""
	Tests one or more TCP ports and logs the first success (or failure).
	:param host: Target host or IP address.
	:param ports: List of ports to try in order (first successful one wins).
	:param timeout: Timeout per attempt (seconds).
	:param csv_file: Path to the CSV file for storing results.
	:param fail_value_ms: Value to record if all ports fail.
	:return: None
	"""
	timestamp = datetime.now().isoformat()
	latency_ms = None

	for p in ports:
		latency_ms = tcp_ping(host, p, timeout)
		if latency_ms is not None:
			if latency_ms > RED_COLOR_THRESHOLD_MS:
				print(f"{Fore.YELLOW}High ping to {host}:{p}: {latency_ms} ms")
			else:
				print(f"{Fore.GREEN}Ping OK to {host}:{p}: {latency_ms} ms")
				break

	if latency_ms is None:
		latency_ms = fail_value_ms
		print(f"{Fore.RED}Failed ping to {host}")

	file_exists = os.path.isfile(csv_file)
	os.makedirs(os.path.dirname(csv_file), exist_ok=True) if os.path.dirname(csv_file) else None
	with open(csv_file, mode="a", newline="") as f:
		writer = csv.writer(f)
		if not file_exists:
			writer.writerow(["timestamp", "host", "latency_ms", "ports_tested"])
		writer.writerow([timestamp, host, latency_ms, "|".join(map(str, ports))])

	return None


if __name__ == "__main__":
	os.makedirs("dat", exist_ok=True)
	
	while True:
		ping_host("google.com", ports=(443, 80), timeout=2.0, csv_file="dat/ping_results.csv")
		time.sleep(1)
