# Python module for control of Awox Smart bulb
# Copyright 2017 Mika Benoit <mika.benoit[at]gmail.com>
#
# This code is released under the terms of the Apache 2.0 License. See the LICENSE
# file for more details.
import struct
import time

from bluepy import btle


class awoxAroma:
    def __init__(self, mac):
        self.mac = mac
        self.color_mode = False
        self.set_state(0, 0, 0, 0, 0, 0, False)

    def set_state(self, white, whiteBrightness, red, green, blue, colourBrightness, power):
        self.white = white
        self.whiteBrightness = whiteBrightness
        self.red = red
        self.green = green
        self.blue = blue
        self.colourBrightness = colourBrightness
        self.power = power

    def connect(self):
        try:
            try:
                self.device = btle.Peripheral(self.mac, addrType=btle.ADDR_TYPE_PUBLIC)
            except btle.BTLEException as inst:
                print(inst)
                btle.Scanner().scan(10)
                self.device = btle.Peripheral(self.mac, addrType=btle.ADDR_TYPE_PUBLIC)

            handles = self.device.getCharacteristics()
            for handle in handles:
                if handle.uuid == "217887f8-0af2-40029c05-24c9ecf71600":
                    self.statehandle = handle
                if handle.uuid == "74532143-fff1-460d-8e8a-370f934d40be":
                    self.rgbhandle = handle
                if handle.uuid == "5b430c99-cb06-4c66-be2c-b538acfd1961":
                    self.whitehandle = handle  # From 0x00 to 0x7F
                if handle.uuid == "1c537b0a-4eaa-4e19-b98c-eaaa5bcd9bc9":
                    self.rgbBrightnessHandle = handle  # From 0x00 to 0x64
                if handle.uuid == "d8da934c-3d8f-4bdf-9230-f61295b69570":
                    self.whiteBrightnessHandle = handle  # From 0x00 to 0x73
                if handle.uuid == "9e926da7-cffa-47f5-8d4b-7e82aff1a02a":
                    self.lightMode = handle  # 0x00 for White mode and 0x01 for color mode

            self.get_state()
            return True
        except btle.BTLEException as inst:
            print(inst)
            return False

    def send_packet(self, handle, data):
        initial = time.time()
        while True:
            if time.time() - initial >= 10:
                return False
            try:
                return handle.write(bytes(data), withResponse=True)
            except:
                self.connect()

    def read(self, handle):
        initial = time.time()
        while True:
            if time.time() - initial >= 10:
                return 0
            try:
                return handle.read()
            except:
                self.connect()

    def off(self):
        self.power = False
        packet = bytearray([0x00])
        self.send_packet(self.statehandle, packet)

    def on(self):
        self.power = True
        packet = bytearray([0x01])
        self.send_packet(self.statehandle, packet)

    def set_rgb(self, red, green, blue):
        self.color_mode = True
        self.red = red
        self.green = green
        self.blue = blue
        packet = bytearray([red, green, blue])
        self.send_packet(self.rgbhandle, packet)

    def set_white(self, white):
        self.color_mode = False
        self.white = white
        if type(white) == bytes:
            packet = [white]
        else:
            packet = bytearray([white])
        self.send_packet(self.whitehandle, packet)

    def set_white_brightness(self, brightness):
        self.color_mode = False
        self.whiteBrightness = brightness
        packet = bytearray([brightness])
        self.send_packet(self.whiteBrightnessHandle, packet)

    def set_colour_brightness(self, brightness):
        self.color_mode = True
        self.colourBrightness = brightness
        packet = bytearray([brightness])
        self.send_packet(self.rgbBrightnessHandle, packet)

    def get_state(self):
        readed = self.read(self.statehandle)
        if readed == 0x00:
            self.power = False
        elif readed == 0x01:
            self.power = True

        readed = self.read(self.rgbhandle)
        self.red = struct.unpack("H", "\x00" + readed[0])[0]
        self.green = struct.unpack("H", "\x00" + readed[1])[0]
        self.blue = struct.unpack("H", "\x00" + readed[2])[0]

        readed = self.read(self.rgbBrightnessHandle)
        self.colourBrightness = readed

        readed = self.read(self.whitehandle)
        self.white = readed

        readed = self.read(self.whiteBrightnessHandle)
        self.whiteBrightness = readed

    def get_on(self):
        return self.power

    def get_colour(self):

        return (int(self.red), int(self.green), int(self.blue))

    def get_colour_brightness(self):
        if type(self.colourBrightness) == int:
            return self.colourBrightness
        else:
            return ord(self.colourBrightness)

    def get_white(self):
        return self.white

    def get_white_brightness(self):
        if type(self.whiteBrightness) == int:
            return self.whiteBrightness
        else:
            return ord(self.whiteBrightness)

    def get_brightness(self):
        if self.color_mode:
            return self.get_colour_brightness()
        else:
            return self.get_white_brightness()

    def set_brightness(self, brightness):
        if self.color_mode:
            self.set_colour_brightness(brightness)
        else:
            self.set_white_brightness(brightness)
