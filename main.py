import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from pathlib import Path

"""
Some precisions:
		. Savitzky requires : window_length < len(TG) on small datasets, otherwise itcrashes
		. Window_length must be odd. Larger = smoother but less details
		. To smooth the prah, you can either increase window length, or use smooth_TG in dTG
"""

def choose_sheet(xls):
	print ("Please chose a sheet between : \n")
	for i, name in enumerate(xls.sheet_names):
		print(i, ":", name)
	try:
		choice = int(input("Type sheet name or index: "))
		return xls.sheet_names[choice]
	except (ValueError, IndexError):
		print("Invalid choice")
		return None

def show_graph(T, TG, smooth_TG, dTG, sheet_name):

	fig, (ax1, ax2) = plt.subplots(
		2, 1,
		sharex=True,
		figsize=(10, 8)
	)

	# --- TG graph ---
	ax1.plot(T, TG, color="blue", label="Raw TG")
	ax1.plot(T, smooth_TG, color="green", label="Smoothed TG")

	ax1.set_ylabel("Mass")
	ax1.set_title(sheet_name)
	ax1.legend()
	ax1.grid(True)

	# --- dTG graph ---
	ax2.plot(T, dTG, color="red", label="dTG")

	ax2.set_xlabel("Temperature")
	ax2.set_ylabel("Derivative")
	ax2.legend()
	ax2.grid(True)

	plt.tight_layout()
	plt.show()

def main():
	FILE = "GGBS_TGA.xlsx"
	if not Path(FILE).exists():
		print(f"Error: file '{FILE}' not found")
		return
	xls = pd.ExcelFile(FILE)

	sheet_name = None
	while sheet_name is None:
		sheet_name = choose_sheet(xls)

	df = pd.read_excel(FILE, sheet_name=sheet_name)
	T = df.iloc[:, 0].to_numpy()
	TG = df.iloc[:, 1].to_numpy()

	smooth_TG = savgol_filter(TG, window_length=11, polyorder=3)
	delta_T = T[1] - T[0] #Without this, the derivative is with respect to point index, not temperature
	dTG = savgol_filter(TG, window_length=41, polyorder=3, deriv=1, delta=delta_T)
	# dTG = savgol_filter(smooth_TG, window_length=51, polyorder=3, deriv=1, delta=delta_T) #You can use this dTG to smooth the graph even more (don't know how trustful it is so make some tests !!)
	show_graph(T, TG, smooth_TG, dTG, sheet_name)

if __name__ == "__main__":
	main()