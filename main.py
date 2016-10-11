#!/usr/bin/env python

import pygame
import time
from pygame.locals import *

# picture display size
width = 1280
height = 800

windowSurfaceObj = pygame.display.set_mode((width,height))
pygame.display.set_caption('picture')

image_queue = list()

# Do producer-consumer pattern:
# producer process ensures image queue constantly has 150 images indefinitely,
# keeping track of the last loaded image, wrapping around when last frame of video loaded
# consumer process takes frames off the queue at a variable rate, but no faster than
# half of the frames in the queue per second - may need to tweak max queue size, max speed

# e.g. http://www.bogotobogo.com/python/Multithread/python_multithreading_Synchronization_Producer_Consumer_using_Queue.php
# e.g. https://docs.python.org/3/library/queue.html
# e.g. https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem

pygame.display.toggle_fullscreen()

# VERY early producer code
i = 1
while i <= 150:
  filename = "frame" + "%03d" % (i,) + ".png"
  image_queue.append(pygame.image.load("frames_projector/" + filename))
  i += 1

# VERY early consumer code
current_time_milliseconds = 0
frame_duration_milliseconds = 40
while image_queue:
  # Change this to instead of waiting n ms, track how much time has passed
  if (current_time_milliseconds == 0) or (int(round(time.time() * 1000)) - current_time_milliseconds >= frame_duration_milliseconds):
    current_time_milliseconds = int(round(time.time() * 1000))
    windowSurfaceObj.blit(image_queue.pop(0),(0,0))
    pygame.display.update()
    # maybe refactor to record time again here and then do time.sleep(remainder to reach 40 ms)
    # time.sleep should block until it's time again, freeing CPU for producer to run... assuming time.sleep works as i think
  
