# make config files
import secrets

def make_config(id, ip):
    enc = secrets.token_urlsafe(32)
    pswd = secrets.token_hex(16)
    config = """
esphome:
  name: nasa%02d

esp32:
  board: esp32cam
  framework:
    type: arduino

# Enable logging
logger:

# Enable Home Assistant API
api:
  password: '%s'
  encryption:
    key: "%s"

ota:
  password: "%s"

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  
  # Optional manual IP
  manual_ip:
    static_ip: 10.42.0.%i
    gateway: 10.42.0.1
    subnet: 255.255.255.0

captive_portal:

# Example configuration entry
esp32_camera:
  external_clock:
    pin: GPIO0
    frequency: 20MHz
  i2c_pins:
    sda: GPIO26
    scl: GPIO27
  data_pins: [GPIO5, GPIO18, GPIO19, GPIO21, GPIO36, GPIO39, GPIO34, GPIO35]
  vsync_pin: GPIO25
  href_pin: GPIO23
  pixel_clock_pin: GPIO22
  power_down_pin: GPIO32
  resolution: 1600x1200

  # Image settings
  name: NASA%02d

# Example configuration entry
esp32_camera_web_server:
  - port: 8080
    mode: stream
  - port: 8081
    mode: snapshot
    
# LED flash configuration
light:
  - platform: binary
    name: "Flash"
    output: light_output
    restore_mode: ALWAYS_OFF

output:
  - id: light_output
    platform: gpio
    pin: GPIO04

"""%(id,pswd, enc,pswd,ip,id)

    return config

for id in range(6,24):
    s= make_config(id, id+20)
    with open('nasa%02d.yaml'%id, 'w') as fout:
        fout.write(s)