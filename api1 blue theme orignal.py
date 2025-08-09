import tkinter as tk
from tkinter import messagebox
import requests
import json
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
from geopy.geocoders import Nominatim
import io
from PIL import Image, ImageTk

# DejaVuSans font setup
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font = fm.FontProperties(fname=font_path)
tk_font = ("DejaVu Sans", 12)

# API key
STORMGLASS_API_KEY = '653cd430-22ae-11f0-88e2-0242ac130003-653cd48a-22ae-11f0-88e2-0242ac130003'

# Color theme
BACKGROUND_COLOR = "#d0eaff"  # light sky blue
FRAME_COLOR = "#f0faff"       # even lighter
BUTTON_COLOR = "#66b3ff"      # bright blue
TEXT_COLOR = "#003366"        # dark blue

# GUI setup
root = tk.Tk()
root.title("🌊 Tide, Weather, and Wave Forecast ")
root.geometry("1200x800")
root.configure(bg=BACKGROUND_COLOR)

main_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
main_frame.pack(fill="both", expand=True)

left_frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=2, relief="ridge")
left_frame.pack(side="left", padx=10, pady=10)

right_frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=2, relief="ridge")
right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Left side (Map)
map_label = tk.Label(left_frame, bg=FRAME_COLOR)
map_label.pack()

# Right side (Info + Graphs)
top_frame = tk.Frame(right_frame, bg=FRAME_COLOR)
top_frame.pack()

bottom_frame = tk.Frame(right_frame, bg=FRAME_COLOR)
bottom_frame.pack()

frame_top_labels = tk.Frame(top_frame, bg=FRAME_COLOR)
frame_top_labels.pack(pady=10)

clock_label = tk.Label(frame_top_labels, text="Time: ", font=tk_font, fg=TEXT_COLOR, bg=FRAME_COLOR)
clock_label.grid(row=0, column=0, sticky="w", padx=5)

status_label = tk.Label(frame_top_labels, text="Status: Waiting for location...", font=tk_font, fg="orange", bg=FRAME_COLOR)
status_label.grid(row=0, column=1, sticky="w", padx=5)

location_entry = tk.Entry(top_frame, font=tk_font, bg="#ffffff", fg=TEXT_COLOR, relief="sunken", bd=2)
location_entry.insert(0, "Thoothukudi")
location_entry.pack(pady=5)

frame_info = tk.Frame(top_frame, bg=FRAME_COLOR)
frame_info.pack()

tide_label = tk.Label(frame_info, text="Tide Info:", font=tk_font, justify="left", bg=FRAME_COLOR, fg=TEXT_COLOR)
tide_label.grid(row=0, column=0, padx=10, sticky="nw")

wave_info_label = tk.Label(frame_info, text="Wave Info:", font=tk_font, justify="left", bg=FRAME_COLOR, fg=TEXT_COLOR)
wave_info_label.grid(row=0, column=1, padx=10, sticky="nw")

weather_label = tk.Label(top_frame, text="Weather Info:", font=tk_font, justify="left", bg=FRAME_COLOR, fg=TEXT_COLOR)
weather_label.pack(pady=5)

refresh_button = tk.Button(top_frame, text="🔄 Refresh", font=tk_font, bg=BUTTON_COLOR, fg="white", activebackground="#3399ff", activeforeground="white", command=lambda: fetch_data(), relief="raised", bd=3)
refresh_button.pack(pady=10)

# Graphs
figure, (tide_plot, wave_plot) = plt.subplots(2, 1, figsize=(8, 6), dpi=100)
figure.tight_layout(pad=3.0)
canvas = FigureCanvasTkAgg(figure, bottom_frame)
canvas.get_tk_widget().pack()

geolocator = Nominatim(user_agent="tide_weather_app")

def fetch_data():
    location_name = location_entry.get()
    if not location_name.strip():
        messagebox.showerror("Input Error", "Please enter a valid location.")
        return

    try:
        location = geolocator.geocode(location_name)
        if not location:
            messagebox.showerror("Geocoding Error", "Location not found. Please try again.")
            return

        lat, lon = location.latitude, location.longitude

        # Time range
        now = datetime.datetime.utcnow()
        end_time = now + datetime.timedelta(hours=12)

        # Fetch tide elevation data
        tide_url = (
            f"https://api.stormglass.io/v2/tide/extremes/point?"
            f"lat={lat}&lng={lon}&start={now.isoformat()}&end={end_time.isoformat()}"
        )
        headers = {"Authorization": STORMGLASS_API_KEY}
        tide_response = requests.get(tide_url, headers=headers, timeout=10)
        tide_data = tide_response.json()

        # Fetch weather & wave data
        weather_url = (
            f"https://api.stormglass.io/v2/weather/point?"
            f"lat={lat}&lng={lon}&params=waveHeight,windSpeed,airTemperature&"
            f"start={now.isoformat()}&end={end_time.isoformat()}"
        )
        weather_response = requests.get(weather_url, headers=headers, timeout=10)
        weather_data = weather_response.json()

        # Fetch map
        map_url = f"https://static-maps.yandex.ru/1.x/?ll={lon},{lat}&z=10&size=450,300&l=map&pt={lon},{lat},pm2rdm"
        map_response = requests.get(map_url)
        image_data = map_response.content
        image = Image.open(io.BytesIO(image_data))
        map_image = ImageTk.PhotoImage(image)
        map_label.config(image=map_image)
        map_label.image = map_image

        # Tide info
        extremes = tide_data.get("data", [])
        if extremes:
            tide_times = [datetime.datetime.strptime(e['time'], "%Y-%m-%dT%H:%M:%S+00:00").strftime('%H:%M') for e in extremes]
            tide_heights = [e['height'] for e in extremes]

            tide_text = "\n".join([f"{extremes[i]['type'].capitalize()} at {tide_times[i]}: {round(tide_heights[i],2)} m" for i in range(len(tide_times))])
        else:
            tide_text = "Tide info unavailable."

        tide_label.config(text=tide_text)

        # Weather and wave info
        hours_data = weather_data.get('hours', [])

        wave_heights = []
        wave_times = []
        temperatures = []
        wind_speeds = []

        for hour in hours_data[:12]:
            time = hour.get('time', '')
            wave = hour.get('waveHeight', {}).get('noaa', None)
            temp = hour.get('airTemperature', {}).get('noaa', None)
            wind = hour.get('windSpeed', {}).get('noaa', None)

            if wave is not None:
                wave_heights.append(wave)
                wave_times.append(datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S+00:00").strftime("%H:%M"))
            if temp is not None:
                temperatures.append(temp)
            if wind is not None:
                wind_speeds.append(wind)

        if wave_heights:
            wave_text = "\n".join([f"At {wave_times[i]}: {round(wave_heights[i],2)} meters" for i in range(len(wave_times))])
        else:
            wave_text = "Wave height info unavailable."

        wave_info_label.config(text=wave_text)

        if temperatures and wind_speeds:
            weather_label.config(text=f"Temperature: {temperatures[0]}°C\nWind Speed: {wind_speeds[0]} m/s")
        else:
            weather_label.config(text="Weather information unavailable.")

        # Graphs
        tide_plot.clear()
        wave_plot.clear()

        if extremes:
            tide_plot.plot(tide_times, tide_heights, marker='o', color='b', label="Tide Height (m)")
            tide_plot.set_title("Tide Height ", fontproperties=font)
            tide_plot.set_xlabel("Time (UTC)", fontproperties=font)
            tide_plot.set_ylabel("Height (m)", fontproperties=font)
            tide_plot.tick_params(axis='x', rotation=45)
            tide_plot.legend()

        if wave_heights:
            wave_plot.plot(wave_times, wave_heights, marker='x', color='g', label="Wave Height (m)")
            wave_plot.set_title("Wave Height ", fontproperties=font)
            wave_plot.set_xlabel("Time (UTC)", fontproperties=font)
            wave_plot.set_ylabel("Height (m)", fontproperties=font)
            wave_plot.tick_params(axis='x', rotation=45)
            wave_plot.legend()

        canvas.draw()

        status_label.config(text=f"Status: Showing data for {location_name}", fg="green")

    except Exception as e:
        print(f"Error: {e}")
        status_label.config(text="Status: Error fetching data", fg="red")
        tide_label.config(text="Tide information unavailable.")
        wave_info_label.config(text="Wave information unavailable.")
        weather_label.config(text="Weather information unavailable.")
        map_label.config(image='')

        tide_plot.clear()
        wave_plot.clear()
        tide_plot.set_title("No data available", fontproperties=font)
        wave_plot.set_title("No data available", fontproperties=font)
        canvas.draw()

def update_clock():
    now = datetime.datetime.now().strftime('%H:%M:%S')
    clock_label.config(text=f"Time: {now}")
    root.after(1000, update_clock)

# Start
update_clock()
root.after(2000, fetch_data)

root.mainloop()

