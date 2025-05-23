

# Physical Parameters Monitoring using 24GHz FMCW Radar

This Arduino-based project captures physical parameters such as presence, motion, and potential breathing activity using a 24GHz FMCW radar module. It is built using the `FallDetectionRadar' library and is designed for use in applications like non-contact sleep monitoring or human presence detection.

---

## Features

- Detects human presence and motion using radar
- Outputs raw and processed radar data over Serial
- Can be integrated into systems for sleep monitoring or indoor safety

---

## Repository Structure

```

├── physical\_parameters\_mmhg.ino     # Main Arduino sketch
├── falldetectionradar.h             # Radar module interface header
├── falldetectionradar.cpp           # Radar communication and processing logic
└── README.md                        # Project documentation

````

---

## Hardware Requirements

- **24GHz FMCW Radar Module** (e.g., Human Static Presence Radar)
- **Arduino UNO / ESP32 / Compatible MCU**
- USB cable for flashing and Serial monitoring

---

## Software Requirements

- [Arduino IDE](https://www.arduino.cc/en/software) (version >= 1.8.0)
- Compatible board drivers (e.g., for ESP32)
- Serial Monitor (built-in or external)

---

## Getting Started

### 1. Download physical_parameters

### 2. Open the Project

* Open `physical_parameters.ino` in the Arduino IDE.

### 3. Connect Your Radar

* Connect the radar module TX/RX to the board’s UART (e.g., D2 and D3 or Serial2 for ESP32).
* Power the radar module as per its datasheet (commonly 5V or 3.3V depending on model).

### 4. Upload the Code

* Select the correct board and port in **Tools > Board** and **Tools > Port**
* Click the **Upload** button

---

## Output

The radar sends interpreted data over Serial. You can view the output using:

* Arduino Serial Monitor
* Python scripts for data logging (optional)

Expected output format (example):

```
Radar Initialized
Human Detected: TRUE
Motion Level: LOW
Breathing Detected: TRUE
```

---

## How it Works

The `FallDetectionRadar` class handles:

* Radar initialization and serial parsing
* Data buffer extraction
* saving Raw data


---

