#    This is where the actual collection of data takes place. For example,
#    it gets video and audio streams from the XO's camera and microphone.
#    Requests to collect data come from the collectdata.py file

import os
from sugar.activity import activity
from sugar.datastore import datastore
import gst
import time
import datetime
import qualitytab
import storedata
import subprocess
# type = mimetypes.types_map['.flac']

# All predefined quality settings have a langth of 5 with quality low to high
BITRATES = [16000, 20000, 24000, 32000, 48000]


class Collect(storedata.Collection):
    def start(self):
        print 'qualitytab.tab in cameramic', qualitytab.tab
        self.bitrate = BITRATES[qualitytab.tab.audio]       
        self.collecting_video, self.collecting_audio = False, False
        if self.tab.video:
            self.video()
        if self.tab.audio:
            self.audio()

            
    def end(self):
        if self.tab.video:
            self.end_video()
        if self.tab.audio:
            self.end_audio()
        if self.tab.image:
            self.image()
        else:
            self.store_data()
    
    def video(self):
        VIDEO_GST_PIPE = ['v4l2src', 'queue', 'videorate', 
                          'video/x-raw-yuv,framerate=15/1', 'videoscale', 
                          'video/x-raw-yuv,width=%d,height=%d' % (qualitytab.tab.width, qualitytab.tab.height),
                          'ffmpegcolorspace', 'theoraenc', 'oggmux']
        pipe = VIDEO_GST_PIPE + ["filesink location=%s" % (self.video_temp)]
        self.video_pipe = gst.parse_launch('!'.join(pipe))
        self.video_pipe.set_state(gst.STATE_PLAYING)
	print qualitytab.tab.width
	print qualitytab.tab.height

    def end_video(self):
        self.video_pipe.set_state(gst.STATE_NULL)    
            
    def audio(self):
        AUDIO_GST_PIPE = ["alsasrc", 
                          "audio/x-raw-int,rate=%d,channels=1,depth=16" % 
                          qualitytab.tab.rate, "audioconvert","flacenc"]
        pipe = AUDIO_GST_PIPE + ["filesink location=%s" % (self.audio_temp)]
        self.audio_pipe = gst.parse_launch('!'.join(pipe))
        self.audio_pipe.set_state(gst.STATE_PLAYING)
	print qualitytab.tab.rate        

    def end_audio(self):
        self.audio_pipe.set_state(gst.STATE_NULL)   

    def image(self):      
        VIDEO_GST_PIPE = ['v4l2src', 'ffmpegcolorspace', 'pngenc']        
        pipe=VIDEO_GST_PIPE + ["filesink location=%s" % self.image_temp]
        self.pipe=gst.parse_launch("!".join(pipe))
        self.bus=self.pipe.get_bus()
        self.pipe.set_state(gst.STATE_PLAYING)
        self.bus.poll(gst.MESSAGE_EOS, -1)
        self.pipe.set_state(gst.STATE_NULL)
        
        self.store_data()
          


class CollectLapse(storedata.LapseCollection):
    def start(self):
        print 'collecting camramic'
        pipe = ['v4l2src', 'videorate',
                'video/x-raw-yuv,width=640,height=480,framerate=1/%d'
                % self.tab.lapse_speed, 'ffmpegcolorspace', 'jpegenc',
                'multipartmux', 'filesink location=%s' % self.lapse_temp]
        self.lapse_pipe = gst.parse_launch("!".join(pipe))
        self.lapse_pipe.set_state(gst.STATE_PLAYING)
       
    def end(self):
        self.lapse_pipe.set_state(gst.STATE_NULL)
        subprocess.check_call(["gst-launch", "filesrc", 
                              "location=%s" %self.lapse_temp, "!",
                              "multipartdemux", "!", "jpegdec", "!",
                              "theoraenc", "!", "oggmux", "!", "filesink",
                              "location=%s" %self.convert_temp])
        '''
        pipe = ['filesrc location=%s' % self.lapse_temp, 'multipartdemux',
                   'jpegdec', 'theoraenc', 'oggmux', 'filesink location=%s' %
                   self.convert_temp]
        convert_pipe = gst.parse_launch("!".join(pipe))
        #bus = convert_pipe.get_bus()
        convert_pipe.set_state(gst.STATE_PLAYING)
        #bus.poll(gst.MESSAGE_EOS, -1)
        time.sleep(15)
        convert_pipe.set_state(gst.STATE_NULL)
        '''
        self.store_data()
    
    
    
    
    
    
    
    
    
    
    
    
    
        
