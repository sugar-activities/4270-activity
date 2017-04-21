#    This maneges the interface of and provides functionality for the 
#    "Incramental Collection" tab.

import interface
import collectdata

TAB_NAME = "Incremental Collection"
WIDGET_NAME = "incramental_collection"


class Tab(interface.NewTab):
    def make(self):
        self.duration = 5
        self.frequency = 15
        self.jurnal_name = ''
        
    def on_begin_pushed(self, widget):
        self.collection = collectdata.Incramental(self)

    def on_name_changed(self, widget):
        self.jurnal_name = widget.get_text()

    def on_video_toggled(self, widget):
        self.video = widget.get_active()
        
    def on_audio_toggled(self, widget):
        self.audio = widget.get_active()       

    def on_image_toggled(self, widget):
        self.image = widget.get_active()

    def on_duration_changed(self, widget):
        self.duration = widget.get_value()

    def on_frequency_min_changed(self, widget):
        self.frequency = widget.get_value() * 60
        hours = self.interface.get_widget('frequency_hour').get_value()
        self.frequency += hours * 3600

    def on_frequency_hour_changed(self, widget):
        self.frequency = widget.get_value() * 3600
        minutes = self.interface.get_widget('frequency_min').get_value()
        self.frequency += minutes * 60

    
tab = Tab(interface.GLADE_TABS, WIDGET_NAME, TAB_NAME)
