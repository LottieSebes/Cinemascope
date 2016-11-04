#!/usr/bin/env python

import time
from triggers import RandomSineTrigger

class Smoother:
    def __init__(self, trigger, size):
        self.trigger = trigger
        self.last = None
        self.buffer = [0 for i in range(size)]
        self.next = 0
        self.cached = 0

    def sample(self):
        return self.cached

    def update(self):
        sample = self.trigger.sample()

        if not sample == self.last:
            self.buffer[self.next] = 1
        else:
            self.buffer[self.next] = 0

        self.last = sample
        self.next = (self.next + 1) % len(self.buffer)
        self.cached = sum(self.buffer) / float(len(self.buffer))
        
        return self.cached

if __name__ == '__main__':
    trigger = RandomSineTrigger(2)
    smoother = Smoother(trigger, 20)
    while True:
        print smoother.update()
        time.sleep(0.1)

