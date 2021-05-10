import string
import random
from tkinter import *
from tkinter import messagebox
from database import *
from password_entry import Password_Entry


class New(Tk):
    """Class that handles the new-entry-frame"""

    def __init__(self, callback=None):
        """Constructor to build the new entry frame"""
        self.numbersVar = None
        self.add_window = Toplevel()
        self.add_window.title("Add new entry")
        self.add_window.minsize(1000, 300)
        self.add_window.maxsize(1000, 300)

        for c in range(4):
            self.add_window.columnconfigure(c, uniform='column')

        create = Label(self.add_window, text="Create password entry", font="Helvetica 12 bold")
        create.grid(row=0, column=1, pady=20)

        # Create Text Boxes
        self.title = Entry(self.add_window, width=30)
        self.title.grid(row=1, column=1, padx=20)

        self.url = Entry(self.add_window, width=30)
        self.url.grid(row=2, column=1, padx=20)

        self.username = Entry(self.add_window, width=30)
        self.username.grid(row=3, column=1, padx=20)

        self.password = Entry(self.add_window, width=30)
        self.password.grid(row=4, column=1, padx=15, pady=5)

        self.password_confirm = Entry(self.add_window, width=30)
        self.password_confirm.grid(row=5, column=1, padx=15, pady=(0, 20))

        self.title_label = Label(self.add_window, text="title:")
        self.title_label.grid(row=1, column=0)
        self.url_label = Label(self.add_window, text="url:")
        self.url_label.grid(row=2, column=0)
        self.username_label = Label(self.add_window, text="username:")
        self.username_label.grid(row=3, column=0)
        self.password_label = Label(self.add_window, text="password:")
        self.password_label.grid(row=4, column=0)
        self.password_confirm_label = Label(self.add_window, text="Confirm password:")
        self.password_confirm_label.grid(row=5, column=0, pady=(0, 20))

        # add button
        submit_btn = Button(self.add_window, text="Add entry", bg="#4a7d4f", fg="white",
                            command=lambda: self.add(callback))
        submit_btn.grid(row=6, column=1, ipadx=5, ipady=5)

        # cancel button
        cancel_button = Button(self.add_window, text="Cancel", bg="#666666", fg="white",
                               command=self.add_window.destroy)
        cancel_button.grid(row=6, column=0, ipadx=5, ipady=5)

        #
        # autogeneration
        #
        pw = Label(self.add_window, text="Autogenerate password", font="Helvetica 12 bold")
        pw.grid(row=0, column=3, pady=20)

        self.numbersVar = BooleanVar()
        numbers = Checkbutton(self.add_window, text='Numbers', variable=self.numbersVar)
        numbers.grid(row=1, column=3)

        self.special_var = BooleanVar()
        special_chars = Checkbutton(self.add_window, text='Special Chars', variable=self.special_var)
        special_chars.grid(row=2, column=3)

        self.title_label = Label(self.add_window, text="length:")
        self.title_label.grid(row=3, column=2, pady=(10, 0))

        self.length = Entry(self.add_window, width=30)
        self.length.grid(row=3, column=3, padx=20, pady=(10, 0))

        submit_btn = Button(self.add_window, text="Auto generate", bg="#4a7d4f", fg="white", command=self.autogen)
        submit_btn.grid(row=6, column=3, ipadx=5, ipady=5)

    def autogen(self):
        """Autogenerates a new password on command"""

        length_field = self.length.get()

        if length_field != "":
            if re.fullmatch("^[0-9]*$", length_field):
                self.password.delete(0, END)

                if self.numbersVar.get() and self.special_var.get():
                    text = ''.join(random.choice(string.ascii_uppercase + string.digits + string.punctuation)
                                   for _ in range(int(length_field)))
                elif self.numbersVar.get():
                    text = ''.join(
                        random.choice(string.ascii_uppercase + string.digits) for _ in range(int(length_field)))
                elif self.special_var.get():
                    text = ''.join(random.choice(string.ascii_uppercase + string.punctuation)
                                   for _ in range(int(length_field)))
                else:
                    text = ''.join(random.choice(string.ascii_uppercase) for _ in range(int(length_field)))

                self.password.insert(0, text)
                self.title_label = Label(self.add_window, fg="gray",
                                         text="The password has automatically been inserted. "
                                              "Please confirm the password manually.")
                self.title_label.grid(row=7, column=2, columnspan=4)
        else:
            self.title_label = Label(self.add_window, fg="gray",
                                     text="You must specify a length for the password.")
            self.title_label.grid(row=7, column=3, columnspan=3)

    def add(self, callback=None):
        """Adds a new entry with the given data to the database"""

        new_index = ''.join(random.choice(string.digits) for _ in range(int(12)))

        if self.password.get() == self.password_confirm.get():
            entry = Password_Entry(self.title.get(), self.password.get(), self.url.get(), self.username.get(),
                                   str(new_index))
            self.password.configure(highlightbackground='white', highlightcolor='white')
            self.password_confirm.configure(highlightbackground='white', highlightcolor='white')

            if entry.get_titel() != "" and entry.get_password() != "":
                add_to_database(entry)

                self.add_window.destroy()
                messagebox.showinfo("Info", "Entry has been added to the database!")
                callback()
            else:
                self.title_label = Label(self.add_window, fg="gray",
                                         text="""You must at least type in a password 
                                         and a title in order to create an entry.""")
                self.title_label.grid(row=8, column=0, columnspan=3)
        else:
            self.title_label = Label(self.add_window, fg="gray",
                                     text="The passwords must be the same.")
            self.title_label.grid(row=8, column=0, columnspan=3)

            self.password.config(bg="#f08f89")
            self.password_confirm.config(bg="#f08f89")
