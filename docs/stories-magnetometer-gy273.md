# User Stories: Magnetometer (GY-273) Integration

## Story 1: As a developer, I want to connect the GY-273 magnetometer to the Pico via I2C so that I can read magnetic field data

- **Acceptance Criteria:**
  - The Pico can detect the GY-273 on the I2C bus.
  - Communication errors are logged and handled.

## Story 2: As a developer, I want to read X, Y, Z magnetic field data from the GY-273 so that I can use it for heading calculation

- **Acceptance Criteria:**
  - Raw sensor data is read and output for debugging.
  - Data is available at a regular interval (e.g., 10Hz).

## Story 3: As a developer, I want to calculate heading from the magnetometer data so that the drone can determine its orientation

- **Acceptance Criteria:**
  - Heading is calculated from X, Y, Z data.
  - Heading is output and available for flight control.

## Story 4: As a developer, I want to handle sensor errors gracefully so that the flight computer remains robust

- **Acceptance Criteria:**
  - Sensor read failures do not crash the system.
  - Errors are logged and retried.
