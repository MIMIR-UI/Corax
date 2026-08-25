## Setup For Dummies

In case you didn't know how to setup the pi and hat for the debugging process, here is a detailed explanation of what you need to do.

## 1. Flash the microSD card

Use Raspberry Pi Imager and install:

Raspberry Pi OS Lite 64-bit
Set a hostname such as corax-01
Set username to corax
Set a password
Add your Wi-Fi or hotspot
Enable SSH

For additional nodes, use different hostnames

## 2. Install the microSD and HAT
Insert the microSD into the Pi.
Install the LoRa HAT onto the GPIO header.
Attach the antenna before using the radio.
Power on the Pi.

## 3. Connect to the Pi

Your computer and Pi must be on the same network.

From PowerShell: 

ssh username@hostname.local 

EXAMPLE: ssh corax@corax-01.local

## 4. Enable the Pi serial port

On the Pi: 

sudo raspi-config

Go to:

Interface Options
→ Serial Port

Choose:

Login shell over serial: No
Serial hardware enabled: Yes

Then reboot. If not prompted to reboot, use: sudo reboot

Reconnect through SSH afterward.

## 5. Verify the serial port

Run: ls -l /dev/serial*

You should see something similar to:

/dev/serial0 -> ttyS0

## 6. Install Python serial support

Run:

sudo apt update
sudo apt install python3-serial

Verify it: 

python3 -c "import serial; print(serial.__version__)"

Then verify Python can open the UART:

python3 -c "import serial; s=serial.Serial('/dev/serial0',9600,timeout=1); print('serial open:',s.is_open); s.close()"

You want:

serial open: True

## 7. Configure the LoRa HAT jumpers

For normal Corax debugging:

Keep the M0 and M1 jumpers in normal transmission mode.
Set the lower communication-selection jumpers to:
B = Pi ↔ LoRa

Do not change the radio configuration jumpers while the Pi is powered.

## 8. Copy the debug files onto the Pi

The working Python files are located in the repository's debug branch.

On the Pi, create a folder:

mkdir -p ~/corax

From PowerShell on your computer, navigate to the folder containing the debug files:

cd "PATH\TO\YOUR\CORAX\DEBUG\FILES"

Copy them to the Pi:

scp main.py config.py message.py radio.py corax@corax-01.local:~/corax/

## 9. Set the node ID

Each Pi needs its own node ID inside config.py.

Example for Node 1:

NODE_ID = "CORAX-01"

Node 2:

NODE_ID = "CORAX-02"

Do not give two physical nodes the same NODE_ID.

## 10. Run Corax

SSH into the Pi and enter the project folder:

cd ~/corax

Run:

python3 main.py

Corax will ask for a temporary Session ID. Input whatever the hell you want. 

Also, messages should be addressed using the current Session ID, not the physical NODE_ID.

That's about as simple and directional as I can put it, thus, it's for dummies. 



## Useful Commands

Stop Corax:

Ctrl + C

Shut down the Pi safely:

sudo poweroff

Reboot:

sudo reboot

See the Pi's IP address:

hostname -I

Scan for Wi-Fi networks:

sudo nmcli device wifi rescan
nmcli device wifi list

Connect to Wi-Fi:

sudo nmcli device wifi connect "NETWORK NAME" password "PASSWORD"
