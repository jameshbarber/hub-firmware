#include "WiFiS3.h"
#include <OneWire.h>
#include <DallasTemperature.h>

char ssid[] = SECRET_SSID;          // your network SSID (name)
char pass[] = SECRET_OPTIONAL_PASS; // your network password
int led = LED_BUILTIN;
WiFiServer server(80);

#define ONE_WIRE_BUS 10
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

int lightSensorPin = A0; // Light sensor is connected to analog pin A0
int humiditySensorPin = A1; // Potentiometer simulating humidity sensor connected to analog pin A1

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);

  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    while (true); // stop further execution if no WiFi module is present
  }

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }

  WiFi.setHostname("sensor-hub");

  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);
    delay(10000);
  }
  server.begin();
  sensors.begin();
  printWifiStatus();
}

void loop() {
  WiFiClient client = server.available(); // listen for incoming clients

  if (client) {
    Serial.println("New client"); // print a message out the serial port
    String currentLine = ""; // make a String to hold incoming data from the client
    while (client.connected()) { // loop while the client's connected
      while (client.available()) { // if there's bytes to read from the client,
        char c = client.read(); // read a byte, then
        Serial.write(c); // print it out to the serial monitor
        if (c == '\n') { // if the byte is a newline character
          if (currentLine.length() == 0) {
            sendJSONResponse(client);
            break; // Exit the while loop after sending the response
          }
          currentLine = ""; // Clear currentLine after processing
        } else if (c != '\r') {
          currentLine += c;  // add it to the end of the currentLine
        }
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  }
}


void sendJSONResponse(WiFiClient& client) {
  // Request temperature data from the DallasTemperature sensor
  sensors.requestTemperatures();
  float temperature = sensors.getTempCByIndex(0);
  
  // Read light sensor value from the analog pin
  int lightValue = analogRead(lightSensorPin);
  
  // Read the analog value from the potentiometer (simulating humidity)
  int rawHumidityValue = analogRead(humiditySensorPin);
  
  // Map the raw humidity value from 9-1016 to 0-100
  int humidityValue = map(rawHumidityValue, 9, 1016, 0, 100);

  // Prepare the JSON response as a String to calculate content length
  String jsonResponse = "{\"temperature\": " + String(temperature, 2) + 
                        ", \"light\": " + String(lightValue) + 
                        ", \"humidity\": " + String(humidityValue) + "}";
  
  // Calculate the content length
  int contentLength = jsonResponse.length();

  // Send HTTP headers
  client.println("HTTP/1.1 200 OK");
  client.println("Content-type: application/json");
  client.print("Content-Length: ");
  client.println(contentLength);
  client.println("Connection: close");
  client.println(); // End of headers

  // Send JSON object
  client.println(jsonResponse);

  // Ensure the client connection is closed after sending the response
  client.stop();
}


void printWifiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");

  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
}
