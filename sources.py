#!/usr/bin/env python

import time
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI

class NormalisedMCPSource:
    def __init__(self, mcp, multiplier = 1.0 / 1024.0):
        self.mcp = mcp
        self.multiplier = multiplier

    def sample_channel(self, channel):
        return self.multiplier * self.mcp.read_adc(channel)

class NormalisedMCPChannel:
    def __init__(self, mcp, channel, multiplier = 1.0 / 1024.0):
        self.mcp = mcp
        self.channel = channel
        self.multiplier = multiplier

    def update_channel(self, channel):
        self.channel = channel

    def sample(self):
        return self.multiplier * self.mcp.read_adc(self.channel)

if __name__ == '__main__':
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0,0))
    source = NormalisedMCPChannel(mcp, 0)
    while True:
        print('{0}'.format(source.sample()))
        time.sleep(0.25)
