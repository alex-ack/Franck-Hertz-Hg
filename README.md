# Mercury Data Analysis and Visualization

This script processes and visualizes experimental data related to the current vs. accelerating voltage of Mercury (Hg). The key functionalities include:

- **Fourier Smoothing:** The current data is smoothed using a Fourier Transform method with a customizable cutoff frequency.

- **Peak Detection:** Identifies peaks in the smoothed current data to analyze significant voltage points.

- **Data Visualization:** Generates a detailed plot of the smoothed current vs. voltage, highlighting peak points and annotated voltage differences (ΔV) between specific peaks.

The final plot is saved as an image file (`compact_voltage_current_plot.png`).
