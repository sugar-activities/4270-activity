#    This maneges the interface of and provides functionality for the 
#    "Time-Lapse Collection" tab.

import interface
import collectdata

TAB_NAME = "Time Lapse Collection"
WIDGET_NAME = "time_lapse_collection"


class Tab(interface.NewTab):
    def make(self):
        self.lapse_speed = 30
        self.jurnal_name = ''
        
    def on_begin_collecting(self, widget):
        print 'collecting tltab'
        self.collection = collectdata.Lapse(self)

    def on_name_changed(self, widget):
        # this along with others could be moved to NewTab class
        self.jurnal_name = widget.get_text()
        
    def on_speed_changed(self, widget):
        hours = self.get_widget('hour_speed').get_value()
        mins = self.get_widget('min_speed').get_value()
        secs = self.get_widget('sec_speed').get_value()
        # I should do this a nicer non math way
        self.lapse_speed = int(hours * 3600 + mins * 60 + secs)
        print "lapse speed changed: ", self.lapse_speed
        
    
    
    
tab = Tab(interface.GLADE_TABS, WIDGET_NAME, TAB_NAME)
