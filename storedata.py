#    Deals with storage of data and metadata.
from sugar.datastore import datastore
from canvas import canvas
import time

def unique_title(name):
    if name == '':
        name = 'Untitled'
    objs, num_objects = datastore.find({'title':name, 'TimeLapse':'yes'})
    if num_objects == 0:
        return name
    i = 1
    while num_objects != 0:
        i += 1
        objs, num_objects = datastore.find({'title':name + str(i),
                                          'TimeLapse':'yes'})
    return name + str(i)

def change_description(title, new_discription):
    dsobjects, num = datastore.find({'title':title, 'TimeLapse':'yes'})
    for dsobject in dsobjects:
        dsobject.metadata['description'] = new_discription
        datastore.write(dsobject)
        dsobject.destroy()
        
def change_name(old_name, new_name):
    dsobjects, num = datastore.find({'title':old_name, 'TimeLapse':'yes'})
    for dsobject in dsobjects:
        dsobject.metadata['title'] = new_name
        dsobject.metadata['TimeLapsetitle'] = new_name
        datastore.write(dsobject)
        dsobject.destroy()
       
        
def store_data(entry_title, mime_type, file_path):
    file_dsobject = datastore.create()
    file_dsobject.metadata['TimeLapse'] = 'yes'
    file_dsobject.metadata['TimeLapsetitle'] = entry_title
    file_dsobject.metadata['title'] = entry_title
    file_dsobject.metadata['mime_type'] = mime_type
    file_dsobject.metadata['description'] = ''
    file_dsobject.set_file_path(file_path)
    datastore.write(file_dsobject) 
    file_dsobject.destroy()
    
class Collection:
    def __init__(self, tab):
        self.tab = tab
        self.entry_title = unique_title(tab.jurnal_name)
        if tab.video:
            self.video_temp = "/tmp/tmp" + str(time.time()) + '.ogv'
        if tab.audio:
            self.audio_temp = "/tmp/tmp" + str(time.time()) + '.flac'
        if tab.image:
            self.image_temp = "/tmp/tmp" + str(time.time()) + '.png'
        self.start()

    def store_data(self):
        if self.tab.video:
            store_data(self.entry_title, 'video/ogg', self.video_temp)
        if self.tab.audio:
            store_data(self.entry_title, 'audio/ogg', self.audio_temp)
        if self.tab.image:
            store_data(self.entry_title, 'image/png', self.image_temp)
        canvas.new_data_entry(self.entry_title)
    
    
   
class LapseCollection:
    def __init__(self, tab):
        self.tab = tab
        self.entry_title = unique_title(tab.jurnal_name)
        self.lapse_temp = "/tmp/tmp" + str(time.time()) + '.mjpeg'
        self.convert_temp = "/tmp/tmp" + str(time.time()) + '.ogg'
        self.start()

    def store_data(self):
        store_data(self.entry_title, 'video/ogg', self.convert_temp)
        canvas.new_data_entry(self.entry_title)
