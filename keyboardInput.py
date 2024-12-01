from panda3d.core import InputDevice


class KeyboardInput:
    def __init__(self):
        self.keyboard = None

        # Get all connected keyboard devices

        devices = base.devices.getDevices(InputDevice.DeviceClass.keyboard)

        if devices:
            print("Connected keyboards: " + str(devices))

            self.connect(devices[0])  # Connect the first available keyboard

        # Listen for connect/disconnect events

        base.accept("connect-device", self.connect)

        base.accept("disconnect-device", self.disconnect)

    def connect(self, device):
        """Event handler that is called when a device is discovered."""

        # We're only interested in keyboard devices and only if we don't have one yet

        if (
            device.device_class == InputDevice.DeviceClass.keyboard
            and not self.keyboard
        ):
            print("Connected to keyboard: %s" % device)

            self.keyboard = device

            # Enable this device in ShowBase to receive events

            # We set up the events with a prefix of "keyboard-".

            base.attachInputDevice(device, prefix="keyboard")

    def disconnect(self, device):
        """Event handler that is called when a device is removed."""

        if self.keyboard != device:
            # If this is not our keyboard, ignore it

            return

        # Remove this device from ShowBase's active devices

        print("Disconnected keyboard: %s" % device)

        base.detachInputDevice(device)

        self.keyboard = None

        # Check for other available keyboards and attach the first one if available

        devices = base.devices.getDevices(InputDevice.DeviceClass.keyboard)

        if devices:
            self.connect(devices[0])
