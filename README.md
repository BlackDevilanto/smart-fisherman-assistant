# smart-fisherman-assistant
a device can be used by the small scale fisherman to be informed about the weather and tidal data
Raspberry Pi DS1307 RTC Setup
This repository contains instructions for setting up and using a DS1307 Real-Time Clock (RTC) module with a Raspberry Pi.

The DS1307 is a low-power, full binary-coded decimal (BCD) clock/calendar with 56 bytes of NV SRAM. It communicates with the Raspberry Pi over the I²C interface, allowing the Pi to keep accurate time even when powered off (with a backup battery).

📌 Features
Persistent date & time storage via battery backup.

I²C communication for easy integration.

Can be used in projects that require accurate timestamps without internet access.

🛠 Hardware Requirements
Raspberry Pi (any model with I²C support)

DS1307 RTC module

CR2032 coin cell battery (for RTC backup)

Female-to-female jumper wires

📡 Wiring Connections
DS1307 Pin	Raspberry Pi Pin
VCC	3.3V or 5V
GND	GND
SDA	SDA (GPIO2, Pin 3)
SCL	SCL (GPIO3, Pin 5)

⚙️ Enabling I²C on Raspberry Pi
Open Raspberry Pi configuration:

bash
Copy
Edit
sudo raspi-config
Navigate to:

pgsql
Copy
Edit
Interface Options → I2C → Enable
Install I²C tools:

bash
Copy
Edit
sudo apt update
sudo apt install -y i2c-tools python3-smbus
Reboot your Raspberry Pi:

bash
Copy
Edit
sudo reboot
🔍 Checking DS1307 Detection
After reboot, run:

bash
Copy
Edit
sudo i2cdetect -y 1
You should see the DS1307 detected at address 0x68.

⏱️ Configuring the DS1307 as the Hardware Clock
Load the RTC kernel module:

bash
Copy
Edit
sudo modprobe rtc-ds1307
Add the RTC device:

bash
Copy
Edit
sudo bash -c "echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device"
Check if /dev/rtc0 exists:

bash
Copy
Edit
ls /dev/rtc*
Read the current RTC time:

bash
Copy
Edit
sudo hwclock -r
To set the RTC time from the system clock:

bash
Copy
Edit
sudo hwclock -w
🐍 Python Dependencies
If you want to interact with the DS1307 using Python, install the following packages:

bash
Copy
Edit
pip install smbus2 RPi.GPIO
These allow I²C communication and GPIO control in Python scripts.

📜 Notes
Ensure the battery is installed
🖥 Setting up DS1307 as System RTC
Edit boot configuration:

bash
Copy
Edit
sudo nano /boot/config.txt
Add at the end:

ini
Copy
Edit
dtoverlay=i2c-rtc,ds1307
Reboot:

bash
Copy
Edit
sudo reboot
Disable the fake hardware clock:

bash
Copy
Edit
sudo apt-get remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove
Sync system time from RTC:

bash
Copy
Edit
sudo hwclock -r   # Read from RTC
sudo hwclock -w   # Write current system time to RTC
🧪 Testing RTC
Unplug your Raspberry Pi from the internet and reboot:

bash
Copy
Edit
date
You should see the correct time maintained.

📄 License
This project is licensed under the MIT License.

🤝 Contributing
Pull requests are welcome! For significant changes, please open an issue first to discuss your idea.


