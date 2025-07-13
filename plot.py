import pandas as pd
import matplotlib.pyplot as plt

def plot_ping_times(csv_file: str = "ping_results.csv") -> None:
  """
  Lee un archivo CSV con resultados de ping y genera una gráfica de serie temporal.

  :param csv_file: Ruta al archivo CSV con columnas: timestamp, ip, ping_ms.
  :return: None
  """
  try:
    # Leer el CSV
    df = pd.read_csv(csv_file, parse_dates=["timestamp"])

    # Eliminar pings fallidos (valores nulos)
    df = df.dropna(subset=["ping_ms"])

    # Ordenar por timestamp
    df = df.sort_values("timestamp")

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.plot(df["timestamp"], df["ping_ms"], marker="o", linestyle="-")
    plt.title("Ping Time Series")
    plt.xlabel("Timestamp")
    plt.ylabel("Ping Time (ms)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

  except FileNotFoundError:
    print(f"No se encontró el archivo {csv_file}. Asegúrate de correr primero el script de ping.")
  except Exception as e:
    print(f"Error al generar la gráfica: {e}")

  return None


# Ejemplo de uso
if __name__ == "__main__":
  plot_ping_times()
