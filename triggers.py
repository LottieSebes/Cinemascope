#!/usr/bin/env python

import time
import datetime
import random
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
from sources import NormalisedMCPChannel

class RandomTrigger:
    def __init__(self, min_delta, max_delta, state='L'):
        self.state = state

        self.min_delta = min_delta
        self.max_delta = max_delta

        self.generate_next_event()

    def generate_next_event(self):
        delta = random.uniform(self.min_delta, self.max_delta)
        self.next_event = datetime.datetime.now() + datetime.timedelta(seconds=delta)

    def transition(self):
        if self.state == 'L':
            self.state = 'H'
            transition = 'R'
        else:
            self.state = 'L'
            transition = 'F'
        return transition

    def sample(self):
        if datetime.datetime.now() > self.next_event:
            self.generate_next_event()
            return self.transition()
        return self.state

class SchmittTrigger:
    def __init__(self, lower_threshold, upper_threshold, source):
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.source = source

        midpoint = (self.upper_threshold + self.lower_threshold) / 2
        level = self.source.sample()
        if level < midpoint:
            self.state = 'L'
        else:
            self.state = 'H'

    def transition(self):
        if self.state == 'L':
            self.state = 'H'
            transition = 'R'
        else:
            self.state = 'L'
            transition = 'F'
        return transition

    def sample(self):
        level = self.source.sample()
        if self.state == 'L' and level >= self.upper_threshold:
            return self.transition()
        elif self.state == 'H' and level <= self.lower_threshold:
            return self.transition()
        return self.state

if __name__ == '__main__':
    #epoch = datetime.datetime.now()
    #trigger = RandomTrigger(1, 2)
    #for t in range(20):
    #    delta = datetime.datetime.now() - epoch
    #    print('{0} {1}'.format(delta.total_seconds(), trigger.sample()))
    #    time.sleep(0.3333)

    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0,0))
    source = NormalisedMCPChannel(mcp, 0)
    trigger = SchmittTrigger(0.25, 0.75, source)
    while True:
        print('{0}'.format(trigger.sample()))
        time.sleep(1.0)
