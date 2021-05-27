#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = "Franziska Loof, 307583"

from tkinter import *
from tkinter import messagebox
from database import *
from passwordentry import PasswordEntry


class Edit(Tk):
    """Class that handles the edit-entry-frame"""

    def __init__(self, id_to_edit, callback=None):
        """Constructor to build the edit frame"""
        self.selected_row_id = id_to_edit

        if id_to_edit != "":
            try:
                if read_one_from_database(id_to_edit):

                    # main frame
                    self.edit = Toplevel()
                    self.edit.title("Edit entry")
                    self.edit.geometry("400x200+500+250")

                    # text fields
                    self.title_edit = Entry(self.edit, width=30)
                    self.title_edit.grid(row=0, column=1, padx=20)
                    self.url_edit = Entry(self.edit, width=30)
                    self.url_edit.grid(row=1, column=1, padx=20)
                    self.username_edit = Entry(self.edit, width=30)
                    self.username_edit.grid(row=2, column=1, padx=20)
                    self.password_edit = Entry(self.edit, width=30)
                    self.password_edit.grid(row=3, column=1, padx=20)
                    self.password_confirm_edit = Entry(self.edit, width=30)
                    self.password_confirm_edit.grid(row=4, column=1, padx=20)

                    # labels
                    self.title_label_edit = Label(self.edit, text="Title:")
                    self.title_label_edit.grid(row=0, column=0)
                    self.url_label_edit = Label(self.edit, text="URL:")
                    self.url_label_edit.grid(row=1, column=0)
                    self.username_label_edit = Label(self.edit, text="Username:")
                    self.username_label_edit.grid(row=2, column=0)
                    self.password_label_edit = Label(self.edit, text="Password:")
                    self.password_label_edit.grid(row=3, column=0)
                    self.password_confirm_label_edit = Label(self.edit, text="Confirm password:")
                    self.password_confirm_label_edit.grid(row=4, column=0, pady=(0, 20))

                    # save button
                    self.submit_btn_edit = Button(self.edit, text="Save entry", command=lambda: self.update(callback))
                    self.submit_btn_edit.grid(row=6, column=0, columnspan=2, pady=5, padx=15, ipadx=135)

                    # get selected entry from database
                    records = read_one_from_database(id_to_edit)

                    # fill textfields with data of selected entry
                    for record in records:
                        self.title_edit.insert(0, record[0])
                        self.url_edit.insert(0, record[1])
                        self.username_edit.insert(0, record[2])
                        self.password_edit.insert(0, record[3])
                else:
                    messagebox.showinfo("Alert", "No entry '{}' found.".format(id_to_edit))
            except Exception as exp:
                messagebox.showinfo("Alert", "Please select the entry you want to edit.")
                print(exp.with_traceback())
        else:
            messagebox.showinfo("Alert", "Please select the entry you want to edit.")

    def update(self, callback=None):
        """Updates the entry with the new data"""

        # entry must at least contain a title and a password
        if self.title_edit.get() != "" and self.password_edit.get() != "":

            # password-input and confirm-input must be the same
            if self.password_edit.get() == self.password_confirm_edit.get():

                # forge a PasswordEntry-Object out of input fields
                entry = PasswordEntry(self.title_edit.get(), self.password_edit.get(), self.url_edit.get(),
                                      self.username_edit.get(), self.selected_row_id)

                # update entry in database
                update_entry(entry)

                messagebox.showinfo("Info", "The entry has been updated in the database!")
                self.edit.destroy()
                self.selected_row_id = ""

                # callback is usually read() to update the list after editing an entry
                callback()
            else:
                title_label = Label(self.edit, fg="gray",
                                    text="The passwords must be the same.")
                title_label.grid(row=8, column=0, columnspan=3)

                self.password_edit.config(bg="#f08f89")
                self.password_confirm_edit.config(bg="#f08f89")

        else:
            messagebox.showinfo("Alert",
                                "You must at least type in a password and a title in order to create an entry.")
