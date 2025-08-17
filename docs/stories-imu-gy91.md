# User Stories: IMU (GY-91) Integration

## Story 1: As a developer, I want to connect the GY-91 IMU to the Pico via I2C so that I can read sensor data

- **Acceptance Criteria:**
  - The Pico can detect the GY-91 on the I2C bus.
  - Communication errors are logged and handled.


## Story 2: As a developer, I want to read acceleration, gyroscope, and temperature data from the GY-91 so that I can use it for flight stabilization

- **Acceptance Criteria:**
  - Raw sensor data is read and output for debugging.
  - Data is available at a regular interval (e.g., 10Hz).


## Story 3: As a developer, I want to process IMU data using a Madgwick filter so that I can obtain orientation (pitch and roll)

- **Acceptance Criteria:**
  - The Madgwick filter is implemented and tested with sample data.
  - Orientation data is output and available for flight control.


## Story 4: As a developer, I want to handle sensor errors gracefully so that the flight computer remains robust

- **Acceptance Criteria:**
  - Sensor read failures do not crash the system.
  - Errors are logged and retried.


---

Each story will be tracked as a separate issue in GitHub with the 'story' label.
