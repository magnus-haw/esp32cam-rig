// Auto generated code by esphome
// ========== AUTO GENERATED INCLUDE BLOCK BEGIN ===========
#include "esphome.h"
using namespace esphome;
using std::isnan;
using std::min;
using std::max;
using namespace light;
using namespace text_sensor;
logger::Logger *logger_logger;
web_server_base::WebServerBase *web_server_base_webserverbase;
captive_portal::CaptivePortal *captive_portal_captiveportal;
wifi::WiFiComponent *wifi_wificomponent;
mdns::MDNSComponent *mdns_mdnscomponent;
ota::OTAComponent *ota_otacomponent;
api::APIServer *api_apiserver;
using namespace api;
preferences::IntervalSyncer *preferences_intervalsyncer;
esp32_camera::ESP32Camera *esp32_camera_esp32camera;
esp32_camera_web_server::CameraWebServer *esp32_camera_web_server_camerawebserver;
esp32_camera_web_server::CameraWebServer *esp32_camera_web_server_camerawebserver_2;
binary::BinaryLightOutput *binary_binarylightoutput;
light::LightState *light_lightstate;
using namespace output;
gpio::GPIOBinaryOutput *light_output;
esp32::ArduinoInternalGPIOPin *esp32_arduinointernalgpiopin;
wifi_info::IPAddressWiFiInfo *wifi_info_ipaddresswifiinfo;
psram::PsramComponent *psram_psramcomponent;
#define yield() esphome::yield()
#define millis() esphome::millis()
#define micros() esphome::micros()
#define delay(x) esphome::delay(x)
#define delayMicroseconds(x) esphome::delayMicroseconds(x)
// ========== AUTO GENERATED INCLUDE BLOCK END ==========="

void setup() {
  // ========== AUTO GENERATED CODE BEGIN ===========
  // async_tcp:
  //   {}
  // esphome:
  //   name: nasa14
  //   build_path: .esphome/build/nasa14
  //   platformio_options: {}
  //   includes: []
  //   libraries: []
  //   name_add_mac_suffix: false
  App.pre_setup("nasa14", __DATE__ ", " __TIME__, false);
  // light:
  // text_sensor:
  // logger:
  //   id: logger_logger
  //   baud_rate: 115200
  //   tx_buffer_size: 512
  //   deassert_rts_dtr: false
  //   hardware_uart: UART0
  //   level: DEBUG
  //   logs: {}
  logger_logger = new logger::Logger(115200, 512, logger::UART_SELECTION_UART0);
  logger_logger->pre_setup();
  logger_logger->set_component_source("logger");
  App.register_component(logger_logger);
  // web_server_base:
  //   id: web_server_base_webserverbase
  web_server_base_webserverbase = new web_server_base::WebServerBase();
  web_server_base_webserverbase->set_component_source("web_server_base");
  App.register_component(web_server_base_webserverbase);
  // captive_portal:
  //   id: captive_portal_captiveportal
  //   web_server_base_id: web_server_base_webserverbase
  captive_portal_captiveportal = new captive_portal::CaptivePortal(web_server_base_webserverbase);
  captive_portal_captiveportal->set_component_source("captive_portal");
  App.register_component(captive_portal_captiveportal);
  // wifi:
  //   id: wifi_wificomponent
  //   domain: .local
  //   reboot_timeout: 15min
  //   power_save_mode: LIGHT
  //   fast_connect: false
  //   networks:
  //   - ssid: !secret 'wifi_password'
  //     password: !secret 'wifi_password'
  //     id: wifi_wifiap
  //     priority: 0.0
  //   use_address: nasa14.local
  wifi_wificomponent = new wifi::WiFiComponent();
  wifi_wificomponent->set_use_address("nasa14.local");
  wifi::WiFiAP wifi_wifiap = wifi::WiFiAP();
  wifi_wifiap.set_ssid("shadowfax");
  wifi_wifiap.set_password("shadowfax");
  wifi_wifiap.set_priority(0.0f);
  wifi_wificomponent->add_sta(wifi_wifiap);
  wifi_wificomponent->set_reboot_timeout(900000);
  wifi_wificomponent->set_power_save_mode(wifi::WIFI_POWER_SAVE_LIGHT);
  wifi_wificomponent->set_fast_connect(false);
  wifi_wificomponent->set_component_source("wifi");
  App.register_component(wifi_wificomponent);
  // mdns:
  //   id: mdns_mdnscomponent
  //   disabled: false
  mdns_mdnscomponent = new mdns::MDNSComponent();
  mdns_mdnscomponent->set_component_source("mdns");
  App.register_component(mdns_mdnscomponent);
  // ota:
  //   password: 0df4c01c653a82360f74076a90494f41
  //   id: ota_otacomponent
  //   safe_mode: true
  //   port: 3232
  //   reboot_timeout: 5min
  //   num_attempts: 10
  ota_otacomponent = new ota::OTAComponent();
  ota_otacomponent->set_port(3232);
  ota_otacomponent->set_auth_password("0df4c01c653a82360f74076a90494f41");
  ota_otacomponent->set_component_source("ota");
  App.register_component(ota_otacomponent);
  if (ota_otacomponent->should_enter_safe_mode(10, 300000)) return;
  // api:
  //   password: MyPassword
  //   encryption:
  //     key: G0CqAnEYZPWgtwsUBQqh8bUrz3gR6fdxOckJxt96Fgg=
  //   id: api_apiserver
  //   port: 6053
  //   reboot_timeout: 15min
  api_apiserver = new api::APIServer();
  api_apiserver->set_component_source("api");
  App.register_component(api_apiserver);
  api_apiserver->set_port(6053);
  api_apiserver->set_password("MyPassword");
  api_apiserver->set_reboot_timeout(900000);
  api_apiserver->set_noise_psk({27, 64, 170, 2, 113, 24, 100, 245, 160, 183, 11, 20, 5, 10, 161, 241, 181, 43, 207, 120, 17, 233, 247, 113, 57, 201, 9, 198, 223, 122, 22, 8});
  // esp32:
  //   board: esp32cam
  //   framework:
  //     version: 1.0.6
  //     source: ~3.10006.0
  //     platform_version: platformio/espressif32 @ 3.5.0
  //     type: arduino
  //   variant: ESP32
  // preferences:
  //   id: preferences_intervalsyncer
  //   flash_write_interval: 60s
  preferences_intervalsyncer = new preferences::IntervalSyncer();
  preferences_intervalsyncer->set_write_interval(60000);
  preferences_intervalsyncer->set_component_source("preferences");
  App.register_component(preferences_intervalsyncer);
  // esp32_camera:
  //   external_clock:
  //     pin: 0
  //     frequency: 20000000.0
  //   i2c_pins:
  //     sda: 26
  //     scl: 27
  //   data_pins:
  //   - 5
  //   - 18
  //   - 19
  //   - 21
  //   - 36
  //   - 39
  //   - 34
  //   - 35
  //   vsync_pin: 25
  //   href_pin: 23
  //   pixel_clock_pin: 22
  //   power_down_pin: 32
  //   resolution: 1600X1200
  //   name: NASA14
  //   disabled_by_default: false
  //   id: esp32_camera_esp32camera
  //   jpeg_quality: 10
  //   contrast: 0
  //   brightness: 0
  //   saturation: 0
  //   vertical_flip: true
  //   horizontal_mirror: true
  //   special_effect: NONE
  //   agc_mode: AUTO
  //   aec2: false
  //   ae_level: 0
  //   aec_value: 300
  //   aec_mode: AUTO
  //   agc_value: 0
  //   agc_gain_ceiling: 2X
  //   wb_mode: AUTO
  //   test_pattern: false
  //   max_framerate: 10.0
  //   idle_framerate: 0.1
  esp32_camera_esp32camera = new esp32_camera::ESP32Camera();
  esp32_camera_esp32camera->set_name("NASA14");
  esp32_camera_esp32camera->set_disabled_by_default(false);
  esp32_camera_esp32camera->set_component_source("esp32_camera");
  App.register_component(esp32_camera_esp32camera);
  esp32_camera_esp32camera->set_data_pins({5, 18, 19, 21, 36, 39, 34, 35});
  esp32_camera_esp32camera->set_vsync_pin(25);
  esp32_camera_esp32camera->set_href_pin(23);
  esp32_camera_esp32camera->set_pixel_clock_pin(22);
  esp32_camera_esp32camera->set_power_down_pin(32);
  esp32_camera_esp32camera->set_jpeg_quality(10);
  esp32_camera_esp32camera->set_vertical_flip(true);
  esp32_camera_esp32camera->set_horizontal_mirror(true);
  esp32_camera_esp32camera->set_contrast(0);
  esp32_camera_esp32camera->set_brightness(0);
  esp32_camera_esp32camera->set_saturation(0);
  esp32_camera_esp32camera->set_special_effect(esp32_camera::ESP32_SPECIAL_EFFECT_NONE);
  esp32_camera_esp32camera->set_aec_mode(esp32_camera::ESP32_GC_MODE_AUTO);
  esp32_camera_esp32camera->set_aec2(false);
  esp32_camera_esp32camera->set_ae_level(0);
  esp32_camera_esp32camera->set_aec_value(300);
  esp32_camera_esp32camera->set_agc_mode(esp32_camera::ESP32_GC_MODE_AUTO);
  esp32_camera_esp32camera->set_agc_value(0);
  esp32_camera_esp32camera->set_agc_gain_ceiling(esp32_camera::ESP32_GAINCEILING_2X);
  esp32_camera_esp32camera->set_wb_mode(esp32_camera::ESP32_WB_MODE_AUTO);
  esp32_camera_esp32camera->set_test_pattern(false);
  esp32_camera_esp32camera->set_external_clock(0, 20000000.0f);
  esp32_camera_esp32camera->set_i2c_pins(26, 27);
  esp32_camera_esp32camera->set_max_update_interval(100.0f);
  esp32_camera_esp32camera->set_idle_update_interval(10000.0f);
  esp32_camera_esp32camera->set_frame_size(esp32_camera::ESP32_CAMERA_SIZE_1600X1200);
  // esp32_camera_web_server:
  //   port: 8080
  //   mode: STREAM
  //   id: esp32_camera_web_server_camerawebserver
  esp32_camera_web_server_camerawebserver = new esp32_camera_web_server::CameraWebServer();
  esp32_camera_web_server_camerawebserver->set_port(8080);
  esp32_camera_web_server_camerawebserver->set_mode(esp32_camera_web_server::STREAM);
  esp32_camera_web_server_camerawebserver->set_component_source("esp32_camera_web_server");
  App.register_component(esp32_camera_web_server_camerawebserver);
  // esp32_camera_web_server:
  //   port: 8081
  //   mode: SNAPSHOT
  //   id: esp32_camera_web_server_camerawebserver_2
  esp32_camera_web_server_camerawebserver_2 = new esp32_camera_web_server::CameraWebServer();
  esp32_camera_web_server_camerawebserver_2->set_port(8081);
  esp32_camera_web_server_camerawebserver_2->set_mode(esp32_camera_web_server::SNAPSHOT);
  esp32_camera_web_server_camerawebserver_2->set_component_source("esp32_camera_web_server");
  App.register_component(esp32_camera_web_server_camerawebserver_2);
  // light.binary:
  //   platform: binary
  //   name: Flash
  //   output: light_output
  //   restore_mode: ALWAYS_OFF
  //   disabled_by_default: false
  //   id: light_lightstate
  //   output_id: binary_binarylightoutput
  binary_binarylightoutput = new binary::BinaryLightOutput();
  light_lightstate = new light::LightState(binary_binarylightoutput);
  App.register_light(light_lightstate);
  light_lightstate->set_component_source("light");
  App.register_component(light_lightstate);
  light_lightstate->set_name("Flash");
  light_lightstate->set_disabled_by_default(false);
  light_lightstate->set_restore_mode(light::LIGHT_ALWAYS_OFF);
  light_lightstate->add_effects({});
  // output:
  // output.gpio:
  //   platform: gpio
  //   id: light_output
  //   pin:
  //     number: 4
  //     mode:
  //       output: true
  //       input: false
  //       open_drain: false
  //       pullup: false
  //       pulldown: false
  //     id: esp32_arduinointernalgpiopin
  //     inverted: false
  light_output = new gpio::GPIOBinaryOutput();
  light_output->set_component_source("gpio.output");
  App.register_component(light_output);
  esp32_arduinointernalgpiopin = new esp32::ArduinoInternalGPIOPin();
  esp32_arduinointernalgpiopin->set_pin(4);
  esp32_arduinointernalgpiopin->set_inverted(false);
  esp32_arduinointernalgpiopin->set_flags(gpio::Flags::FLAG_OUTPUT);
  light_output->set_pin(esp32_arduinointernalgpiopin);
  // text_sensor.wifi_info:
  //   platform: wifi_info
  //   ip_address:
  //     name: ESPip
  //     disabled_by_default: false
  //     id: wifi_info_ipaddresswifiinfo
  //     entity_category: diagnostic
  //     update_interval: 1s
  wifi_info_ipaddresswifiinfo = new wifi_info::IPAddressWiFiInfo();
  App.register_text_sensor(wifi_info_ipaddresswifiinfo);
  wifi_info_ipaddresswifiinfo->set_name("ESPip");
  wifi_info_ipaddresswifiinfo->set_disabled_by_default(false);
  wifi_info_ipaddresswifiinfo->set_entity_category(::ENTITY_CATEGORY_DIAGNOSTIC);
  wifi_info_ipaddresswifiinfo->set_update_interval(1000);
  wifi_info_ipaddresswifiinfo->set_component_source("wifi_info.text_sensor");
  App.register_component(wifi_info_ipaddresswifiinfo);
  // socket:
  //   implementation: bsd_sockets
  // network:
  //   {}
  // psram:
  //   id: psram_psramcomponent
  psram_psramcomponent = new psram::PsramComponent();
  psram_psramcomponent->set_component_source("psram");
  App.register_component(psram_psramcomponent);
  binary_binarylightoutput->set_output(light_output);
  // =========== AUTO GENERATED CODE END ============
  App.setup();
}

void loop() {
  App.loop();
}
