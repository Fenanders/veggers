#include <LiquidCrystal_I2C.h>
#include <DHT.h>

// Set the LCD number of columns and rows
int lcdColumns = 16;
int lcdRows = 2;

// Setup Soil and Temp PIN
#define DHTTYPE DHT_11
#define SOIL_PIN A0
#define DATA_PIN D1

DHT dht(DATA_PIN, DHT11);

// Set LCD address, number of columns and rows
LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);

void setup() {
  // Initialize LCD
  lcd.init();
  // Turn on LCD backlight
  lcd.backlight();

  Serial.begin(115200);
  dht.begin();

  turnOnSetup();
}

void turnOnSetup() {
  lcd.setCursor(0, 0);
  lcd.println("Hi!");

  lcd.setCursor(0, 1);
  lcd.print("Mr Yandi Fenanda");
  delay(3000);
  lcd.clear();
}

float readSoilMoisture() {
  int soilVal = analogRead(SOIL_PIN);
  float soilMoist = (soilVal - 0) * 100.0 / (1023 - 0);
  return soilMoist;
}

void checkTemperature(float &temp, float &humidity) {
  temp = dht.readTemperature();
  humidity = dht.readHumidity();
  if (isnan(temp) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
  }
}

void loop() {
  float moisture = readSoilMoisture();
  Serial.printf("Soil Moisture: %.2f%%\n", moisture);

  float temp, humidity;
  checkTemperature(temp, humidity);
  if (!isnan(temp) && !isnan(humidity)) {
    lcd.clear();

    lcd.setCursor(0, 1);
    lcd.print("loading....");
    delay(3000);
    lcd.clear();

    Serial.printf("Temperature: %.2f C, Humidity: %.2f%%\n", temp, humidity);

    // Display soil moisture on the first row
    lcd.setCursor(0, 0);
    lcd.print("Moist: ");
    lcd.print(moisture, 1);
    lcd.print("%");

    // Display temperature and humidity on the second row
    lcd.setCursor(0, 1);
    lcd.print(temp, 1);
    lcd.print("C ");
    lcd.print("Hum: ");
    lcd.print(humidity, 1);
    lcd.print("%");
  } else {
    Serial.println("Sensor reading failed");
    lcd.setCursor(0, 0);
    lcd.print("Sensor Error!   ");
    lcd.setCursor(0, 1);
    lcd.print("Check Connections");
  }

  delay(5000);  // Sleep for next reading
}