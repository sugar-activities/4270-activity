#    This is where the TimeLapse activity starts up. The actual TimeLapse
#    window gets created here, among other things.

from threading import Timer
from sugar.activity import activity
import singletab, incramentaltab, lapsetab, timetab, qualitytab
import playback
import canvas
from sugar.graphics.alert import Alert
from sugar.graphics.icon import Icon
import gtk


canvas = canvas.canvas
singletab = singletab.tab
singletab.set_canvas(canvas)
incramentaltab = incramentaltab.tab
lapsetab = lapsetab.tab
timetab = timetab.tab
qualitytab = qualitytab.tab
print 'qualitytab.tab in tlactivity:', qualitytab
tabs = [singletab, incramentaltab, lapsetab, timetab, qualitytab]
    
    
class TimeLapseActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.set_canvas(canvas.widget)
        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        alert = Alert()
        # Populate the title and text body of the alert. 
        alert.props.title='Current Recording'
        alert.props.msg = 'recording information goes here'
        stop_icon = Icon(icon_name='dialog-cancel')
        stop_icon.set_pixel_size(50)
        alert.add_button(gtk.RESPONSE_CANCEL, 'End', stop_icon)
        stop_icon.show()
        alert.connect('response', singletab.stop)
        alert.connect('response', incramentaltab.stop)
        alert.connect('response', lapsetab.stop)
        # Call the add_alert() method (inherited via the sugar.graphics.Window superclass of Activity)
        # to add this alert to the activity window. 
        self.add_alert(alert)
        alert.hide()

        for tab in tabs:
            toolbox.add_toolbar(tab.tab_name, tab.widget)
            tab.set_alert(alert)


        
        
