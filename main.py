import pathlib
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *


class Main:
    def __init__(self):
        # Path
        self.path_to_saves = pathlib.Path("saves")
        self.TITLE = self.path_to_saves / "_titles_.txt"
        self.EXCEPTIONS = self.path_to_saves / "_exceptions_.txt"

        if not self.path_to_saves.is_dir():
            self.path_to_saves.mkdir(parents=True, exist_ok=True)
        self.check_path(self.TITLE, True)
        self.check_path(self.EXCEPTIONS, True)

        # Initialize window
        self.master = tk.Tk()
        # Set window size
        self.master.geometry("500x500")
        # Plain text printed
        self.label_1 = tk.Label(self.master, text="Here you can add new title").pack()

        # Entry widget
        self.entry = Entry(self.master, font=("Ariel", 16))
        self.entry.pack(padx=10, pady=5, fill=tk.X)

        self.title_choices = []
        self.combobox_1 = Combobox(
            self.master, font=("Ariel", 16), values=sorted(self.title_choices)
        )
        self.combobox_1.pack(pady=50, padx=10, fill=tk.X)
        self.update_combobox()

        # self.edit_button = Button(self.master, text="Edit").place(x=300, y=80)
        self.add_title = Button(self.master, text="Add", command=self.add_new_title)
        self.add_title.place(width=100, height=30, x=60, y=67)

        self.op_title = Button(
            self.master,
            text="Open",
            command=lambda: self.open_link(
                path=self.path_to_saves / (self.combobox_1.get().rstrip() + ".txt")
            ),
        )

        self.op_title.place(width=100, height=30, x=200, y=160)

        self.rmv_title = Button(self.master, text="Remove", command=self.remove_title)
        self.rmv_title.place(width=100, height=30, x=60, y=160)
        # mainloop, runs infinitely
        self.master.mainloop()

    def change_state(self, widget, disabled=False):
        widget["state"] = "disabled" if disabled else "normal"

    def open_link(self, text=None, path=None):
        def delete_link():
            try:
                text = lb.get(*lb.curselection())
                if messagebox.askyesno(
                    "Delete link", f'Are you sure you want to delete "{text}"'
                ):
                    # Making the path to the file and removing it
                    p = self.path_to_saves / (text + ".txt")
                    p.unlink(missing_ok=True)
                    # Removing link from the listbox
                    lb.delete(lb.curselection())

            except TypeError:
                messagebox.showwarning(
                    "Deleting link", "Select the link before trying to delete it!"
                )

        def load_links(text, title):
            data_dic = {}

            with open(self.EXCEPTIONS, "r") as txt:
                data = txt.read().splitlines()

            for el in data:
                if el:
                    el_list = el.split(",")
                    data_dic[el_list[0].strip()] = [x.strip() for x in el_list[1:]]

            for name in self.path_to_saves.glob("*.txt"):
                name = name.stem.lower()
                if name != title:
                    if name in text.lower():
                        lb.insert(0, name)
                    elif name in data_dic:
                        for v in data_dic[name]:
                            if v in text.lower():
                                if v not in lb.get(0, "end"):
                                    lb.insert(0, name)
                                    break

        def load_exceptions():
            try:
                self.lb_cur_sel = lb.get(*lb.curselection())
                data_dic = {}

                with open(self.EXCEPTIONS, "r") as txt:
                    data = txt.read().splitlines()

                for el in data:
                    if el:
                        el_list = el.split(",")
                        data_dic[el_list[0].strip()] = [x.strip() for x in el_list[1:]]

                if self.lb_cur_sel in data_dic:
                    eb.delete(0, tk.END)
                    eb.insert(tk.END, *data_dic[self.lb_cur_sel])
                else:
                    eb.delete(0, tk.END)
            except TypeError:
                pass

        def add_exception():
            data_dic = {}
            if messagebox.askyesno("Add exception", "Do you want to add exception?"):
                try:
                    entry_text = ex.get().lower().strip()
                    link_text = lb.get(*lb.curselection()).lower().strip()

                    if entry_text and link_text:
                        # Reading from txt file
                        with open(self.EXCEPTIONS, "r") as txt:
                            data = txt.read().splitlines()

                        # Storing data in dicionary
                        for el in data:
                            if el:
                                el_list = el.split(",")
                                data_dic[el_list[0].strip()] = [
                                    x.strip() for x in el_list[1:]
                                ]

                        if link_text in data_dic:
                            if (
                                entry_text not in data_dic[link_text]
                                and entry_text != link_text
                            ):
                                data_dic[link_text] += [entry_text]
                            else:
                                messagebox.showinfo(
                                    "Exception",
                                    "Exception exists or exception is a link",
                                )
                        else:
                            data_dic[link_text] = [entry_text]

                        with open(self.EXCEPTIONS, "w") as txt:
                            for key, values in data_dic.items():
                                txt.write(f"{key}, {', '.join(values)}\n")
                    ex.delete(0, tk.END)
                    load_exceptions()
                except TypeError:
                    messagebox.showwarning(
                        "Add exception",
                        "Please select the link to add exceptions to it!",
                    )

        def remove_exception():
            data_dic = {}
            if messagebox.askyesno(
                "Remove exception", "Do you want to remove exception?"
            ):
                try:
                    exception_sel = eb.get(*eb.curselection()).lower().strip()
                    if exception_sel:
                        # Reading from txt file
                        with open(self.EXCEPTIONS, "r") as txt:
                            data = txt.read().splitlines()

                        # Storing data in dicionary
                        for el in data:
                            if el:
                                el_list = el.split(",")
                                data_dic[el_list[0].strip()] = [
                                    x.strip() for x in el_list[1:]
                                ]

                    if exception_sel in data_dic[self.lb_cur_sel]:
                        data_dic[self.lb_cur_sel] = [
                            el
                            for el in data_dic[self.lb_cur_sel]
                            if el != exception_sel
                        ]

                    data_dic = {k: v for k, v in data_dic.items() if v}

                    with open(self.EXCEPTIONS, "w") as txt:
                        for key, values in data_dic.items():
                            txt.write(f"{key}, {', '.join(values)}\n")

                    eb.delete(*eb.curselection())
                except TypeError:
                    messagebox.showwarning(
                        "Remove exception", "Please select the exception to remove it!"
                    )

        def edit_exception():
            if messagebox.askyesno("Edit exception", "Do you want to edit exception?"):
                try:
                    ex.delete(0, tk.END)
                    ex.insert(0, eb.get(*eb.curselection()).lower().strip())
                    add_ex.config(text="Save", command=edit_save_exception)
                    self.edit = True
                except TypeError:
                    messagebox.showwarning(
                        "Remove exception", "Please select the exception to edit it!"
                    )

        def edit_save_exception():
            data_dic = {}
            if messagebox.askyesno("Save exception", "Do you want to save exception?"):
                try:
                    exception_sel = eb.get(*eb.curselection()).lower().strip()

                    if exception_sel:
                        # Reading from txt file
                        with open(self.EXCEPTIONS, "r") as txt:
                            data = txt.read().splitlines()

                        # Storing data in dicionary
                        for el in data:
                            if el:
                                el_list = el.split(",")
                                data_dic[el_list[0].strip()] = [
                                    x.strip() for x in el_list[1:]
                                ]

                    if exception_sel in data_dic[self.lb_cur_sel]:
                        data_dic[self.lb_cur_sel][
                            data_dic[self.lb_cur_sel].index(exception_sel)
                        ] = (ex.get().lower().strip())

                    with open(self.EXCEPTIONS, "w") as txt:
                        for key, values in data_dic.items():
                            txt.write(f"{key}, {', '.join(values)}\n")

                    ex.delete(0, tk.END)
                    load_exceptions()
                except TypeError:
                    self.edit = False
                    messagebox.showwarning(
                        "Save exception",
                        "Please select the exception to which to edit it!",
                    )
            else:
                ex.delete(0, tk.END)
                add_ex.config(text="Add", command=add_exception)

        def create_link():
            def contain(item):
                iscontain = item.strip().lower() in lb.get(0, "end")
                return iscontain

            try:
                # Selected text
                text = tb.get("sel.first", "sel.last")
                if not contain(text):
                    lb.insert("end", text.strip().lower())
            except tk.TclError:
                messagebox.showwarning(
                    "Select text error",
                    "Cant create a link!\nSelect text and try again!",
                )

        def save():
            if messagebox.askyesno("Save", "Do you want to save?"):
                with open(path, "w") as txt:
                    txt.write(tb.get("1.0", tk.END))
                nw.destroy()

        def recursive_call():
            try:
                text = lb.get(*lb.curselection())
                self.open_link(text)
            except TypeError:
                messagebox.showwarning(
                    "Open link", "Select the link and try open again!"
                )

        self.edit = False
        self.lb_cur_sel = None
        if not path:
            path_text = text.strip()
            path = self.path_to_saves / (path_text + ".txt")
        if self.check_path(path, True):
            nw = tk.Toplevel(self.master)
            nw.title(path.stem)
            nw.geometry("1000x500")
            # Grid configuration
            nw.columnconfigure(0, weight=4)
            nw.columnconfigure(1, weight=1)
            nw.rowconfigure((0, 1), weight=10)
            nw.rowconfigure((2, 3), weight=1)

            # Text widget and config
            self.state = "normal"
            tb = tk.Text(nw, font=("arial", 10), state=self.state)
            tb.grid(row=0, column=0, padx=10, pady=10, rowspan=3, sticky="nswe")

            # Reading from txt, saving to variable
            with open(path, "r") as txt:
                data = txt.read()

            # Inserting text into text widget
            tb.insert(("1.0"), data)
            tb["state"] = "disabled"

            # Listbox and config
            lb = tk.Listbox(
                nw, selectmode="single", font=("arial", 10), exportselection=False
            )
            lb.grid(row=0, column=1, padx=(0, 10), pady=(9, 30), sticky="nswe")

            # Loading links to link manager "TOP LISTBOX"
            load_links(data, path.stem)
            # When selected in link manager "TOP LISTBOX" loads exceptions to exception manager "BOTTOM LISTBOX"
            lb.bind("<<ListboxSelect>>", lambda e: load_exceptions())

            # Exception listbox and config widget
            eb = tk.Listbox(
                nw, selectmode="single", font=("arial", 10), exportselection=False
            )
            eb.grid(row=1, column=1, padx=(0, 10), pady=(0, 1), sticky="nswe")

            # Entry widget and config widget (for adding, editing exceptions)
            ex = tk.Entry(nw, font=("arial", 13))
            ex.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky="nswe")

            # Edit button and config widget (changes state to "normal")(for text widget)
            edit = Button(
                nw,
                text="Edit",
                command=lambda: self.change_state(tb),
            )
            edit.grid(row=3, column=0, padx=10, pady=(2, 10), sticky="w")

            # Save button and config widget (saves text to a txt file)(for text widget)
            save_b = Button(nw, text="Save", command=save)
            save_b.grid(row=3, column=0, padx=100, pady=(2, 10), sticky="w")

            # Link button and config widget (saves link to a file and adds to link manager)
            # (usage:select the text in text widget and press "add link")
            link = Button(nw, text="Create Link", command=create_link)
            link.grid(row=3, column=0, padx=190, pady=(2, 10), sticky="w")

            # Opening link button and config widget (open link from link manager)
            op_link = Button(nw, text="Open", command=recursive_call)
            op_link.grid(row=0, column=1, padx=30, pady=3, sticky="ws")

            # Delete link and config widget
            del_link = Button(nw, text="Delete", command=delete_link)
            del_link.grid(row=0, column=1, padx=40, pady=3, sticky="es")

            # Add, Edit, Remove exception and config widgets
            # Add_ex : add exception to ex.manager and saves to a txt file
            # Edit_ex : edits existing exception, adds to ex.manager, edited in txt file
            # Remove_ex: removes exception from ex.manager and txt file
            add_ex = Button(nw, text="Add", command=add_exception)
            add_ex.grid(row=3, column=1, pady=(0, 10), sticky="w")

            edit_ex = Button(nw, text="Edit", command=edit_exception)
            edit_ex.grid(row=3, column=1, padx=(0, 8.5), pady=(0, 10))

            remove_ex = Button(nw, text="Remove", command=remove_exception)
            remove_ex.grid(row=3, column=1, padx=(0, 10), pady=(0, 10), sticky="e")

        else:
            messagebox.showwarning("Opening Error", "Opening file error")

    def check_path(self, path, create_file=False):
        if not path.exists():
            if path.stem != ".txt":
                if create_file:
                    path.touch(exist_ok=True)
                    return True
                else:
                    return False
        else:
            return True

    def add_new_title(self):
        if self.entry.get():
            if messagebox.askyesno(message="Are you sure you want to add this title?"):
                # Appending text to a file
                self.lines = []
                with open(self.TITLE, "r") as fp:
                    self.lines = fp.readlines()

                if self.entry.get() + "\n" not in self.lines:
                    self.lines.append(self.entry.get() + "\n")
                    with open(self.TITLE, "w") as title:
                        for l in sorted(self.lines):
                            title.write(l.lower())

                self.entry.delete(0, tk.END)
                self.update_combobox()

    def remove_title(self):
        if messagebox.askyesno(
            "Remove?", "Are you sure you want to remove this title?"
        ):
            # Save file
            self.lines = []
            with open(self.TITLE, "r") as fp:
                self.lines = fp.readlines()

            # Text to remove
            text = self.combobox_1.get()

            # Remove title and txt file
            for num, title in enumerate(self.lines):
                if text == title:
                    f_path = self.path_to_saves / f"{text.rstrip()}.txt"
                    if f_path.exists() and messagebox.askyesno(
                        "File remove",
                        "Do you want to remove file? Removing file would remove all the content PERMANENTLY!",
                    ):
                        f_path.unlink()

                    del self.lines[num]
                    break

            # Write file without the text
            with open(self.TITLE, "w") as fp:
                for line in sorted(self.lines):
                    fp.write(line)

            self.combobox_1.delete(0, tk.END)
            self.combobox_1["values"] = []
            self.update_combobox()

    def update_combobox(self):
        # Reading text from a file and adding to the combobox widget
        with open(self.TITLE, "r") as title:
            for t in title:
                if t not in self.combobox_1["values"]:
                    self.combobox_1["values"] = (*self.combobox_1["values"], t)


if __name__ == "__main__":
    Main()
