from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import messagebox
from database import *
from password_entry import Password_Entry


class Edit(Tk):
    """Class that handles the edit-entry-frame"""

    def __init__(self, id_to_edit, callback=None):
        """Constructor to build the edit frame"""
        self.selected_row_id = id_to_edit

        if id_to_edit != "":
            try:
                if read_one_from_database(id_to_edit):

                    self.edit = Toplevel()
                    self.edit.title("Edit entry")
                    self.edit.geometry("500x400")
                    self.edit.minsize(450, 300)
                    self.edit.maxsize(450, 300)

                    # Create Text Boxes
                    self.title_edit = Entry(self.edit, width=30)
                    self.title_edit.grid(row=0, column=1, padx=20)
                    self.url_edit = Entry(self.edit, width=30)
                    self.url_edit.grid(row=1, column=1, padx=20)
                    self.username_edit = Entry(self.edit, width=30)
                    self.username_edit.grid(row=2, column=1, padx=20)
                    self.password_edit = Entry(self.edit, width=30)
                    self.password_edit.grid(row=3, column=1, padx=20)

                    # Create Text Box Labels
                    self.title_label_edit = Label(self.edit, text="title:")
                    self.title_label_edit.grid(row=0, column=0)
                    self.url_label_edit = Label(self.edit, text="URL:")
                    self.url_label_edit.grid(row=1, column=0)
                    self.username_label_edit = Label(self.edit, text="Username:")
                    self.username_label_edit.grid(row=2, column=0)
                    self.password_label_edit = Label(self.edit, text="Password:")
                    self.password_label_edit.grid(row=3, column=0)

                    # Create Save Button
                    self.submit_btn_edit = Button(self.edit, text="Save entry", command=lambda: self.update(callback))
                    self.submit_btn_edit.grid(row=4, column=0, columnspan=2, pady=5, padx=15, ipadx=135)

                    records = read_one_from_database(id_to_edit)

                    for record in records:
                        self.title_edit.insert(0, record[0])
                        self.url_edit.insert(0, record[1])
                        self.username_edit.insert(0, record[2])
                        self.password_edit.insert(0, record[3])
                else:
                    messagebox.showinfo("Alert", "No entry '{}' found.".format(id_to_edit))
            except Exception:
                messagebox.showinfo("Alert", "Please select the entry you want to edit.")
        else:
            messagebox.showinfo("Alert", "Please select the entry you want to edit.")

    def update(self, callback=None):
        """Updates the entry with the new data"""

        if self.title_edit.get() != "" and self.password_edit.get() != "":
            entry = Password_Entry(self.title_edit.get(), self.password_edit.get(), self.url_edit.get(),
                                   self.username_edit.get(), self.selected_row_id)
            update_entry(entry)

            messagebox.showinfo("Info", "The entry has been updated in the database!")
            self.edit.destroy()
            selected_row_id = ""
            callback()

        else:
            messagebox.showinfo("Alert",
                                "You must at least type in a password and a title in order to create an entry.")
