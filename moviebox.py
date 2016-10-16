#!/usr/bin/env python

import time
from triggers import SchmittTrigger
#from triggers import RandomTrigger
from sources import NormalisedMCPChannel
from smoother import Smoother
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI

if __name__ == '__main__':
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0,0))
    source = NormalisedMCPChannel(mcp, 0)
    trigger = SchmittTrigger(0.45, 0.55, source)
    #trigger = RandomTrigger(0.1, 0.25)
    smoother = Smoother(trigger, 10)
    while True:
        print smoother.update()
        time.sleep(0.1)
