#!/usr/bin/env python

import vlc
import sys
from Tkinter import Tk, Frame, BOTH

class TkScope(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="black")   
         
        self.parent = parent
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
        self.player.set_rate(rate)
        self.parent.after(5000, lambda: self.set_rate(1.5))

    @vlc.callbackmethod
    def loop_it(self, event, player):
        self.parent.after(0, lambda: self.restart())

    def open(self, path):
        self.media = self.instance.media_new(path)
        self.player.set_media(self.media)
        self.player.set_xwindow(self.winfo_id())
        self.player.play()
        
if __name__ == '__main__':
    root = Tk()

    player = TkScope(root)
    player.open(sys.argv[1])
    root.after(5000, lambda: player.set_rate(0.1))

    root.mainloop()
