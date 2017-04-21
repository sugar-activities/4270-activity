#    Provides funcitonality to the canvas (everything below the toolbox)
#    The canvas is where collected data is managed, analized, played
#    back...

import gtk
import gtk.glade
from sugar.datastore import datastore
import interface
import storedata
import gst
import os

GLADE_FILE = "canvas.glade"
WIDGET_NAME = "canvas"

class Canvas(interface.New):
    def setup(self):
        self.player = gst.element_factory_make("playbin", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        self.PhotoView = self.interface.get_widget("photoView")
        self.model = gtk.ListStore(str, gtk.gdk.Pixbuf)
        self.PhotoView.set_model(self.model)
        self.PhotoView.set_text_column(0)
        self.PhotoView.set_pixbuf_column(1)
        self.MainImage = self.interface.get_widget("mainImage")
        self.selected_name = None
        self.load_all_data()
    
    def on_message(self, bus, message):
            t = message.type
            if t == gst.MESSAGE_EOS:
                     self.player.set_state(gst.STATE_NULL)
            elif t == gst.MESSAGE_ERROR:
                    self.player.set_state(gst.STATE_NULL)
                    err, debug = message.parse_error()
                    print "Error: %s" % err, debug 
                            
    def get_pixbuf(self, entry_title, main_image=False):
        print 'makeing new data entry'
        obj, num = datastore.find({'title':entry_title, 'TimeLapse':'yes',
                                  'mime_type':'image/png'})
        if num != 0:        
            filepath = obj[0].get_file_path()
        else:
            return None
        if not main_image:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filepath, 96, 96)
        else:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filepath, 640, 480)
        return pixbuf


    def new_data_entry(self, entry_title):
        pixbuf = self.get_pixbuf(entry_title)
        self.model.insert(0, [entry_title, pixbuf])
    
    def load_all_data(self):
        try:
            titles = datastore.get_unique_values('TimeLapsetitle')
        except: titles = []    
        for title in titles:
            self.new_data_entry(title)
            

    def get_description_buffer(self, title):
        objects, num = datastore.find({'title':title, 'TimeLapse':'yes'})
        description = objects[0].metadata['description']
        description_buffer = gtk.TextBuffer(table=None)
        description_buffer.set_text(description)
        return description_buffer

    def on_photo_selected(self, widget):
        self.selected_name = widget.get_cells()[0].get_property("text")
        print self.selected_name
        self.interface.get_widget("name_entry").set_text(self.selected_name)
        pixbuf = self.get_pixbuf(self.selected_name, True)
        if pixbuf == None:
            self.MainImage.clear()
        else:
            self.MainImage.set_from_pixbuf(pixbuf)
        description_buffer = self.get_description_buffer(self.selected_name)
        self.get_widget("description_entry").set_buffer(description_buffer)

    def on_name_changed(self, widget, data):
        # not finished. Still need to get old_name and new_name and define change_name
        new_name = self.get_widget('name_entry').get_text()
        print new_name
        new_name = storedata.unique_title(new_name)
        #self.get_widget('name_entry').set_text(new_name)
        storedata.change_name(self.selected_name, new_name)
        for obj in self.model:
            if obj[0] == self.selected_name:
                obj[0] = new_name
        self.selected_name = new_name

    def on_description_changed(self, widget, event):
        textBuffer = widget.get_buffer()
        start = textBuffer.get_start_iter()
        end = textBuffer.get_end_iter()
        description = textBuffer.get_text(start, end)
        storedata.change_description(self.selected_name, description)

    def on_play_clicked(self, widget):
        print 'playing audio'
        if self.selected_name != None:
            obj, num = datastore.find({'title':self.selected_name, 
                                      'TimeLapse':'yes',
                                      'mime_type':'audio/ogg'})
            print 'num of play objects:', num
            soundfile = obj[0].get_file_path()
            if os.path.isfile(os.path.abspath(soundfile)):
                self.player.set_property("uri", "file://" + 
                                         os.path.abspath(soundfile))
	        self.player.set_state(gst.STATE_PLAYING)
	        
    def on_delete_clicked(self, widget):
        if self.selected_name != None:
            count = 0
            for obj in self.model:
                if obj[0] == self.selected_name:
                    iterator = self.model.iter_nth_child(None,count)
                    self.model.remove(iterator)
                count += 1
            ds_objects, num_objects = datastore.find({'title': self.selected_name, 'TimeLapse':'yes'}) 
            
            for i in xrange (0, num_objects, 1):
                print 'DELETING ' + ds_objects[i].metadata['title'] + '...'
                ds_objects[i].destroy()
                datastore.delete(ds_objects[i].object_id)
            self.MainImage.clear()
            self.get_widget('name_entry').set_text('')
            description_buffer = gtk.TextBuffer(table=None)
            description_buffer.set_text('')
            self.get_widget("description_entry").set_buffer(description_buffer)


'''        
    def on_save_clicked(self, widget):
        #name = self.interface.get_widget("name_entry").get_text()
        textBuffer = self.interface.get_widget("description_entry").get_buffer()
        start = textBuffer.get_start_iter()
        end = textBuffer.get_end_iter()
        description = textBuffer.get_text(start, end)
        print description
        if self.selected_name:
            event = self.events[self.selected_name]
            for obj in event:
                new_obj = datastore.create()
                new_obj.metadata['activity'] = "TimeLapse"
                new_obj.metadata['title'] = obj.metadata['title']
                new_obj.metadata['mime_type'] = obj.metadata['mime_type']
                new_obj.metadata["Description"] = description
                obj.metadata["Description"] = description
                new_obj.set_file_path(obj.get_file_path())
                datastore.delete(obj.object_id)
                datastore.write(new_obj)

    def on_photo_selected(self, widget):
        name = widget.get_cells()[0].get_property("text")
        if name in self.events.keys():
            event = self.events[name]
            for obj in event:
                if obj.metadata['mime_type'] == 'image/png':
                     obj.metadata['keep'] = 1
                     datastore.write(obj)
                     filepath = obj.get_file_path()
                     pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filepath,
                                                                   500, 375)
                     self.MainImage.set_from_pixbuf(pixbuf)
                     self.interface.get_widget("name_entry").set_text(name)
                     description_buffer = gtk.TextBuffer(table=None)
                     description_buffer.set_text(obj.metadata['Description'])
                     self.interface.get_widget("description_entry").set_buffer(description_buffer)
                     self.selected_name = name
'''

    
canvas = Canvas(GLADE_FILE, WIDGET_NAME)
