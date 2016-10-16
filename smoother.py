#!/usr/bin/env python

import time
from triggers import RandomTrigger

class Smoother:
    def __init__(self, trigger, size):
        self.trigger = trigger
        self.last = None
        self.buffer = [0 for i in range(size)]
        self.next = 0

    def update(self):
        sample = self.trigger.sample()

        if not sample == self.last:
            self.buffer[self.next] = 1
        else:
            self.buffer[self.next] = 0

        self.last = sample
        self.next = (self.next + 1) % len(self.buffer)
        
        return sum(self.buffer) / float(len(self.buffer))

if __name__ == '__main__':
    trigger = RandomTrigger(0.25, 0.5)
    smoother = Smoother(trigger, 10)
    while True:
        print smoother.update()
        time.sleep(0.1)

