
 #include "Arduino.h"
 #include <falldetectionradar.h>
 #include "FS.h"
 #include "SD.h"
 #include "SPI.h"

 #define SD_CS_PIN 5  
 #define MAX_SAMPLES 1000
 #define FILE_PATH "/radar_data.csv"

 FallDetectionRadar radar;
 int sampleCount = 0;
 bool sdInitialized = false;

 void setup() {
     Serial.begin(115200);
     radar.SerialInit();
     delay(1500);
    
     Serial.println("Initializing SD Card...");
     if (!SD.begin(SD_CS_PIN)) {
         Serial.println("SD Card initialization failed.");
         return;
     }

     Serial.println("SD Card initialized.");
     sdInitialized = true;

     if (!SD.exists(FILE_PATH)) {
         Serial.println("Creating new CSV file...");
         File file = SD.open(FILE_PATH, FILE_WRITE);
         if (file) {
             file.println("Sample No,Hex Data");  
             file.close();
         } else {
             Serial.println("Failed to create radar_data.csv");
             sdInitialized = false;
         }
     } else {
         Serial.println("CSV file exists. Appending data.");
     }

     Serial.println("Ready to record radar data.");
 }

 void loop() {
     if (!sdInitialized) {
         Serial.println("SD Card not initialized. Stopping data collection.");
         return; 
     }

     if (sampleCount >= MAX_SAMPLES) {
         Serial.println(" Max samples reached. Stopping.");
         return; 
     }

     radar.recvRadarBytes(); 

     if (radar.newData) {
         saveToCSV();
         radar.newData = false;
         sampleCount++;
     }
 }

 void saveToCSV() {
     if (!sdInitialized) return; 

     File file = SD.open(FILE_PATH, FILE_APPEND);
     if (!file) {
         Serial.println("Error opening radar_data.csv for writing.");
         return;
     }

     Serial.print("Saving Sample #");
     Serial.println(sampleCount + 1);

     String dataRow = String(sampleCount + 1) + ",";  
     dataRow += "55 ";  

     for (int i = 0; i < radar.dataLen; i++) {
         char hexStr[4];
         sprintf(hexStr, "%02X", radar.Msg[i]); 
         dataRow += hexStr;
         dataRow += " ";
     }

     file.println(dataRow);  
     file.close();  

 }
