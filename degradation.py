import fastf1
import matplotlib.pyplot as plt
import numpy as np

# Connect to the cache
fastf1.Cache.enable_cache('./cache')

print("Downloading Bahrain Race Data... (This takes a moment!)")
# Notice we are loading 'R' for Race now, not 'Q' for Qualifying
session = fastf1.get_session(2024, 'Bahrain', 'R')
session.load()

# 1. Get Max Verstappen's race laps
# We use pick_quicklaps() to automatically delete safety cars, pit stops, and out-laps
laps = session.laps.pick_drivers('VER').pick_quicklaps()

# 2. Isolate his very first driving stint of the race
stint_laps = laps[laps['Stint'] == 1]

# 3. Set our X axis (Tyre Age) and Y axis (Lap Time in seconds)
x = stint_laps['TyreLife']
y = stint_laps['LapTime'].dt.total_seconds()

# 4. THE ENGINE: Calculate the exact degradation rate using linear regression
m, b = np.polyfit(x, y, 1)
print(f"\n--- SUCCESS ---")
print(f"Verstappen's Stint 1 Degradation Rate: +{m:.3f} seconds per lap")

# 5. Plot the actual lap times (dots) and the mathematical degradation trendline
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Actual Lap Times')
plt.plot(x, m*x + b, color='red', linestyle='--', label=f'Degradation Slope (+{m:.3f}s/lap)')

# Make the chart look professional
plt.xlabel('Tyre Age (Laps)')
plt.ylabel('Lap Time (Seconds)')
plt.title('Tyre Degradation Engine: Verstappen Stint 1 (Bahrain 2024)')
plt.legend()
plt.grid(True, linestyle=':')

plt.show()