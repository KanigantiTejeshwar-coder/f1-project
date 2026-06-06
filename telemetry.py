import fastf1
import matplotlib.pyplot as plt

# Connect to your cache
fastf1.Cache.enable_cache('./cache')

print("Loading data... (This will be instant this time!)")
session = fastf1.get_session(2024, 'Silverstone', 'Q')
session.load()

# 1. Grab the fastest laps for both drivers
ver_lap = session.laps.pick_drivers('VER').pick_fastest()
nor_lap = session.laps.pick_drivers('NOR').pick_fastest()

# 2. Extract the car telemetry and calculate track distance
ver_tel = ver_lap.get_car_data().add_distance()
nor_tel = nor_lap.get_car_data().add_distance()

# 3. Build the graph!
print("Drawing graph...")
plt.figure(figsize=(12, 6))

# Plot Verstappen (Blue) and Norris (Orange)
plt.plot(ver_tel['Distance'], ver_tel['Speed'], label='Verstappen', color='blue')
plt.plot(nor_tel['Distance'], nor_tel['Speed'], label='Norris', color='orange')

# Add labels and titles
plt.xlabel('Track Distance (meters)')
plt.ylabel('Speed (km/h)')
plt.title('2024 Silverstone Qualifying: Verstappen vs Norris')
plt.legend()

# Show the final chart on your screen
plt.show()