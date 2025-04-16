from machine import Pin
import ujson
import network
import utime as time
import urequests as requests

# Konfigurasi
DEVICE_ID = "esp32"
WIFI_SSID = "PEXIST106_9"
WIFI_PASSWORD = "imanilmuamal"
TOKEN = "BBUS-8Iob9h82Y8og37zgb2tCSde4jVHTh9"

# Inisialisasi sensor
PIR_PIN = Pin(14, Pin.IN)

# Fungsi buat JSON
def create_json_data(motion):
    data = ujson.dumps({
        "device_id": DEVICE_ID,
        "motion": motion,
        "type": "sensor"
    })
    return data

# Fungsi untuk kirim data ke Ubidots
def send_data(motion):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
    headers = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}
    data = {
        "motion": motion,
    }
    response = requests.post(url, json=data, headers=headers)
    print("Response:", response.text)

# Koneksi WiFi
wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Connecting device to WiFi")
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi_client.isconnected():
    print("Connecting...")
    time.sleep(0.5)

print("WiFi Connected!")
print(wifi_client.ifconfig())

# Loop utama
telemetry_data_old = ""

while True:
    try:
        motion = PIR_PIN.value()  # Baca status sensor PIR
        
        telemetry_data_new = create_json_data(motion)

        if telemetry_data_new != telemetry_data_old:
            telemetry_data_old = telemetry_data_new
            send_data(motion)

        time.sleep(3)

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
