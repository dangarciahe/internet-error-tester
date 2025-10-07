import subprocess
import time
import csv
from datetime import datetime
import os

def ping_ip(ip_address: str, csv_file: str = "dat/ping_results.csv") -> None:
	"""
	Pings an IP address, measures the response time in milliseconds,
	and saves the result with a timestamp to a CSV file.

	:param ip_address: IP address or domain to ping.
	:param csv_file: Name of the CSV file to save the results.
	:return: None
	"""
	start_time = time.time()

	try:
		# Execute the ping (send only 1 packet)
		result = subprocess.run(
			["ping", "-c", "1", "-W", "2", ip_address],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True
		)

		end_time = time.time()
		timestamp = datetime.now().isoformat()
		duration_ms = round((end_time - start_time) * 1000, 2)

		if result.returncode == 0:
			print(f"Ping to {ip_address} successful: {duration_ms} ms")
		else:
			print(f"Ping to {ip_address} failed. Error: {result.stderr}")
			duration_ms = 1000

	except Exception as e:
		print(f"Error executing ping: {e}")
		timestamp = datetime.now().isoformat()
		duration_ms = 1000

	# Save to CSV file
	file_exists = os.path.isfile(csv_file)
	with open(csv_file, mode="a", newline="") as file:
		writer = csv.writer(file)
		if not file_exists:
			writer.writerow(["timestamp", "ip", "ping_ms"])
		writer.writerow([timestamp, ip_address, duration_ms])

	return None


# Example usage
if __name__ == "__main__":
	os.makedirs("dat", exist_ok=True)
	while True:
		ping_ip("google.com")
		time.sleep(0.5)
