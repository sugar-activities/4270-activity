#    This maneges the interface of and provides functionality for the 
#    "Start/End Time" tab.

import interface
import datetime
import gobject

TAB_NAME = "Start/End Time"
WIDGET_NAME = "start_end_time"


class Tab(interface.NewTab):
    def make(self):      
        time = datetime.datetime.now()
        if time.hour == 23:
            hour = 0
            # I know, day could be pushed over to 32, causing this program to
            # not function in the last hour of the last day of every month. But
            # I'm too lasy to do a good job... someone else needs to fix this.
            day = time.day + 1
        else:
            day = time.day
            hour = time.hour + 1
        self.get_widget('end_cal').select_month(time.month - 1, time.year)
        self.get_widget('end_cal').select_day(day + 1)
        self.get_widget('end_hour').set_value(hour)
        self.get_widget('start_hour').set_value(hour)
        self.get_widget('start_cal').select_month(time.month - 1, time.year)      
        self.get_widget('start_cal').select_day(day)
        self.set_start_time()
        self.set_end_time()
        gobject.timeout_add(1000, self.update_time)
    
    def update_time(self):
        current_time = datetime.datetime.now().ctime()
        self.get_widget('time').set_text(current_time)
        return True
        
    def set_start_time(self):
        print 'setting start time'
        date = self.get_widget('start_cal').get_date()
        hour = int(self.get_widget('start_hour').get_value())
        minute = int(self.get_widget('start_min').get_value())
        second = int(self.get_widget('start_sec').get_value())
        self.start = datetime.datetime(date[0], date[1] + 1, date[2],
                                       hour, minute, second)
        self.get_widget('start_toggle').set_label(self.start.ctime())
        if not self.get_widget('start_time_toggle').get_active():
            self.start = None
    
    def on_start_time_changed(self, widget):
        self.set_start_time()
            
    def on_start_toggled(self, widget):
        if widget.get_active():
            self.get_widget('start_toggle').show()
            self.get_widget('no_start_label').hide()
        else:
            self.get_widget('start_toggle').hide()
            self.get_widget('no_start_label').show()
            self.get_widget('start_toggle').set_active(False)
    
    def on_change_start_toggled(self, widget):
        if widget.get_active():
            self.get_widget('start_time_ajustment').show()
        else:
            self.get_widget('start_time_ajustment').hide()
            
    def set_end_time(self):
        print 'setting end time'
        date = self.get_widget('end_cal').get_date()
        hour = int(self.get_widget('end_hour').get_value())
        minute = int(self.get_widget('end_min').get_value())
        second = int(self.get_widget('end_sec').get_value())
        self.end = datetime.datetime(date[0], date[1] + 1, date[2],
                                       hour, minute, second)
        self.get_widget('end_toggle').set_label(self.end.ctime())
        if not self.get_widget('end_time_toggle').get_active():
            self.end = None
    
    def on_end_time_changed(self, widget):
        self.set_end_time()
            
    def on_end_toggled(self, widget):
        if widget.get_active():
            self.get_widget('end_toggle').show()
            self.get_widget('no_end_label').hide()
        else:
            self.get_widget('end_toggle').hide()
            self.get_widget('no_end_label').show()
            self.get_widget('end_toggle').set_active(False)
            
    def on_change_end_toggled(self, widget):
        if widget.get_active():
            self.get_widget('end_time_ajustment').show()
        else:
            self.get_widget('end_time_ajustment').hide()


    
tab = Tab(interface.GLADE_TABS, WIDGET_NAME, TAB_NAME)
