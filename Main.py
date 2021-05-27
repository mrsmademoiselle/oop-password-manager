#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = "Franziska Loof, 307583"

from tkinter import ttk
from idlelib.tooltip import Hovertip
from Edit import *
from New import *

# TBD:
# - Database-Encryption with master password
# - Bugfix: Bug at the bottom of the Main.py file
# - Visual scrollbar: to indicate that scrolling is possible


class Main(ttk.Frame):
    """Class that handles the main window"""

    def __init__(self, main_window):
        """Constructor to build the main frame"""

        self.tree = None
        self.selected_row_id = ""
        self.hide_btn = None
        self.entries_label = None

        initialize_db()
        main_window.title("Password-Manager")
        # center the displayed main frame
        main_window.geometry("1039x500+200+180")
        main_window.maxsize(1200, 500)

        for col in range(4):
            main_window.grid_columnconfigure(col, minsize=30)

        # frame for password-entry-list
        entry_list_frame = Frame(main_window, bd=15)
        entry_list_frame.place(rely=0.2, anchor="nw")

        # configure columns to display a prettier order of buttons
        for counter in range(9):
            main_window.columnconfigure(counter, uniform='column')

        # delete button
        delete_button = Button(main_window, text="Delete entry", bg="#753030", fg="white", command=self.delete)
        delete_button.grid(row=0, column=2, ipadx=5, ipady=5)
        Hovertip(delete_button, 'Delete the selected list entry.')

        # edit button
        edit_button = Button(main_window, text="Edit entry", bg="#8f6325", fg="white",
                             command=lambda: Edit(self.selected_row_id, self.read))
        edit_button.grid(row=0, column=1, ipadx=5, ipady=5)
        Hovertip(edit_button, 'Edit the selected list entry.')

        # add button
        add_btn = Button(main_window, text="New entry", bg="#4a7d4f", fg="white", command=lambda: New(self.read))
        add_btn.grid(row=0, column=0, ipadx=5, ipady=5, padx=(15, 0))
        Hovertip(edit_button, 'Add a new entry to the list.')

        # search box
        self.search_box = Entry(main_window, width=30)
        self.search_box.grid(row=0, columnspan=2, column=8, ipadx=5, ipady=5, padx=(15, 0))

        # search button
        search_btn = Button(main_window, text="Search", command=self.search_entries)
        search_btn.grid(row=0, column=10, ipady=3, pady=10)
        Hovertip(search_btn, 'Search entries for the input.')

        # button to delete any search filters and show all elements
        delete_filters = Button(main_window, text="×", command=self.clear_search, fg="red", font='sans 13 bold')
        delete_filters.grid(row=0, columnspan=2, column=11, padx=5)
        Hovertip(delete_filters, 'Delete all search filters')

        # copy button
        copy_btn = Button(main_window, text="Copy password",
                          command=lambda: self.copy_to_clipboard(self.selected_row_id))
        copy_btn.grid(row=1, column=8,ipady=5, columnspan=2)
        Hovertip(copy_btn, 'Copy password of selected entry to clipboard.')

        # "hide and show passwords" button
        self.hide_btn = Button(main_window, text="Hide passwords", command=lambda: self.read(False))
        self.hide_btn.grid(row=1, column=9, ipady=5, columnspan=2)
        Hovertip(self.hide_btn, 'Show/Hide passwords in clear text.')

        # password box
        self.entries_label = Label(entry_list_frame, anchor="nw", justify="left")
        self.entries_label.grid(row=1, column=1)

        # at the end of the frontend-configuration, read all the entries from the database
        self.read(False)

    def clear_search(self):
        """deletes all search filters"""

        self.search_box.delete(0, END)
        self.read(False)

    def search_entries(self):
        """reads all entries from the database that match the terms and prints them into the table"""

        search_term = self.search_box.get()

        if search_term:
            results = search_entries(search_term)
            self.hide_btn.configure(text="Show passwords", command=lambda: self.read(True))
            self.create_table(results, False)
        else:
            self.read(False)

    def read(self, show=False):
        """reads all entries from the database and prints them into the table"""

        # clear the selected row, in case this is a callback-call from Edit
        self.selected_row_id = ""

        # change text and onclick-command of hide-button
        if bool(show):
            self.hide_btn.configure(text="Hide passwords", command=lambda: self.read(False))
        else:
            self.entries_label['text'] = ""
            self.hide_btn.configure(text="Show passwords", command=lambda: self.read(True))

        # read all entries
        # if search box isnt empty (= search filter on),
        # use search results instead of all entries
        search_term = self.search_box.get()
        if search_term:
            entries = search_entries(search_term)
        else:
            entries = read_from_database()

        self.create_table(entries, show)

    def create_table(self, entry_list, show):

        # create table
        cols = ('NO.', 'TITLE', 'URL', 'USERNAME', 'PASSWORD')
        self.tree = ttk.Treeview(self.entries_label, columns=cols, show='headings')
        self.tree.grid(row=1, column=0, columnspan=1)

        # onclick event on table row to copy paste password
        self.tree.bind('<ButtonRelease-1>', self.get_selected_row)

        # fill in table headers
        for col in cols:
            self.tree.heading(col, text=col)

        # fill in table rows
        if len(entry_list) > 0:
            for entry in entry_list:
                self.tree.insert("", "end",
                                 values=(entry[4], entry[0], entry[1], entry[2],
                                         entry[3] if show else "**********"))
        else:
            self.tree.insert("", "end", values=("No entries found.", "", "", "", ""))

    def delete(self):
        """Deletes the selected entry-row from the database"""

        id_param = self.selected_row_id

        # if a row has been selected
        if id_param != "":

            # if entry exists in database
            if read_one_from_database(id_param):
                success = delete_entry(str(id_param))
                if success:
                    self.read(False)
                    messagebox.showinfo("Alert", "Entry with ID {} has successfully been deleted.".format(id_param))
                    self.selected_row_id = ""
            else:
                messagebox.showinfo("Alert", "No entry with ID '{}' found.".format(id_param))
                self.selected_row_id = ""
        else:
            messagebox.showinfo("Alert", "Please select the entry you want to delete.")

    def get_selected_row(self, event):
        """reads the row the user has clicked on and stores the item-id internally"""

        current_item = self.tree.focus()
        row_array = self.tree.item(current_item, 'values')

        # necessary, in case someone taps on the table headers
        if row_array != "":
            # save id for delete/edit-process
            self.selected_row_id = row_array[0]

    def copy_to_clipboard(self, id_to_copy):
        """copies the stored id to the clipboard.
        Is used to edit an entry or copy the password from a selected row.."""

        # temporary window to store input on
        temp = Tk()
        temp.withdraw()
        temp.clipboard_clear()

        id_of_item = self.selected_row_id

        # if a row has been selected
        if id_of_item != "":
            try:
                # should return one item only
                entries = read_one_from_database(id_of_item)
                # item is wrapped in a list, therefore we need to call [0] before we select the value.
                temp.clipboard_append(entries[0][3])
                temp.update()
            except Exception:
                print("Entry with id {} not found in database.".format(id_of_item))
        else:
            messagebox.showinfo("Alert", "Please select an entry to copy the password from.")

        temp.destroy()


root = Tk()
gui = Main(root)
root.mainloop()
# following line fixed a bug, where the main window would reopen itself upon x-ing it
# However, the line also triggers following Exception upon x-ing the window:
# '_tkinter.TclError: can't invoke "destroy" command: application has been destroyed'
root.destroy()
