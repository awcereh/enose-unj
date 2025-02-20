#include <DHT.h>

#define DHTPIN 5       // Pin yang digunakan untuk koneksi sensor DHT11
#define DHTTYPE DHT11  // Tipe sensor DHT yang digunakan

// Definisi pin untuk sensor MQ
#define MQ2pin A0
#define MQ3pin A1
#define MQ4pin A2
#define MQ5pin A3
#define MQ6pin A4
#define MQ7pin A5
#define MQ8pin A6
#define MQ9pin A7
#define MQ135pin A8

DHT dht(DHTPIN, DHTTYPE);  // Inisialisasi objek DHT

const int pinPompa1 = 2;
const int pinPompa2 = 3;
const int pinPompa3 = 4;

bool kondisiSelesai = false;  // Variabel untuk menandai apakah kondisi telah selesai atau belum

void setup() {
    // Inisialisasi pin sebagai input atau output
    pinMode(MQ2pin, INPUT);
    pinMode(MQ3pin, INPUT);
    pinMode(MQ4pin, INPUT);
    pinMode(MQ5pin, INPUT);
    pinMode(MQ6pin, INPUT);
    pinMode(MQ7pin, INPUT);
    pinMode(MQ8pin, INPUT);
    pinMode(MQ9pin, INPUT);
    pinMode(MQ135pin, INPUT);
    pinMode(pinPompa1, OUTPUT);
    pinMode(pinPompa2, OUTPUT);
    pinMode(pinPompa3, OUTPUT);

    // Atur semua pompa ke HIGH (mati)
    digitalWrite(pinPompa1, HIGH);
    digitalWrite(pinPompa2, HIGH);
    digitalWrite(pinPompa3, HIGH);

    // Mulai komunikasi serial dan inisialisasi sensor DHT
    dht.begin();
    Serial.begin(9600);
}

void loop() {
    // Mengecek apakah ada input dari serial dan apakah kondisi belum selesai
    if (!kondisiSelesai && Serial.available() > 0) {
        // Membaca kondisi dari input serial
        int kondisi = Serial.parseInt();
        
        if (kondisi == 0) {
            // Membaca durasi baseline, sampel, dan purging dari input serial
            int durDel = Serial.parseInt();
            int durSamp = Serial.parseInt();
            int durPur = Serial.parseInt();

            // Proses baseline
            digitalWrite(pinPompa1, LOW);
            delay(100);
            digitalWrite(pinPompa2, HIGH);
            digitalWrite(pinPompa3, LOW);
            delay(25000);
            
            int n_base = durDel * 10;
            for (int i = 0; i < n_base; i++) {
                readAndPrintSensorData();
                delay(100);
            }

            // Proses sampel
            digitalWrite(pinPompa1, HIGH);
            delay(100);
            digitalWrite(pinPompa2, LOW);
            digitalWrite(pinPompa3, HIGH);
            int n_samp = durSamp * 10;
            for (int i = 0; i < n_samp; i++) {
                readAndPrintSensorData();
                delay(100);
            }

            // Proses purging
            digitalWrite(pinPompa1, LOW);
            delay(100);
            digitalWrite(pinPompa2, HIGH);
            digitalWrite(pinPompa3, LOW);
            int n_purg = durPur * 10;
            for (int i = 0; i < n_purg; i++) {
                readAndPrintSensorData();
                delay(100);
            }
            
            kondisiSelesai = true; // Setelah kondisi 0 selesai, tandai sebagai selesai
        } else if (kondisi == 1) {
            // Proses pembersihan E-Nose
            digitalWrite(pinPompa3, LOW);
            digitalWrite(pinPompa2, HIGH);
            delay(100);
            digitalWrite(pinPompa1, LOW);
            delay(10000);
            digitalWrite(pinPompa1, HIGH);
            digitalWrite(pinPompa2, HIGH);
            digitalWrite(pinPompa3, HIGH);
            
            kondisiSelesai = true; // Setelah kondisi 1 selesai, tandai sebagai selesai
        }
    }

    if (kondisiSelesai && Serial.available() > 0) {
        // Mengizinkan masukan kondisi baru setelah kondisi sebelumnya selesai
        kondisiSelesai = false;
    }
}

void readAndPrintSensorData() {
    // Membaca nilai dari sensor MQ
    float mq2Value = analogRead(MQ2pin);
    float mq3Value = analogRead(MQ3pin);
    float mq4Value = analogRead(MQ4pin);
    float mq5Value = analogRead(MQ5pin);
    float mq6Value = analogRead(MQ6pin);
    float mq7Value = analogRead(MQ7pin);
    float mq8Value = analogRead(MQ8pin);
    float mq9Value = analogRead(MQ9pin);
    float mq135Value = analogRead(MQ135pin);
    
    // Membaca nilai suhu dan kelembapan dari sensor DHT
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    // Mengirimkan nilai sensor ke serial
    Serial.print(mq2Value);
    Serial.print(",");
    Serial.print(mq3Value);
    Serial.print(",");
    Serial.print(mq4Value);
    Serial.print(",");
    Serial.print(mq5Value);
    Serial.print(",");
    Serial.print(mq6Value);
    Serial.print(",");
    Serial.print(mq7Value);
    Serial.print(",");
    Serial.print(mq8Value);
    Serial.print(",");
    Serial.print(mq9Value);
    Serial.print(",");
    Serial.print(mq135Value);
    Serial.print(",");
    Serial.print(temperature);
    Serial.print(",");
    Serial.println(humidity);
}
