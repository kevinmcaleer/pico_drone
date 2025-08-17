import machine
import aioble
import asyncio
from micropython import const
import bluetooth
from time import ticks_ms, ticks_diff
from ssd1306 import SSD1306_I2C
from machine import I2C

# Pinouts
A_BUTTON = 6
B_BUTTON = 7
X_BUTTON = 4
Y_BUTTON = 5
UP_BUTTON = 8
DOWN_BUTTON = 9
LEFT_BUTTON = 2
RIGHT_BUTTON = 3
START_BUTTON = 12
SELECT_BUTTON = 11
MENU_BUTTON = 10

class Button:
    def __init__(self, pin: int, debounce_ms: int = 50):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.debounce_ms = debounce_ms
        self._last_pressed = ticks_ms()
        self._was_pressed = False

    async def is_pressed(self) -> bool:
        current_time = ticks_ms()
        if self.pin.value() == 0:  # Button is pressed
            if ticks_diff(current_time, self._last_pressed) > self.debounce_ms:
                self._last_pressed = current_time
                return True
        return False

    async def state_changed(self) -> tuple[bool, bool]:
        """Check for button press/release events."""
        is_pressed = self.pin.value() == 0
        if is_pressed and not self._was_pressed:  # Button down
            self._was_pressed = True
            return True, False
        elif not is_pressed and self._was_pressed:  # Button up
            self._was_pressed = False
            return False, True
        return False, False

class GamePad:
    
    def __init__(self):
        """ Initialise the GamePad """
        self.buttons = {
            "A": Button(6),
            "B": Button(7),
            "X": Button(4),
            "Y": Button(5),
            "Up": Button(8),
            "Down": Button(9),
            "Left": Button(2),
            "Right": Button(3),
            "Start": Button(12),
            "Select": Button(11),
            "Menu": Button(10),
        }
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.connected = False
        self.connection = None

        # UUIDs and constants
        self._GENERIC_UUID = bluetooth.UUID(0x1848)
        self._BUTTON_UUID = bluetooth.UUID(0x2A6E)

        # BLE Service and Characteristic
        self.device_info = aioble.Service(self._GENERIC_UUID)
        self.button_characteristic = aioble.Characteristic(
            self.device_info,
            self._BUTTON_UUID,
            read=True,
            notify=True,
        )

        # Register the service
        aioble.register_services(self.device_info)

        # Setup OLED
        id = 0
        sda = 0
        scl = 1
        i2c = I2C(sda=sda, scl=scl, id=id)
        self.oled = SSD1306_I2C(128, 64, i2c)
        self.oled.text("GamePad", 0, 0)
        self.oled.show()

        print("GamePad initialized")

    async def monitor_buttons(self):
        """Continuously check button states asynchronously."""
        while True:
            for name, button in self.buttons.items():
                button_down, button_up = await button.state_changed()
                connected_text = 'Connected' if self.connected else 'Disconnected'
                if button_down:
                    print(f"Button {name} pressed down")
                    self.oled.fill(0)
                    self.oled.text(f"{name} down", 0, 0)                 
                    self.oled.text(f"{connected_text}",0,40)
                    self.oled.show()
                    if self.connected:
                        # Send button press notification
                        self.button_characteristic.write(f"{name}_down".encode())
                        self.button_characteristic.notify(self.connection)
                elif button_up:
                    print(f"Button {name} released")
                    self.oled.fill(0)
                    self.oled.text(f"{name} up", 0, 0)
                    self.oled.text(f"{connected_text}",0,40)
                    self.oled.show()
                    if self.connected:
                        # Send button release notification
                        self.button_characteristic.write(f"{name}_up".encode())
                        self.button_characteristic.notify(self.connection)
            await asyncio.sleep_ms(10)

    async def peripheral_task(self):
        """Handle BLE advertising and connections."""
        print("Peripheral task started")
        while True:
            self.connected = False
            async with await aioble.advertise(
                250_000,
                name="KevsRobots",
                services=[self._GENERIC_UUID],
            ) as self.connection:
                self.oled.clear()
                self.oled.text(f"Connected.",0,40)
                self.oled.show()
                print("Connection from", self.connection.device)
                self.connected = True
                
                await self.connection.disconnected()
                self.oled.clear()
                self.oled.text(f"Disconnected.",0,40)
                self.oled.show()
                print("Disconnected")

    async def blink_task(self):
        """Blink the LED to indicate connection status."""
        print("Blink task started")
        while True:
            self.led.toggle()
            blink_interval = 250 if not self.connected else 1000
            await asyncio.sleep_ms(blink_interval)

    async def main(self):
        """Run all tasks concurrently."""
        tasks = [
            asyncio.create_task(self.peripheral_task()),
            asyncio.create_task(self.blink_task()),
            asyncio.create_task(self.monitor_buttons()),
        ]
        await asyncio.gather(*tasks)

    def begin(self):
        """Start the gamepad."""
        print("GamePad starting")
        asyncio.run(self.main())


class GamePadServer:
    """
    A class to handle BLE communication and interpret commands from a Bluetooth gamepad remote.

    Attributes:
        device_name (str): The name of the BLE device.
        led (Pin): Onboard LED for connection status indication.
        connected (bool): Tracks the connection status.
        connection (aioble.Connection): Active BLE connection.
        command (str): The last received command from the gamepad.
    """

    def __init__(self, device_name="KevsRobots"):
        """
        Initializes the BLE server with the specified device name.

        Args:
            device_name (str): The name of the BLE device to advertise.
        """
#         import aioble
#         import bluetooth
#         from micropython import const

        self.device_name = device_name
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.connected = False
        self.connection = None
        self.command = None
        self.tasks = []

        # UUIDs and constants
        self._REMOTE_UUID = bluetooth.UUID(0x1848)
        self._BUTTON_UUID = bluetooth.UUID(0x2A6E)
        self._BLE_APPEARANCE_GENERIC_REMOTE_CONTROL = const(384)

        # Services and Characteristics
        self.remote_service = aioble.Service(self._REMOTE_UUID)
        self.button_characteristic = aioble.Characteristic(
            self.remote_service, self._BUTTON_UUID, read=True, notify=True
        )

        # Register the services
        aioble.register_services(self.remote_service)
        
    async def peripheral_task(self):
        print("Peripheral task started")
        while True:
            device = await self.find_remote()
            if not device:
                print("Remote not found, retrying...")
                continue

            try:
                print(f"Connecting to {device}...")
                self.connection = await device.connect()
                self.connected = True
                print(f"Connected to {self.connection.device}")

                # Keep connection active until disconnected
                async with self.connection:
                    await self.connection.disconnected()
                    print("Disconnected from remote.")
            except Exception as e:
                print(f"Error during connection: {e}")
            finally:
                self.connected = False
                await asyncio.sleep(2)  # Avoid aggressive reconnection retries

        
    async def blink_task(self):
        print('blink task started')
        toggle = True
        while True:
            self.led.value(toggle)
            toggle = not toggle
            blink = 1000
            if self.connected:
                blink = 1000
            else:
                blink = 250
            await asyncio.sleep_ms(blink)

    async def read_commands(self):
        print("Waiting for notifications...")
        service = None
        characteristic = None

        while True:
            if self.connected:
                try:
                    # Discover service and characteristic once
                    if not service or not characteristic:
                        service = await self.connection.service(self._REMOTE_UUID)
                        characteristic = await service.characteristic(self._BUTTON_UUID)

                    # Wait for notifications
                    while self.connected:
                        value = await characteristic.read()
                        if value:
                            self.command = value.decode("utf-8").strip().lower()
#                             print(f"Received command: {self.command}")
                except Exception as e:
                    print(f"Error during notification handling: {e}")
                    self.connected = False
                    service = None
                    characteristic = None
            else:
                await asyncio.sleep(1)

    @property
    def is_up(self):
        return self.command == "up_down"

    @property
    def is_down(self):
        return self.command == "down_down"

    @property
    def is_left(self):
        return self.command == "left_down"

    @property
    def is_right(self):
        return self.command == "right_down"

    @property
    def is_a(self):
        return self.command == "a_down"

    @property
    def is_b(self):
        return self.command == "b_down"
    
    @property
    def is_x(self):
        return self.command == "x_down"
    
    @property
    def is_y(self):
        return self.command == "y_down"
    
    @property
    def is_menu(self):
        return self.command == "menu_down"
    
    @property
    def is_start(self):
        return self.command == "start_down"

    @property
    def is_select(self):
        return self.command == "select_down"
            
    async def find_remote(self):
        print("Scanning for BLE devices...")
        while True:
            async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
                async for result in scanner:
                    if result.name() == self.device_name:
                        print(f"Found {self.device_name}")
                        return result.device  # Return the device for direct connection
            print("Device not found. Retrying in 2 seconds...")
            await asyncio.sleep(2)

    
    async def main(self):
        while True:
            """ Run all tasks concurrently """
            
            print('starting tasks')
            try:
                read_commands_task = asyncio.create_task(self.read_commands())
                peripheral_task = asyncio.create_task(self.peripheral_task())
                
                self.tasks.append(peripheral_task)
                self.tasks.append(read_commands_task)
                await asyncio.gather(*self.tasks)
            except Exception as e:
                print(f"Error in main task: {e}")
                for task in self.tasks:
                    task.cancel()

