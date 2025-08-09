# smart-fisherman-assistant
a device can be used by the small scale fisherman to be informed about the weather and tidal data
Raspberry Pi DS1307 RTC Module Setup
 This repository provides a step-by-step guide to set up a DS1307 Real Time Clock (RTC) module
 on a Raspberry Pi.
 Requirements
 Hardware:- Raspberry Pi (any model with I2C support)- DS1307 RTC Module- Jumper wires
 Software:- Raspberry Pi OS (Bookworm or Bullseye recommended)- I2C tools- Python 3- SMBus library
 Installation Steps
 1. Enable I2C on Raspberry Pi
 Run:
 sudo raspi-config
 Navigate to:
 Interfacing Options → I2C → Enable
 2. Install Required Packages
 sudo apt update
 sudo apt install i2c-tools python3-smbus
 3. Check if RTC is Detected
 sudo i2cdetect -y 1
 If detected, you will see `68` in the output grid.
 4. Load RTC Kernel Module
sudo modprobe rtc-ds1307
 5. Add RTC to Boot Configuration
 Edit `/boot/config.txt`:
 dtoverlay=i2c-rtc,ds1307
 6. Remove Fake Hardware Clock
 sudo apt-get -y remove fake-hwclock
 sudo update-rc.d -f fake-hwclock remove
 7. Sync System Time with RTC
 On boot, the Raspberry Pi will read the time from the RTC.
 You can manually sync with:
 sudo hwclock -r
 sudo hwclock -w
 Python Dependencies- Python 3.x- smbus (`sudo apt install python3-smbus`
📄 License
This project is licensed under the MIT License.

🤝 Contributing
Pull requests are welcome! For significant changes, please open an issue first to discuss your idea.


