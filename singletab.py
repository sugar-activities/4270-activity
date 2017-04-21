#    This maneges the interface of and provides functionality for the 
#    "Single Collection" tab.

import interface
import collectdata

TAB_NAME = "Single Collection"
WIDGET_NAME = "single_collection"


class Tab(interface.NewTab):
    def make(self):
        self.duration = 15
        self.jurnal_name = self.interface.get_widget('single_name').get_text()
    def set_canvas(self, canvas):
        self.canvas = canvas
     
        
    def on_collect_pushed(self, widget):
        print "collect pushed"
        self.collection = collectdata.Single(self)
        #self.canvas.addEvent()
        
    def on_name_changed(self, widget):
        self.jurnal_name = widget.get_text()
        print "jurnal name:", self.jurnal_name
        
    def on_video_toggled(self, widget):
        self.video = widget.get_active()
        
    def on_audio_toggled(self, widget):
        self.audio = widget.get_active()       

    def on_image_toggled(self, widget):
        self.image = widget.get_active()
    
    def on_duration_changed(self, widget):
        self.duration = int(widget.get_value())


tab = Tab(interface.GLADE_TABS, WIDGET_NAME, TAB_NAME)
