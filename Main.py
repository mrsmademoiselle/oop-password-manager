from tkinter import ttk
from idlelib.tooltip import Hovertip
from Edit import *
from New import *

# TBD:
# - Database-Encryption with master password
# - Fix Password-Label-Height
# - Fix Bug at the bottom


class Main(ttk.Frame):
    """Class that handles the main window"""

    def __init__(self, main_window):
        """Constructor to build the main frame"""

        self.tree = None
        self.selected_row_id = ""
        self.hide_btn = None
        self.entries_label = None

        initialize_db()
        # main frame
        main_window.title("Password-Manager")
        main_window.geometry("600x500")
        main_window.minsize(1039, 500)
        main_window.maxsize(1200, 500)

        for col in range(4):
            main_window.grid_columnconfigure(col, minsize=30)

        for row in range(9):
            main_window.grid_rowconfigure(row, minsize=10)

        # all entries
        entry_list_frame = Frame(main_window, bd=7)
        entry_list_frame.place(rely=0.2, relwidth=1, anchor="nw")

        # configure column-frontend for main window
        for counter in range(9):
            main_window.columnconfigure(counter, uniform='column')

        delete_button = Button(main_window, text="Delete entry", bg="#753030", fg="white", command=self.delete)
        delete_button.grid(row=0, column=2, ipadx=5, ipady=5)
        Hovertip(delete_button, 'Delete selected entry of list.')

        edit_button = Button(main_window, text="Edit entry", bg="#8f6325", fg="white",
                             command=lambda: Edit(self.selected_row_id, self.read))
        edit_button.grid(row=0, column=1, ipadx=5, ipady=5)
        Hovertip(edit_button, 'Edit selected entry of list.')

        # add button
        add_btn = Button(main_window, text="New entry", bg="#4a7d4f", fg="white", command=lambda: New(self.read))
        add_btn.grid(row=0, column=0, ipadx=5, ipady=5, padx=(15, 0))
        Hovertip(edit_button, 'Add a new entry to the list.')

        copy_btn = Button(main_window, text="copy pw",
                          command=lambda: self.copy_to_clipboard(self.selected_row_id))
        copy_btn.grid(row=0, column=8, ipadx=5, ipady=5)
        Hovertip(copy_btn, 'Copy password of selected entry to clipboard.')

        # hide and show button
        self.hide_btn = Button(main_window, text="Hide entries", command=lambda: self.read(False))
        self.hide_btn.grid(row=0, column=9, ipadx=5, ipady=5)
        Hovertip(self.hide_btn, 'Show/Hide passwords in clear text.')

        # password box
        self.entries_label = Label(entry_list_frame, anchor="nw", justify="left")
        self.entries_label.grid(row=1, column=1)

        self.read(False)

    def read(self, show=False):
        """reads all entries from the database and prints them into the table"""

        # clear the string, in case this is a callback from Edit
        self.selected_row_id = ""

        # change hide-buttons onclick-command
        if bool(show):
            self.hide_btn.configure(text="Hide entries", command=lambda: self.read(False))
        else:
            self.entries_label['text'] = ""
            self.hide_btn.configure(text="Show entries", command=lambda: self.read(True))

        entries = read_from_database()

        # create table
        cols = ('NR.', 'TITLE', 'URL', 'USERNAME', 'PASSWORD')

        self.tree = ttk.Treeview(self.entries_label, columns=cols, show='headings')
        self.tree.grid(row=1, column=0, columnspan=1)

        # onclick event on table row to copy paste password
        self.tree.bind('<ButtonRelease-1>', self.get_selected_row)

        # fill table headers
        for col in cols:
            self.tree.heading(col, text=col)

        # fill table rows
        if len(entries) > 0:
            for entry in entries:
                self.tree.insert("", "end",
                                 values=(entry[4], entry[0], entry[1], entry[2],
                                         entry[3] if show else "**********"))
        else:
            self.tree.insert("", "end", values=("No entries found.", "", "", "", ""))

    def delete(self):
        """Deletes the selected entry-row from the database"""

        id_param = self.selected_row_id
        if id_param != "":
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

        # temporary window to store input on and destroy
        temp = Tk()
        temp.withdraw()
        temp.clipboard_clear()
        id_of_item = self.selected_row_id

        if id_of_item != "":
            try:
                entries = read_one_from_database(id_of_item)
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
# fix to a bug, where the main window reopened itself upon close
# TBD: triggers _tkinter.TclError: can't invoke "destroy" command: application has been destroyed
root.destroy()