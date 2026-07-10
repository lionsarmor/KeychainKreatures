/*
  Keychain Kreatures Factory Test
  ESP32-C3 Super Mini
*/

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include "driver/i2s.h"
#include <math.h>

// Display
#define TFT_SCLK 4
#define TFT_MOSI 6
#define TFT_RST  7
#define TFT_DC   2
#define TFT_CS   10
Adafruit_ST7789 tft(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);

// Audio
#define I2S_DIN   20
#define I2S_BCLK  21
#define I2S_LRC   0
#define AMP_SD    5
#define I2S_PORT  I2S_NUM_0

// PCF8574
#define PCF_ADDR 0x20
#define I2C_SDA  8
#define I2C_SCL  9
#define BTN_UP    0
#define BTN_DOWN  1
#define BTN_LEFT  2
#define BTN_RIGHT 3
#define BTN_A     4
#define BTN_B     5
#define BTN_P6    6
#define IR_RX_P7  7

// IR + vibration
#define IR_TX_PIN 1
#define VIBE_PIN  3

uint8_t lastState = 0xFF;
bool pcfOK = false;
int logY = 116;
unsigned long lastIrMs = 0;

void logLine(const String &s, uint16_t color = ST77XX_WHITE) {
  Serial.println(s);
  if (logY > 264) {
    tft.fillRect(0, 112, 240, 168, ST77XX_BLACK);
    logY = 116;
  }
  tft.setTextSize(1);
  tft.setTextColor(color, ST77XX_BLACK);
  tft.setCursor(6, logY);
  tft.println(s);
  logY += 13;
}

void drawUI() {
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextSize(2);
  tft.setTextColor(ST77XX_CYAN);
  tft.setCursor(8, 8);
  tft.println("KEYCHAIN");
  tft.setCursor(8, 31);
  tft.println("KREATURES");

  tft.setTextSize(1);
  tft.setTextColor(ST77XX_WHITE);
  tft.setCursor(8, 60);
  tft.println("FACTORY TEST");

  tft.drawLine(0, 76, 239, 76, ST77XX_BLUE);
  tft.setCursor(8, 83);
  tft.setTextColor(ST77XX_ORANGE);
  tft.print("A = VIBRATE");
  tft.setCursor(112, 83);
  tft.setTextColor(ST77XX_MAGENTA);
  tft.print("B = IR TX");

  tft.setCursor(8, 99);
  tft.setTextColor(pcfOK ? ST77XX_GREEN : ST77XX_RED);
  tft.print(pcfOK ? "PCF8574 OK" : "PCF8574 FAIL");
}

bool detectPCF() {
  Wire.beginTransmission(PCF_ADDR);
  return Wire.endTransmission() == 0;
}

void releasePCFPins() {
  Wire.beginTransmission(PCF_ADDR);
  Wire.write(0xFF);
  Wire.endTransmission();
}

uint8_t readPCF() {
  Wire.requestFrom(PCF_ADDR, 1);
  return Wire.available() ? Wire.read() : 0xFF;
}

bool setupAudio() {
  pinMode(AMP_SD, OUTPUT);
  digitalWrite(AMP_SD, HIGH);

  i2s_config_t cfg = {
    .mode = i2s_mode_t(I2S_MODE_MASTER | I2S_MODE_TX),
    .sample_rate = 22050,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 128,
    .use_apll = false,
    .tx_desc_auto_clear = true,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pins = {
    .bck_io_num = I2S_BCLK,
    .ws_io_num = I2S_LRC,
    .data_out_num = I2S_DIN,
    .data_in_num = I2S_PIN_NO_CHANGE
  };

  esp_err_t e = i2s_driver_install(I2S_PORT, &cfg, 0, nullptr);
  if (e != ESP_OK && e != ESP_ERR_INVALID_STATE) return false;
  return i2s_set_pin(I2S_PORT, &pins) == ESP_OK;
}

void toneOut(int frequency, int durationMs, int amplitude = 15000) {
  const int sampleRate = 22050;
  const int framesTotal = sampleRate * durationMs / 1000;
  const int chunk = 64;
  int16_t buffer[chunk * 2];

  for (int made = 0; made < framesTotal; ) {
    int count = min(chunk, framesTotal - made);
    for (int i = 0; i < count; i++) {
      float phase = 2.0f * PI * frequency * (made + i) / sampleRate;
      int16_t sample = (int16_t)(sinf(phase) * amplitude);
      buffer[i * 2] = sample;
      buffer[i * 2 + 1] = sample;
    }
    size_t written = 0;
    i2s_write(I2S_PORT, buffer, count * 4, &written, portMAX_DELAY);
    made += count;
  }
}

void vibrate(unsigned long ms) {
  logLine("VIBRATOR ON", ST77XX_ORANGE);
  digitalWrite(VIBE_PIN, HIGH);
  delay(ms);
  digitalWrite(VIBE_PIN, LOW);
  logLine("VIBRATOR OFF", ST77XX_ORANGE);
}

void irMark(unsigned int us) {
  unsigned long start = micros();
  while ((unsigned long)(micros() - start) < us) {
    digitalWrite(IR_TX_PIN, HIGH);
    delayMicroseconds(13);
    digitalWrite(IR_TX_PIN, LOW);
    delayMicroseconds(13);
  }
}

void irSpace(unsigned int us) {
  digitalWrite(IR_TX_PIN, LOW);
  delayMicroseconds(us);
}

void sendIR() {
  logLine("IR TX START", ST77XX_MAGENTA);
  irMark(9000);
  irSpace(4500);
  for (int i = 0; i < 16; i++) {
    irMark(560);
    irSpace((i & 1) ? 1690 : 560);
  }
  irMark(560);
  digitalWrite(IR_TX_PIN, LOW);
  logLine("IR TX DONE", ST77XX_MAGENTA);
}

void handlePress(uint8_t pin) {
  static const int tones[7] = {520, 440, 600, 700, 820, 980, 300};

  switch (pin) {
    case BTN_UP:    logLine("BUTTON UP", ST77XX_YELLOW); break;
    case BTN_DOWN:  logLine("BUTTON DOWN", ST77XX_YELLOW); break;
    case BTN_LEFT:  logLine("BUTTON LEFT", ST77XX_YELLOW); break;
    case BTN_RIGHT: logLine("BUTTON RIGHT", ST77XX_YELLOW); break;
    case BTN_A:     logLine("BUTTON A", ST77XX_ORANGE); break;
    case BTN_B:     logLine("BUTTON B", ST77XX_MAGENTA); break;
    case BTN_P6:    logLine("PCF P6 ACTIVE", ST77XX_YELLOW); break;
  }

  toneOut(tones[pin], 70);

  if (pin == BTN_A) vibrate(300);
  if (pin == BTN_B) sendIR();
}

void processPCF(uint8_t state) {
  uint8_t changed = state ^ lastState;

  for (uint8_t pin = 0; pin <= 6; pin++) {
    if (bitRead(changed, pin) && bitRead(state, pin) == LOW) {
      handlePress(pin);
    }
  }

  if (bitRead(changed, IR_RX_P7) &&
      bitRead(state, IR_RX_P7) == LOW &&
      millis() - lastIrMs > 120) {
    lastIrMs = millis();
    logLine("IR RX ACTIVITY", ST77XX_GREEN);
    toneOut(350, 70);
    toneOut(700, 90);
  }

  lastState = state;
}

void setup() {
  Serial.begin(115200);
  delay(400);

  pinMode(VIBE_PIN, OUTPUT);
  digitalWrite(VIBE_PIN, LOW);

  pinMode(IR_TX_PIN, OUTPUT);
  digitalWrite(IR_TX_PIN, LOW);

  Wire.begin(I2C_SDA, I2C_SCL);
  Wire.setClock(100000);

  pcfOK = detectPCF();
  if (pcfOK) {
    releasePCFPins();
    delay(5);
    lastState = readPCF();
  }

  tft.init(240, 280);
  tft.setRotation(0);
  drawUI();

  bool audioOK = setupAudio();

  logLine("DISPLAY OK", ST77XX_GREEN);
  logLine(pcfOK ? "PCF8574 OK" : "PCF8574 FAIL",
          pcfOK ? ST77XX_GREEN : ST77XX_RED);
  logLine(audioOK ? "AUDIO TEST" : "AUDIO INIT FAIL",
          audioOK ? ST77XX_GREEN : ST77XX_RED);

  if (audioOK) {
    toneOut(440, 90);
    toneOut(660, 90);
    toneOut(880, 130);
  }

  vibrate(250);
  logLine("READY", ST77XX_CYAN);
}

void loop() {
  if (pcfOK) {
    processPCF(readPCF());
  }
  delay(2);
}