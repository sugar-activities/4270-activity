#    This provides funcionality that is common to all or many of the tabs
#    and the canvas.

import gtk
import gtk.glade
import tlactivity


GLADE_TABS = "tabs.glade"
GLADE_FILE = "canvas.glade"
    
    
class New:
    """Initializes the interface for a tab or canvas."""
    def __init__(self, glade_file, widget_name, tab_name=None):
        self.interface = gtk.glade.XML(glade_file, widget_name)
        self.get_widget = self.interface.get_widget
        self.interface.signal_autoconnect(self)
        self.widget = self.interface.get_widget(widget_name)
        if tab_name is not None:
            self.tab_name = tab_name
        self.setup()


class NewTab(New):
    def setup(self):
        self.store_name = None
        self.duration, self.frequency, self.lapse_speed = None, None, None       
        self.video, self.audio, self.image = True, True, True
        self.make()
        self.collection = None
        
    def set_tab_sensitives(self, sensitive=True):
        tabs = tlactivity.tabs
        if sensitive:
            for tab in tabs:
                tab.widget.set_sensitive(True)
        else:
            for tab in tabs:
                tab.widget.set_sensitive(False)

    def set_alert(self, alert):
        self.alert = alert

    def stop(self, alert, response_id):
        if response_id is gtk.RESPONSE_CANCEL:
            if self.collection != None:
                self.collection.end()

