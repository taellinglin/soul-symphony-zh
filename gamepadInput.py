
from panda3d.core import InputDevice



    
class GamepadInput:
    def __init__(self):
        self.gamepad = None

        devices = base.devices.getDevices(InputDevice.DeviceClass.gamepad)

        if devices:
            print(str(devices))

            self.connect(devices[0])

        base.accept("connect-device", self.connect)

        base.accept("disconnect-device", self.disconnect)

    def connect(self, device):
        """Event handler that is called when a device is discovered."""

        # We're only interested if this is a gamepad and we don't have a

        # gamepad yet.

        if device.device_class == InputDevice.DeviceClass.gamepad and not self.gamepad:
            print("Found %s" % (device))

            self.gamepad = device

            # Enable this device to ShowBase so that we can receive events.

            # We set up the events with a prefix of "gamepad-".

            if not (self.gamepad == None):
                base.attachInputDevice(device, prefix="gamepad")

    def disconnect(self, device):
        """Event handler that is called when a device is removed."""

        if self.gamepad != device:
            # We don't care since it's not our gamepad.

            return

        # Tell ShowBase that the device is no longer needed.

        print("Disconnected %s" % (device))

        base.detachInputDevice(device)

        self.gamepad = None

        # Do we have any other gamepads?  Attach the first other gamepad.

        devices = base.devices.getDevices(InputDevice.DeviceClass.gamepad)

        if devices:
            self.connect(devices[0])