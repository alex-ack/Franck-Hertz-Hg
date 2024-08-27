import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

def smooth_data_fourier(data, cutoff_frequency=0.1):
    sp = fft(data)
    frequencies = np.fft.fftfreq(len(sp))
    sp[np.abs(frequencies) > cutoff_frequency] = 0
    smoothed_data = np.real(ifft(sp))
    return smoothed_data

data = pd.read_csv('mercury.csv')
voltage = data['Voltage, Ch B (V) Run #2'].to_numpy()
current = -1 * data['Current, Ch A (A) Run #2'].to_numpy()
current_smooth = smooth_data_fourier(current[1258:], cutoff_frequency=1)
voltage_smooth = voltage[1258:]

peaks, _ = find_peaks(current_smooth, height=0.2e-11, distance=3, prominence=1e-12)
voltage_peaks = voltage_smooth[peaks]

delta_vs = [4.70, 4.90, 4.90, 4.80, 4.80]
peak_pairs = [(0,1), (1,2), (2,3), (3,5), (5,6)]

plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.5

fig, ax = plt.subplots(figsize=(8, 5), dpi=100)

y_smooth = gaussian_filter1d(current_smooth * 1e11, sigma=2)

main_color = '#1f77b4'
background_color = '#f5f5f5'
grid_color = '#e0e0e0'
annotation_color = '#2c3e50'

ax.plot(voltage_smooth, y_smooth, '-', label='Smoothed curve', 
        color=main_color, linewidth=2)
ax.scatter(voltage_peaks, current_smooth[peaks] * 1e11, color=main_color, s=40, zorder=5, label='Peaks')

ax.set_facecolor(background_color)
ax.grid(color=grid_color, linestyle='-', linewidth=1)

y_pos = max(y_smooth) * 1.10

for (start, end), delta_v in zip(peak_pairs, delta_vs):
    x_start = voltage_peaks[start]
    x_end = voltage_peaks[end]
    x_mid = (x_start + x_end) / 2
    
    ax.vlines(x=x_start, ymin=0, ymax=max(y_smooth), 
              color=main_color, linestyle='--', linewidth=1, alpha=0.5)
    ax.vlines(x=x_end, ymin=0, ymax=max(y_smooth), 
              color=main_color, linestyle='--', linewidth=1, alpha=0.5)
    
    ax.annotate('', xy=(x_start, y_pos), xytext=(x_end, y_pos),
                arrowprops=dict(arrowstyle='<->', color=annotation_color, linewidth=1))
    ax.annotate(f'ΔV = {delta_v:.2f}V', xy=(x_mid, y_pos), fontsize=8, ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=annotation_color, alpha=0.7),
                color=annotation_color)

ax.set_title("Current vs Accelerating Voltage of Mercury (Hg)", fontsize=14, fontweight='bold', pad=10, color=annotation_color)
ax.set_xlabel("Accelerating Voltage $V_{G2K}$ (V)", fontsize=12, labelpad=8, color=annotation_color)
ax.set_ylabel("Current $I_A$ ($\\times 10^{-11}$ A)", fontsize=12, labelpad=8, color=annotation_color)

ax.legend(loc='upper left', fontsize=10, frameon=True, facecolor='white', edgecolor=annotation_color)

ax.set_xlim(min(voltage_smooth), max(voltage_smooth))
ax.set_ylim(0, max(y_smooth) * 1.15)

for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color(annotation_color)
    spine.set_linewidth(1)

plt.tight_layout()
plt.savefig('compact_voltage_current_plot.png', dpi=100, bbox_inches='tight')
plt.show()