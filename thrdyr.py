import firebase_admin
from firebase_admin import credentials, db
import serial
import time

# === Initialize Firebase ===
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://real-time-energy-monitor-98ea1-default-rtdb.firebaseio.com/'
})

# === Connect to Arduino ===
try:
    arduino = serial.Serial('COM8', 9600, timeout=1)  # Adjust COM port if needed
    time.sleep(2)  # Wait for Arduino to initialize
    print("✅ Arduino connected.")
except serial.SerialException as e:
    print("❌ Could not open serial port:", e)
    exit()

# === Firebase reference ===
control_ref = db.reference("/sensor/control")
last_command = ""

# === Main Loop ===
while True:
    try:
        command = control_ref.get()
        if command and command != last_command:
            arduino.write((command.strip() + "\n").encode('utf-8'))
            print(f"📤 Sent command: {command}")
            last_command = command
        time.sleep(1)
    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(2)
