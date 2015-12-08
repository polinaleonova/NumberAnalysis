import os
import gtk, gobject


class MyApp:
    def __init__( self, title):
        self.window = gtk.Window()
        self.title = 'Number Analysis'
        self.window.set_title(title)
        self.window.set_default_size(300, 300)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("destroy", self.destroy)
        self.create_interior()
        self.window.show_all()
        self.counter = 0
        self.fullname = ""

    def create_interior(self):
        self.label_template = "<b>%s</b>"
        self.label = gtk.Label(self.label_template % (""))
        self.label.set_use_markup(True)
        select_file = gtk.Button("Select file..")
        select_file.set_size_request(100, 30)
        select_file.connect("clicked", self.open_file)
        #button go
        self.go_button = gtk.Button("GO")
        self.go_button.set_size_request(100, 100)
        self.go_button.connect("clicked", self.go)
        #entry field and label
        lab = gtk.Label("Sequence:")
        self.entry = gtk.TextView()
        self.entry.set_size_request(50, 100)
        self.entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
        #field found and label
        self.found_template = "Found: <b>%s</b>"
        self.found = gtk.Label(self.found_template % (""))
        self.found.set_use_markup(True)
        #progressbar
        self.prog_bar = gtk.ProgressBar(adjustment=None)
        self.prog_bar.set_size_request(260, 10)
        #errorlabel
        self.error_label = gtk.Label()
        # self.error_label.set_size_request(20, 200)
        self.error_label.set_label("")
        #fixed
        fixed = gtk.Fixed()

        fixed.put(self.label, 150, 25)
        fixed.put(self.go_button, 150, 90)
        fixed.put(select_file, 20, 20)
        fixed.put(lab, 20, 60)
        fixed.put(self.entry, 25, 90)
        fixed.put(self.found, 20, 200)
        fixed.put(self.prog_bar, 20, 230)
        fixed.put(self.error_label, 20, 250)
        self.window.add(fixed)

    def main(self):
        gtk.main()

    def destroy(self, w):
        gtk.main_quit()

    def open_file(self, w, data=None):
        file_chooser = gtk.FileChooserDialog(
            title="Select a file",
            parent=self.window,
            action=gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=("OK", True, "Cancel", False)
        )
        ok = file_chooser.run()
        print ok
        if ok:
            self.fullname = file_chooser.get_filename()
            dirname, fname = os.path.split(self.fullname)
            text = self.label_template % (fname)
        else:
            self.fullname = ""
            text = self.label_template % ("")
        self.label.set_label(text)
        file_chooser.destroy()

    def _go_step(self):
        self.start_settings()
        yield True
        #read user's sequence
        buffer = self.entry.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        wat = (buffer.get_text(start_iter, end_iter, True)).splitlines()
        #read list of number from file
        if self.fullname:
            f = open(self.fullname)
            where = f.read().splitlines()
            f.close()
            if where and wat:
                for procent in self.generate_result(where, wat):
                    self.prog_bar.set_fraction(round(procent, 2))
                    self.found.set_label(self.found_template % (str(self.counter)))
                    yield True
            else:
                self.error_label.set_label("Please, fill \"Sequence\" \n field with column of numbers")
        else:
            self.error_label.set_label("Please, choose file")
            self.fullname = None
            self.label.set_label(self.label_template % (""))
        self.go_button.set_sensitive(True)
        # self.fullname = None
        # self.label.set_label(self.label_template % (""))
        yield False

    def go(self, w):
        self.go_button.set_sensitive(False)
        job = self._go_step()
        gobject.idle_add(job.next)

    def start_settings(self):
        self.prog_bar.set_fraction(0.00)
        self.found.set_label(self.found_template % (""))
        self.error_label.set_label("")

    def generate_result(self, where, wat):
        len_wat = len(wat)
        len_all = float(len(where))
        self.counter = 0
        self.prog_bar.set_fraction(0.00)
        index = -1
        while True:
            try:
                index = where[index+1:].index(wat[0]) + index + 1
            except ValueError:
                break
            percent = (index + 1) / len_all
            percent_need_format = round(percent, 2)
            if where[index:index+len_wat] == wat:
                self.counter += 1
            # self.prog_bar.set_fraction(p)
            yield percent_need_format
        yield 1.00


if __name__ == "__main__":
    m = MyApp("Open File")
    m.main()