import pandas as pd
import matplotlib.pyplot as plt

def plot_ping_times(csv_file: str = "dat/ping_results.csv") -> None:
	"""
	Reads a CSV file with ping results and generates a time series plot.

	:param csv_file: Path to the CSV file with the following columns: timestamp, ip, ping_ms.
	:return: None
	"""
	try:
		# Read the CSV
		df = pd.read_csv(csv_file, parse_dates=["timestamp"])

		# Remove failed pings (null values)
		df = df.dropna(subset=["ping_ms"])

		# Sort by timestamp
		df = df.sort_values("timestamp")

		# Plot
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
		print(f"The file {csv_file} was not found. Make sure to run the ping script first.")
	except Exception as e:
		print(f"Error while generating the plot: {e}")

	return None


# Example usage
if __name__ == "__main__":
	plot_ping_times()
