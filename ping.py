import socket
import time
import csv
from datetime import datetime
import os
from typing import Optional, Sequence

def tcp_ping(host: str, port: int = 443, timeout: float = 2.0) -> Optional[float]:
	"""
	Intenta abrir una conexión TCP para medir latencia.
	:param host: Host o IP de destino.
	:param port: Puerto TCP (443 por defecto).
	:param timeout: Timeout en segundos para la conexión.
	:return: Latencia en milisegundos si conecta; None si falla.
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
	Prueba uno o varios puertos TCP y registra el primer éxito (o un fallo).
	:param host: Host o IP de destino.
	:param ports: Lista de puertos a intentar en orden (primero que conecte gana).
	:param timeout: Timeout por intento (s).
	:param csv_file: Ruta del CSV para guardar resultados.
	:param fail_value_ms: Valor a registrar si todos los puertos fallan.
	:return: None
	"""
	timestamp = datetime.now().isoformat()
	latency_ms = None

	for p in ports:
		latency_ms = tcp_ping(host, p, timeout)
		if latency_ms is not None:
			print(f"TCP ping a {host}:{p} OK: {latency_ms} ms")
			break

	if latency_ms is None:
		latency_ms = fail_value_ms
		print(f"TCP ping a {host} falló (puertos probados: {list(ports)}).")

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
		time.sleep(0.5)
