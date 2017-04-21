#    This controls data collection. It gets data using the cameramic.py
#    file based on the requests and settings of the "tab" files. It does
#    things like starting and stoping data collection.

from sugar.activity import activity
import cameramic
import timetab
import tlactivity
import gobject
import time
import datetime
timetab = timetab.tab


class Timer:                 
    def __init__(self, seconds, call):
        self.canceled = False
        def timer_call():
            if not self.canceled:
                call()
            return False      
            
        milliseconds = int(seconds * 1000) # change this to use time conversion
        gobject.timeout_add(milliseconds, timer_call) 
        
    def cancel(self):
        self.canceled = True
        
        
class Collection:
    def __init__(self, tab):
        self.tab = tab
        self.start_time = timetab.start
        self.end_time = timetab.end
        
        if self.start_time is not None:
            self.start_time
            wait_time = self.start_time - datetime.datetime.now()
            wait_time = wait_time.seconds
            print 'wait time', wait_time
            self.starter = Timer(wait_time, self.collect)
        else:
            self.collect()
 
        if self.end_time is not None:
            wait_time = self.end_time - datetime.datetime.now()
            wait_time = wait_time.seconds
            self.ender = Timer(wait_time, self.end)

    def end_now(self):
        self.starter.cancel()
        self.end()


class Single(Collection):
    def collect(self):
        video, audio, image = '', '', ''
        if self.tab.video:
            video = 'Video  '
        if self.tab.audio:
            audio = 'Audeo  '
        if self.tab.image:
            image = 'Image  '
        self.tab.alert.props.title='Single Collection'
        msg = 'Start Time: ' + str(self.start_time) + '; End Time: ' + \
        str(self.end_time) + ";  Duration: " + str(self.tab.duration) + \
        ';  Collecting: %s%s%s' %(video, audio, image)
        self.tab.alert.props.msg = msg
        self.tab.alert.show()
        self.collection = cameramic.Collect(self.tab)
        self.timer = Timer(self.tab.duration, self.end)
        self.tab.set_tab_sensitives(False)
     
    def end(self):
        self.timer.cancel()
        self.collection.end()
        self.tab.set_tab_sensitives(True)
        self.tab.alert.hide()
        self.tab.collection = None
             
class Incramental(Collection):
    def single_collect(self):
        self.collection = cameramic.Collect(self.tab)
        self.stimer = Timer(self.tab.duration, self.collection.end)
  
    def collect(self):        
        video, audio, image = '', '', ''
        if self.tab.video:
            video = 'Video  '
        if self.tab.audio:
            audio = 'Audeo  '
        if self.tab.image:
            image = 'Image  '
        self.tab.alert.props.title='Incramental Collection'
        msg = 'Start Time: ' + str(self.start_time) + '; End Time: ' + \
        str(self.end_time) + ";  Duration: " + str(self.tab.duration) + \
        ';  Frequency:' + str(self.tab.frequency) + ';  Collecting: %s%s%s' % \
        (video, audio, image)
        self.tab.alert.props.msg = msg
        self.tab.alert.show()
        self.started_time = time.time()
        self.count = 1
        self.incrament() 
           
    def incrament(self):
        self.single_collect()       
        start_time = self.started_time + self.tab.frequency * self.count
        wait_time = start_time - time.time()
        print "wait time:", wait_time
        self.itimer = Timer(wait_time, self.incrament)
        self.count += 1

    def end(self):
        self.itimer.cancel()
        self.collection.end()
        self.tab.alert.hide()
        self.tab.collection = None
            
class Lapse(Collection):
    def collect(self): 
        self.tab.alert.props.title='Time Lapse Collection'
        msg = 'Start Time: ' + str(self.start_time) + '; End Time: ' + \
        str(self.end_time) +'  Collecting one frame every %s seconds.' % (
                                                           self.tab.lapse_speed)
        self.tab.alert.props.msg = msg
        self.tab.alert.show()
        print 'collecting collectdata'
        self.collection = cameramic.CollectLapse(self.tab)
        #self.timer = Timer(30, self.end)
                                                           
    def end(self):
        print "lapse collection ending"
        self.collection.end()
        self.tab.alert.hide()
        self.tab.collection = None
