#    This maneges the interface of and provides functionality for the 
#    "Quality" tab.

import interface
import cameramic

TAB_NAME = "Quality"
WIDGET_NAME = "data_quality"


class Tab(interface.NewTab):
    def make(self):
        # change these to glade callbacks later.
        self.video, self.audio, self.image, self.lapse, self.width, self.height, self.rate = 4, 4, 4, 4, 100, 75, 12000

    def on_video_changed(self, widget):
        self.video = widget.get_value()
        print "video quality", self.video
	if self.video < 1.50:
		self.width = 100
		self.height = 75
	if self.video >= 1.50 and self.video < 2.50:
		self.width = 200
		self.height = 150
		print "optimal"
	if self.video >= 2.50 and self.video < 3.50:
		self.width = 256
		self.height = 192
	if self.video >= 3.50 and self.video < 4.50:
		self.width = 320
		self.height = 240
	if self.video >= 4.50 and self.video < 5.50:
		self.width = 400
		self.width = 300
	if self.video >= 5.50 and self.video <= 6.00:
		self.width = 512
		self.height = 384

    def on_audio_changed(self, widget):
        self.audio = widget.get_value()        
	print "audio quality", self.audio
	if self.audio < 1.50:
		self.rate = 12000
	if self.audio >= 1.50 and self.video < 2.50:
		self.rate = 18000
	if self.audio >= 2.50 and self.video < 3.50:
		self.rate = 24000
	if self.audio >= 3.50 and self.video < 4.50:
		self.rate = 30000
	if self.audio >= 4.50 and self.video < 5.50:
		self.rate = 36000
	if self.audio >= 5.50 and self.video <= 6.00:
		self.rate = 48000

tab = Tab(interface.GLADE_TABS, WIDGET_NAME, TAB_NAME)
