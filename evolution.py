import fastf1
import matplotlib.pyplot as plt

# Connect to the cache
fastf1.Cache.enable_cache('./cache')

print("Loading Silverstone Qualifying Data... (Loading from cache!)")
session = fastf1.get_session(2024, 'Silverstone', 'Q')
session.load()

# Grab the final results table
results = session.results

# Filter for just the Top 5 drivers so the graph doesn't get too cluttered
top_5 = results.head(5)

print("\n--- DRAWING TRACK EVOLUTION CHART ---")
plt.figure(figsize=(10, 6))

# Loop through each of the top 5 drivers and plot their progression
for index, driver in top_5.iterrows():
    
    # Extract times and convert to pure seconds
    q1 = driver['Q1'].total_seconds()
    q2 = driver['Q2'].total_seconds()
    q3 = driver['Q3'].total_seconds()
    
    times = [q1, q2, q3]
    sessions = ['Q1', 'Q2', 'Q3']
    
    # Plot a line with dots for each session
    plt.plot(sessions, times, marker='o', linewidth=2, label=driver['Abbreviation'])

# Format the graph
plt.xlabel('Qualifying Session')
plt.ylabel('Lap Time (Seconds)')
plt.title('Track Evolution: Top 5 Drivers (Silverstone 2024 Qualifying)')
plt.legend()
plt.grid(True, linestyle=':')

# Show the chart
plt.show()