import subprocess
import time
import csv
from datetime import datetime
import os

def ping_ip(ip_address: str, csv_file: str = "Ping/ping_results.csv") -> None:
	"""
	Realiza un ping a una IP, mide el tiempo en milisegundos y guarda el resultado con timestamp en un CSV.

	:param ip_address: Dirección IP o dominio a hacer ping.
	:param csv_file: Nombre del archivo CSV donde guardar los resultados.
	:return: None
	"""
	start_time = time.time()

	try:
		# Ejecuta el ping (1 solo paquete)
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
			print(f"Ping a {ip_address} exitoso: {duration_ms} ms")
		else:
			print(f"Fallo el ping a {ip_address}. Error: {result.stderr}")
			duration_ms = 1000

	except Exception as e:
		print(f"Error al ejecutar el ping: {e}")
		timestamp = datetime.now().isoformat()
		duration_ms = 1000

	# Guardar en el archivo CSV
	file_exists = os.path.isfile(csv_file)
	with open(csv_file, mode="a", newline="") as file:
		writer = csv.writer(file)
		if not file_exists:
			writer.writerow(["timestamp", "ip", "ping_ms"])
		writer.writerow([timestamp, ip_address, duration_ms])

	return None


# Ejemplo de uso
if __name__ == "__main__":
	while True:
		ping_ip("google.com")
		time.sleep(1)
