# filter.py
# Copyright 2016 Roger Marsh
# Licence: See LICENSE.txt (BSD licence)

"""Filter fields in zipped DBF files.

This module axtracts the contents of the zip file into memory files and allows
fields to be removed from any DBF files present without making a permanent copy
of the original data on the local computer's drives.

The lifetime of, and access to, any temporary copy will depend on the security
policy in force: hard disk encryption and swap space overwrite for example.

The filterd files may be included in a zip file replacing the original versions,
but otherwise containing all files from the original zip file.

The extracted files may be saved on the local computer.

The size of the extracted files which can be handled is limited by the memory
installed on the local computer.

DBF files may be viewed or saved in CSV format.  The utf-8 and iso-8859-1
encodings are tried, utf-8 first, to do either action.  Other encodings are
not supported.

"""

import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox
import urllib.request
import io
import os
import zipfile
import datetime

from . import urlzippedfile

_SELECTEDNAME = 'selectedname'
_FIELDNAMETAG = 'fieldnametag'
_FILENAMETAG = 'filenametag_'
_DBFFILENAME = 'dbffilename_'
_OTHERFILENAME = 'otherfilename'
_FIELDNAMECURSOR = 'fieldnamecursor'
_FILENAMECURSOR = 'filenamecursor'
_START_TEXT = ''.join(('Enter URL in upper row, or right-click for menu.',
                       ' Password, if any, in lower row.',
                       ))
_HELP = 'help.rst'


class FilterError(Exception):
    pass


class Filter:
    """Select fields in DBF files and replace values by null.

    The values of the selected fields are overwritten with '\x00' bytes.
    
    """
    def __init__(self):
        """Build the user interface."""
        root = tkinter.Tk()
        root.wm_title('Filter fields in zipped DBF files')
        root.wm_resizable(width=tkinter.FALSE, height=tkinter.FALSE)
        frame = tkinter.ttk.Frame(master=root)
        frame.pack()
        entry = tkinter.ttk.Entry(master=frame)
        entry.pack(fill=tkinter.X)
        contents = tkinter.StringVar()
        entry["textvariable"] = contents
        pwentry = tkinter.ttk.Entry(master=frame, show='*')
        pwentry.pack(fill=tkinter.X)
        pwcontents = tkinter.StringVar()
        pwentry["textvariable"] = pwcontents
        panedwindow = tkinter.ttk.Panedwindow(
            master=frame,
            orient=tkinter.VERTICAL,
            width=600,
            height=300)
        panedwindow.pack(fill=tkinter.BOTH)
        frame = tkinter.ttk.Frame(master=panedwindow)
        panedwindow.add(frame, weight=1)
        text = tkinter.Text(master=frame, wrap=tkinter.WORD)
        scrollbar = tkinter.ttk.Scrollbar(
            master=frame,
            orient=tkinter.VERTICAL,
            command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        text.pack(fill=tkinter.BOTH)
        dbfframe = tkinter.ttk.Frame(master=panedwindow)
        panedwindow.add(dbfframe, weight=2)
        dbftext = tkinter.Text(master=dbfframe, wrap=tkinter.NONE)
        scrollbar = tkinter.ttk.Scrollbar(
            master=dbfframe,
            orient=tkinter.VERTICAL,
            command=dbftext.yview)
        dbftext.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollbar = tkinter.ttk.Scrollbar(
            master=dbfframe,
            orient=tkinter.HORIZONTAL,
            command=dbftext.xview)
        dbftext.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        dbftext.pack(fill=tkinter.BOTH)
        self.dbf_menu = tkinter.Menu(master=dbfframe, tearoff=False)
        self.menu = tkinter.Menu(master=frame, tearoff=False)
        self.__menu = self.menu
        self.menu_file_dbf = tkinter.Menu(master=frame, tearoff=False)
        self.menu_file_other = tkinter.Menu(master=frame, tearoff=False)
        self.menu_field = tkinter.Menu(master=frame, tearoff=False)
        self.entry = entry
        self.pwentry = pwentry
        self.dbftext = dbftext
        self.text = text
        self.set_menu_and_entry_events_for_open_url(True)
        entry.bind('<ButtonPress-3>', self.show_menu)
        text.bind('<ButtonPress-3>', self.show_menu)
        dbftext.bind('<ButtonPress-3>', self.show_dbf_menu)
        self.insert_text(_START_TEXT)
        entry.focus_set()
        self.root = root
        self.contents = contents
        self.pwcontents = pwcontents
        self.zippeddata = None
        self.__help = None
        self.original_zip_password_protected = None

        # This way round so _SELECTEDNAME has higher priority than other two.
        text.tag_configure(_FIELDNAMECURSOR, background='greenyellow')
        text.tag_configure(_FILENAMECURSOR, background='yellowgreen')
        text.tag_configure(_SELECTEDNAME, background='cyan')
        
        self.text.tag_bind(_FIELDNAMETAG,
                           sequence='<ButtonPress-1>',
                           func=self.select_field)
        self.text.tag_bind(_FILENAMETAG,
                           sequence='<ButtonPress-1>',
                           func=self.select_file)
        self.text.tag_bind(_FIELDNAMETAG,
                           sequence='<ButtonPress-3>',
                           func=self.show_menu_field)
        self.text.tag_bind(_FILENAMETAG,
                           sequence='<ButtonPress-3>',
                           func=self.show_menu_file_dbf)
        self.text.tag_bind(_OTHERFILENAME,
                           sequence='<ButtonPress-3>',
                           func=self.show_menu_file_other)
        self.menu_field.add_separator()
        self.menu_field.add_command(label='(De)select Field',
                                    command=self.select_field_command,
                                    accelerator='Button 1')
        self.menu_field.add_command(label='Prior Field',
                                    command=self.prior_field_tag,
                                    accelerator='F7')
        self.menu_field.add_command(label='Next Field',
                                    command=self.next_field_tag,
                                    accelerator='F8')
        self.menu_field.add_separator()
        self.menu_field.add_command(label='Help',
                                    command=self.show_help,
                                    accelerator='F1')
        self.menu_file_dbf.add_separator()
        self.menu_file_dbf.add_separator()
        self.menu_file_dbf.add_command(label='(De)select File',
                                       command=self.select_file_command,
                                       accelerator='Button 1')
        self.menu_file_dbf.add_command(label='Prior File',
                                       command=self.prior_file_tag,
                                       accelerator='Alt F7')
        self.menu_file_dbf.add_command(label='Next File',
                                       command=self.next_file_tag,
                                       accelerator='Alt F8')
        self.menu_file_dbf.add_command(label='Show as CSV',
                                       command=self.show_dbf_as_csv_command,
                                       accelerator='F6')
        self.menu_file_dbf.add_separator()
        self.menu_file_dbf.add_command(label='Filter to DBF',
                                       command=self.filter_to_dbf_command,
                                       accelerator='F11')
        self.menu_file_dbf.add_command(label='Filter to CSV',
                                       command=self.filter_to_csv_command,
                                       accelerator='F12')
        self.menu_file_dbf.add_separator()
        self.menu_file_dbf.add_command(label='Help',
                                       command=self.show_help,
                                       accelerator='F1')
        self.menu_file_dbf.add_separator()
        self.menu_file_other.add_separator()
        self.menu_file_other.add_command(label='(De)select File',
                                         command=self.select_file_command,
                                         accelerator='Button 1')
        self.menu_file_other.add_command(label='Prior File',
                                         command=self.prior_file_tag,
                                         accelerator='Alt F7')
        self.menu_file_other.add_command(label='Next File',
                                         command=self.next_file_tag,
                                         accelerator='Alt F8')
        self.menu_file_other.add_separator()
        self.menu_file_other.add_command(label='Extract File',
                                         command=self.extract_original_command,
                                         accelerator='F2')
        self.menu_file_other.add_separator()
        self.menu_file_other.add_command(label='Help',
                                         command=self.show_help,
                                         accelerator='F1')
        self.menu_file_dbf.add_separator()

    def clear_dbftext(self):
        """Wrap Text widget delete with Enable and Disable state configure."""
        self.dbftext.delete('1.0', tkinter.END)

    def insert_dbftext(self, text):
        """Wrap Text widget insert with Enable and Disable state configure."""
        self.dbftext.insert(tkinter.END, text)

    def insert_text(self, text):
        """Wrap Text widget insert with Enable and Disable state configure."""
        self.text.insert(tkinter.END, text)

    def insert_and_tag_text(self, text, tags=None):
        """Wrap Text widget insert and tag with Enable and Disable."""
        if tags:
            self.text.insert(tkinter.END, text, *(tags,))
        else:
            self.text.insert(tkinter.END, text)

    def insert_file_name(self, filename, filetypetag):
        """Append filename to Text widget."""
        self.insert_text('\n')
        self.insert_and_tag_text(filename, (_FILENAMETAG, filetypetag))
        self.insert_text('\n')

    def insert_field_name(self, fieldname, filename, lastfield=False):
        """Append filename to Text widget."""
        self.insert_and_tag_text(fieldname, (filename, _FIELDNAMETAG))
        if lastfield:
            self.insert_text('\n')
        else:
            self.insert_text(' ')

    def show_menu(self, event=None):
        """Show the popup menu for widget."""
        self.__menu.tk_popup(*event.widget.winfo_pointerxy())
        self.__xy = event.x, event.y
        self.__menu = self.menu

    def show_dbf_menu(self, event=None):
        """Show the popup menu for widget."""
        self.dbf_menu.tk_popup(*event.widget.winfo_pointerxy())
        self.__xy = event.x, event.y

    def show_menu_field(self, event=None):
        """Show the popup menu for fieldtag."""
        self.__menu = self.menu_field

    def show_menu_file_dbf(self, event=None):
        """Show the popup menu for file tag."""
        self.__menu = self.menu_file_dbf

    def show_menu_file_other(self, event=None):
        """Show the popup menu for non-dbf file."""
        self.__menu = self.menu_file_other

    def browse_localhost_file(self, event=None):
        """Select a zip file on localhost."""
        localfilename = tkinter.filedialog.askopenfilename(
            parent=self.text,
            title='Browse File',
            defaultextension='.zip',
            initialdir='~')
        if localfilename:
            self.contents.set(''.join(('file:', localfilename)))

    def open_or_download_file(self, event=None):
        """Open or download a zip file by URL."""
        password = self.pwcontents.get().encode()
        if not password:
            password = None
        self.original_zip_password_protected = bool(password)
        resource = self.contents.get()
        if not resource:
            tkinter.messagebox.showinfo(
                title='Get URL',
                message=''.join(('"',
                                 resource,
                                 '"\n\nis not an Uniform Resource Locator ',
                                 '(URL)')))
            return
        try:
            url = urllib.request.urlopen(resource)
        except Exception as exc:
            tkinter.messagebox.showinfo(
                title='Get URL',
                message=''.join(('Eception raised trying to open URL\n\n',
                                 str(exc))))
            return
        try:
            urldata = url.read()
        except Exception as exc:
            tkinter.messagebox.showinfo(
                title='Get URL',
                message=''.join(('Eception raised trying to read URL\n\n',
                                 str(exc))))
            return
        try:
            zippeddata = urlzippedfile.URLZippedFile(
                io.BytesIO(urldata), password)
        except Exception as exc:
            tkinter.messagebox.showinfo(
                title='Get URL',
                message=''.join(('Eception raised trying to unzip URL data\n\n',
                                 str(exc))))
            return
        try:
            for filename in zippeddata.filenames:
                zippeddata.open_zipped_file(filename)
        except Exception as exc:
            tkinter.messagebox.showinfo(
                title='Get URL',
                message=''.join(('Eception raised trying to open dBase ',
                                 'files\n\n',
                                 str(exc))))
            raise
        for filename in zippeddata.filenames:
            zf = zippeddata.filters[filename]
            self.insert_file_name(
                filename,
                _DBFFILENAME if zf.is_dbf_format else _OTHERFILENAME)
            if not zf.is_dbf_format:
                continue
            sfn = zf.sortedfieldnames
            for fieldname in sfn:
                self.insert_field_name(
                    fieldname, filename, lastfield=fieldname==sfn[-1])
        self.set_menu_and_entry_events_for_open_url(False)
        self.set_menu_and_entry_events_for_edit_url(True)
        self.zippeddata = zippeddata

    def _select_item(self, itemtag, selecttag, x, y):
        """Select or deselect field or file item."""
        ti = self.text.index(''.join(('@', str(x), ',', str(y))))
        tags = self.text.tag_names(ti)
        tr = self.text.tag_prevrange(itemtag, ti)
        if selecttag in tags:
            self.text.tag_remove(selecttag, *tr)
        elif itemtag in tags:
            self.text.tag_add(selecttag, *tr)

    def select_field(self, event=None):
        """Select or deselect field for removal from file."""
        self._select_item(_FIELDNAMETAG, _SELECTEDNAME, event.x, event.y)

    def select_field_command(self):
        """Select or deselect field for removal from file."""
        self._select_item(_FIELDNAMETAG, _SELECTEDNAME, *self.__xy)

    def select_file(self, event=None):
        """Select or deselect file for removal from zip archive copy."""
        self._select_item(_FILENAMETAG, _SELECTEDNAME, event.x, event.y)

    def select_file_command(self):
        """Select or deselect file for removal from zip archive copy."""
        self._select_item(_FILENAMETAG, _SELECTEDNAME, *self.__xy)

    def _next_item_tag(self, itemtag, cursortag):
        """Move cursor to next item name."""
        tr = self.text.tag_ranges(cursortag)
        if not tr:
            trf = self.text.tag_ranges(itemtag)
            if trf:
                self.text.tag_add(cursortag, *trf[:2])
            return
        self.text.tag_remove(cursortag, *tr)
        trf = self.text.tag_nextrange(itemtag, tr[-1])
        if trf:
            self.text.tag_add(cursortag, *trf)
            return

    def next_field_tag(self, event=None):
        """Move cursor to next field name."""
        self._next_item_tag(_FIELDNAMETAG, _FIELDNAMECURSOR)

    def next_file_tag(self, event=None):
        """Move cursor to next file name."""
        self._next_item_tag(_FILENAMETAG, _FILENAMECURSOR)

    def _prior_item_tag(self, itemtag, cursortag):
        """Move cursor to prior field name."""
        tr = self.text.tag_ranges(cursortag)
        if not tr:
            trf = self.text.tag_ranges(itemtag)
            if trf:
                self.text.tag_add(cursortag, *trf[-2:])
            return
        self.text.tag_remove(cursortag, *tr)
        trf = self.text.tag_prevrange(itemtag, tr[0])
        if trf:
            self.text.tag_add(cursortag, *trf)
            return

    def prior_field_tag(self, event=None):
        """Move cursor to prior field name."""
        self._prior_item_tag(_FIELDNAMETAG, _FIELDNAMECURSOR)

    def prior_file_tag(self, event=None):
        """Move cursor to prior file name."""
        self._prior_item_tag(_FILENAMETAG, _FILENAMECURSOR)

    def _select_current_item(self, itemtag, selecttag, cursortag):
        """Select or deselect item at cursor for removal."""
        tr = self.text.tag_ranges(cursortag)
        if not tr:
            return
        tags = self.text.tag_names(tr[0])
        if selecttag in tags:
            self.text.tag_remove(selecttag, *tr)
        elif itemtag in tags:
            self.text.tag_add(selecttag, *tr)

    def select_current_field(self, event=None):
        """Select or deselect field at cursor for removal from file."""
        self._select_current_item(
            _FIELDNAMETAG, _SELECTEDNAME, _FIELDNAMECURSOR)

    def select_current_file(self, event=None):
        """Select or deselect field at cursor for removal from file."""
        self._select_current_item(
            _FILENAMETAG, _SELECTEDNAME, _FILENAMECURSOR)

    def _get_selected_items(self, tagname):
        """Return set containing selected files."""
        tr = list(self.text.tag_ranges(_SELECTEDNAME))
        selected = set()
        while tr:
            selected.add(self.text.get(tr.pop(0), tr.pop(0)))
        tr = list(self.text.tag_ranges(tagname))
        items = set()
        while tr:
            items.add(self.text.get(tr.pop(0), tr.pop(0)))
        return selected.intersection(items)

    def get_selected_files(self):
        """Return set containing selected files."""
        return self._get_selected_items(_FILENAMETAG)

    def get_selected_fields_in_file(self, filename):
        """Return set containing selected fields in file."""
        return self._get_selected_items(filename)

    def _extract_original(self, tag_ranges):
        """Write extracted data to file."""
        if not tag_ranges:
            return
        otherfilename = self.text.get(*tag_ranges)
        savefile = tkinter.filedialog.asksaveasfilename(
            title='Save extracted File',
            initialfile=otherfilename,
            initialdir='~')
        if savefile:
            open(savefile, 'wb').write(self.zippeddata.contents[otherfilename])

    def extract_original(self, event=None):
        """Write extracted data to file."""
        tr = self.text.tag_ranges(_FILENAMECURSOR)
        if tr:
            self._extract_original(tr)

    def extract_original_command(self):
        """Write extracted data to file."""
        x, y = self.__xy
        ti = self.text.index(''.join(('@', str(x), ',', str(y))))
        self._extract_original(self.text.tag_prevrange(_FILENAMETAG, ti))

    def _show_dbf_as_csv(self, tag_ranges):
        """Show dbf in CSV format after removing data in selected fields."""
        if not tag_ranges:
            return
        dbfname = self.text.get(*tag_ranges)
        if not self.zippeddata.filters[dbfname].is_dbf_format:
            tkinter.messagebox.showinfo(
                title='Show DBF as CSV',
                message=''.join(('"',
                                 dbfname,
                                 '"\n\nis not a dBase file (*.dbf)')))
            return
        fields = self.get_selected_fields_in_file(dbfname)
        self.clear_dbftext()
        self.insert_dbftext(''.join((dbfname, '\n\n')))
        try:
            self.insert_dbftext(
                self.zippeddata.filters[dbfname].to_csv(discard=fields))
        except UnicodeDecodeError:
            try:
                self.insert_dbftext(
                    self.zippeddata.filters[dbfname].to_csv(
                        encoding='iso-8859-1',
                        discard=fields))
            except UnicodeDecodeError:
                tkinter.messagebox.showinfo(
                    title='Show DBF as CSV',
                    message=''.join(('"',
                                     dbfname,
                                     '"\n\ncannot be decoded using codec ',
                                     'iso-8859-1')))

    def show_dbf_as_csv(self, event=None):
        """Show dbf in CSV format after removing data in selected fields."""
        tr = self.text.tag_ranges(_FILENAMECURSOR)
        if tr:
            self._show_dbf_as_csv(tr)

    def show_dbf_as_csv_command(self):
        """Show dbf in CSV format after removing data in selected fields."""
        x, y = self.__xy
        ti = self.text.index(''.join(('@', str(x), ',', str(y))))
        self._show_dbf_as_csv(self.text.tag_prevrange(_FILENAMETAG, ti))

    def clear_dbf_as_csv(self, event=None):
        """Delete the text currently displayed to show filtered data."""
        self.clear_dbftext()

    def _filter_to_dbf(self, tag_ranges):
        """Write to DBF file after removing data in selected fields."""
        if not tag_ranges:
            return
        dbfname = self.text.get(*tag_ranges)
        if not self.zippeddata.filters[dbfname].is_dbf_format:
            tkinter.messagebox.showinfo(
                title='Filter to DBF',
                message=''.join(('"',
                                 dbfname,
                                 '"\n\nis not a dBase file (*.dbf)')))
            return
        fields = self.get_selected_fields_in_file(dbfname)
        dbfdata = self.zippeddata.filters[dbfname].to_dbf(discard=fields)
        savefile = tkinter.filedialog.asksaveasfilename(
            title='Save filtered DBF file',
            defaultextension='.dbf',
            filetypes=(
                ('dBase files', '*.dbf'),
                ),
            initialfile=''.join((os.path.splitext(dbfname)[0], 'edited')),
            initialdir='~')
        if savefile:
            open(savefile, 'wb').write(dbfdata)

    def filter_to_dbf(self, event=None):
        """Write to DBF file after removing data in selected fields."""
        tr = self.text.tag_ranges(_FILENAMECURSOR)
        if tr:
            self._filter_to_dbf(tr)

    def filter_to_dbf_command(self):
        """Write to DBF file after removing data in selected fields."""
        x, y = self.__xy
        ti = self.text.index(''.join(('@', str(x), ',', str(y))))
        self._filter_to_dbf(self.text.tag_prevrange(_FILENAMETAG, ti))

    def _filter_to_csv(self, tag_ranges):
        """Write to CSV file after removing data in selected fields."""
        if not tag_ranges:
            return
        dbfname = self.text.get(*tag_ranges)
        if not self.zippeddata.filters[dbfname].is_dbf_format:
            tkinter.messagebox.showinfo(
                title='Filter to CSV',
                message=''.join(('"',
                                 dbfname,
                                 '"\n\nis not a dBase file (*.dbf)')))
            return
        fields = self.get_selected_fields_in_file(dbfname)
        try:
            csvdata = self.zippeddata.filters[dbfname].to_csv(discard=fields)
        except UnicodeDecodeError:
            try:
                csvdata = self.zippeddata.filters[dbfname].to_csv(
                    encoding='iso-8859-1',
                    discard=fields)
            except UnicodeDecodeError:
                tkinter.messagebox.showinfo(
                    title='Filter to CSV',
                    message=''.join(('"',
                                     dbfname,
                                     '"\n\ncannot be decoded using codec ',
                                     'iso-8859-1')))
                return
        savefile = tkinter.filedialog.asksaveasfilename(
            title='Save filtered DBF file as CSV',
            defaultextension='.csv',
            filetypes=(
                ('CSV files', '*.csv'),
                ),
            initialfile=''.join((os.path.splitext(dbfname)[0], 'edited')),
            initialdir='~')
        if savefile:
            open(savefile, 'w', encoding='utf-8').write(csvdata)

    def filter_to_csv(self, event=None):
        """Write to CSV file after removing data in selected fields."""
        tr = self.text.tag_ranges(_FILENAMECURSOR)
        if tr:
            self._filter_to_csv(tr)

    def filter_to_csv_command(self):
        """Write to CSV file after removing data in selected fields."""
        x, y = self.__xy
        ti = self.text.index(''.join(('@', str(x), ',', str(y))))
        self._filter_to_csv(self.text.tag_prevrange(_FILENAMETAG, ti))

    def filter_and_copy_to_zip_archive(self, event=None):
        """Select or deselect field at cursor for removal from file."""
        if self.original_zip_password_protected:
            if not tkinter.messagebox.askokcancel(
                title='Save filtered archive as ZIP',
                message=''.join(
                    ('Save files extracted from ZIP quoting a password to ',
                     'ZIP without password protection.',
                     ))):
                return
        zipfilename = tkinter.filedialog.asksaveasfilename(
            title='Save filtered archive as ZIP',
            defaultextension='.zip',
            filetypes=(
                ('Zip files', '*.zip'),
                ),
            initialdir='~')
        if not zipfilename:
            return
        selected_files = self.get_selected_files()
        archive = zipfile.ZipFile(zipfilename, 'w')
        for f in self.zippeddata.filenames:
            if f in selected_files:
                continue
            if self.zippeddata.filters[f].is_dbf_format:
                fields = self.get_selected_fields_in_file(f)
                filedata = self.zippeddata.filters[f].to_dbf(discard=fields)
            else:
                filedata = self.zippeddata.contents[f]

            # At 29 January 2017 the commented statement fills the archive of
            # the file with nul bytes. www.stackoverflow.com/questions/32671170
            # suggested the ZipInfo workaround to get the same effect as just
            # giving the file name.
            #archive.writestr(f, filedata, compress_type=zipfile.ZIP_DEFLATED)
            archive.writestr(
                zipfile.ZipInfo(f, datetime.datetime.now().timetuple()[:6]),
                filedata,
                compress_type=zipfile.ZIP_DEFLATED)
            
        archive.close()
        tkinter.messagebox.showinfo(
            title='Save filtered archive as ZIP',
            message=''.join(('"',
                             zipfilename,
                             '"\n\narchive written.')))

    def close_url(self, event=None):
        """Close the URL."""
        if not tkinter.messagebox.askokcancel(
            title='Close URL',
            message='Please confirm close URL'):
            return
        self.zippeddata.close()
        self.zippeddata = None
        self.text.delete('1.0', tkinter.END)
        self.text.insert(tkinter.END, _START_TEXT)
        self.dbftext.delete('1.0', tkinter.END)
        self.set_menu_and_entry_events_for_edit_url(False)
        self.set_menu_and_entry_events_for_open_url(True)

    def set_menu_and_entry_events_for_open_url(self, active):
        """Turn events for opening a URL on if active is True otherwise off."""
        menu = self.menu
        if active:
            menu.add_separator()
            menu.add_command(label='Open or Download',
                             command=self.open_or_download_file,
                             accelerator='Alt F4')
            menu.add_command(label='Browse',
                             command=self.browse_localhost_file,
                             accelerator='Alt F5')
            menu.add_separator()
            menu.add_command(label='Help',
                             command=self.show_help,
                             accelerator='F1')
            menu.add_separator()
        else:
            menu.delete(0, tkinter.END)
        menu = self.dbf_menu
        if active:
            menu.add_separator()
            menu.add_command(label='Help',
                             command=self.show_help,
                             accelerator='F1')
            menu.add_separator()
        else:
            menu.delete(0, tkinter.END)
        for entry in (self.text, self.dbftext):
            self._bind_for_scrolling_only(entry)
        for entry in (self.entry, self.text, self.dbftext):
            entry.bind('<KeyPress-F1>',
                       '' if not active else self.show_help)
            entry.bind('<Alt-KeyPress-F5>',
                       '' if not active else self.browse_localhost_file)
            entry.bind('<Alt-KeyPress-F4>',
                       '' if not active else self.open_or_download_file)
            entry.bind('<KeyPress-Return>',
                       '' if not active else self.open_or_download_file)

    def set_menu_and_entry_events_for_edit_url(self, active):
        """Turn events for editing a URL on if active is True otherwise off."""
        menu = self.menu
        if active:
            menu.add_separator()
            menu.add_command(label='Prior Field',
                             command=self.prior_field_tag,
                             accelerator='F7')
            menu.add_command(label='Next Field',
                             command=self.next_field_tag,
                             accelerator='F8')
            menu.add_command(label='(De)select Current Field',
                             command=self.select_current_field,
                             accelerator='F9')
            menu.add_command(label='Prior File',
                             command=self.prior_file_tag,
                             accelerator='Alt F3')
            menu.add_command(label='Next File',
                             command=self.next_file_tag,
                             accelerator='Alt F4')
            menu.add_command(label='(De)select Current File',
                             command=self.select_current_file,
                             accelerator='Alt F9')
            menu.add_separator()
            menu.add_command(label='Filter to Zip Archive',
                             command=self.filter_and_copy_to_zip_archive,
                             accelerator='F10')
            menu.add_separator()
            menu.add_command(label='Close URL',
                             command=self.close_url,
                             accelerator='F3')
            menu.add_separator()
            menu.add_command(label='Help',
                             command=self.show_help,
                             accelerator='F1')
            menu.add_separator()
        else:
            menu.delete(0, tkinter.END)
        menu = self.dbf_menu
        if active:
            menu.add_separator()
            menu.add_command(label='Clear',
                             command=self.clear_dbf_as_csv,
                             accelerator='F6')
            menu.add_separator()
            menu.add_command(label='Help',
                             command=self.show_help,
                             accelerator='F1')
            menu.add_separator()
        else:
            menu.delete(0, tkinter.END)
        for entry in (self.text, self.dbftext):
            self._bind_for_scrolling_only(entry)
        for entry in (self.entry, self.text, self.dbftext):
            entry.bind('<KeyPress-F1>',
                       '' if not active else self.show_help)
            entry.bind('<KeyPress-F7>',
                       '' if not active else self.prior_field_tag)
            entry.bind('<KeyPress-F8>',
                       '' if not active else self.next_field_tag)
            entry.bind('<KeyPress-F9>',
                       '' if not active else self.select_current_field)
            entry.bind('<Alt-KeyPress-F7>',
                       '' if not active else self.prior_file_tag)
            entry.bind('<Alt-KeyPress-F8>',
                       '' if not active else self.next_file_tag)
            entry.bind('<Alt-KeyPress-F9>',
                       '' if not active else self.select_current_file)
            entry.bind('<Alt-KeyPress-F3>',
                       '' if not active else self.close_url)
            entry.bind('<KeyPress-F11>',
                       '' if not active else self.filter_to_dbf)
            entry.bind('<KeyPress-F12>',
                       '' if not active else self.filter_to_csv)
            entry.bind('<KeyPress-F2>',
                       '' if not active else self.extract_original)
            entry.bind('<KeyPress-F10>',
                       '' if not active else
                       self.filter_and_copy_to_zip_archive)
        for entry in (self.entry, self.text):
            entry.bind('<KeyPress-F6>',
                       '' if not active else self.show_dbf_as_csv)
        for entry in (self.dbftext,):
            entry.bind('<KeyPress-F6>',
                       '' if not active else self.clear_dbf_as_csv)

    def show_help(self, event=None):
        """"""
        if self.__help:
            return

        def clear_help(event=None):
            self.__help = None
            
        self.__help = tkinter.Toplevel(master=self.root)
        self.__help.wm_title('Help - Filter fields in zipped DBF files')
        self.__help.wm_resizable(width=tkinter.FALSE, height=tkinter.FALSE)
        self.__help.bind('<Destroy>', clear_help)
        text = tkinter.Text(master=self.__help, wrap=tkinter.WORD)
        scrollbar = tkinter.ttk.Scrollbar(
            master=self.__help,
            orient=tkinter.VERTICAL,
            command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        text.pack(fill=tkinter.BOTH)
        try:
            help_text = open(os.path.join(os.path.dirname(__file__), _HELP)
                             ).read()
        except:
            help_text = 'Unable to read help file'
        self._bind_for_scrolling_only(text)
        text.insert(tkinter.END, help_text)

    def _bind_for_scrolling_only(self, widget):
        """"""
        widget.bind('<KeyPress>', 'break')
        widget.bind('<Home>', 'return')
        widget.bind('<Left>', 'return')
        widget.bind('<Up>', 'return')
        widget.bind('<Right>', 'return')
        widget.bind('<Down>', 'return')
        widget.bind('<Prior>', 'return')
        widget.bind('<Next>', 'return')
        widget.bind('<End>', 'return')


if __name__=='__main__':

    Filter().root.mainloop()
