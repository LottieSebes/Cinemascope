#!/usr/bin/env python

import ctypes
import vlc
import sys
import smoother
import triggers
from Tkinter import Tk, Frame, BOTH

class TkScope(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="black")   
         
        self.paused = False
        self.parent = parent
        self.parent.attributes("-fullscreen", True)
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.loop_it, self)

        self.pack(fill=BOTH, expand=1)

        self.parent.bind("q", lambda e: self.parent.destroy())

    def restart(self):
        print "Playing..."
        self.player.stop()
        self.player.play()

    def set_rate(self, rate):
        if rate <= 0.5:
            if not self.paused:
                self.player.pause()
                self.paused = True
                print "Paused..."
        else:
            if self.paused:
                self.player.play()
                self.paused = False
                print "Unpaused..."
            self.player.set_rate(rate)

    @vlc.callbackmethod
    def loop_it(self, event, player):
        self.parent.after(0, lambda: self.restart())

    def open(self, path):
        self.media = self.instance.media_new(path)
        self.player.set_media(self.media)
        self.player.set_xwindow(self.winfo_id())
        self.player.play()
        self.set_rate(0.0)
        
def start_smoother(root, period, smoother):
    root.after(period, lambda: update_smoother(root, period, smoother))

def update_smoother(root, period, smoother):
    smoother.update()
    start_smoother(root, period, smoother)

def start_rate(root, period, player, smoother):
    root.after(period, lambda: update_rate(root, period, player, smoother))

def update_rate(root, period, player, smoother):
    x = smoother.sample() * 1.5 + 0.5
    print("rate: {}".format(x))
    player.set_rate(x)
    start_rate(root, period, player, smoother)

if __name__ == '__main__':
    x11 = ctypes.cdll.LoadLibrary('libX11.so')
    x11.XInitThreads()

    root = Tk()
    root.geometry('{}x{}'.format(1280, 800))
    root.config(cursor='none')

    trigger = triggers.RandomSineTrigger(5)
    smoother = smoother.Smoother(trigger, 10)

    player = TkScope(root)
    player.open(sys.argv[1])

    start_smoother(root, 50, smoother)
    start_rate(root, 200, player, smoother)

    root.mainloop()
