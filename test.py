import fastf1

# Tell Python to save downloaded data inside our local "cache" folder
fastf1.Cache.enable_cache('./cache')

print("Connecting to F1 Servers... This will take a moment on the first run...")

# Request the 2024 British Grand Prix Qualifying data
session = fastf1.get_session(2024, 'Silverstone', 'Q')
session.load()

# Grab Max Verstappen's fastest qualifying lap
max_lap = session.laps.pick_drivers('VER').pick_fastest()

print("\n--- SUCCESS! ---")
print(f"Max Verstappen fastest lap: {max_lap['LapTime']}")