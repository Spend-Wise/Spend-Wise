from tkinter import END

class EntryPlaceholderManager:
    def __init__(self, entry, placeholder=None):
        self.entry = entry
        self.placeholder = placeholder

        entry.configure(text_color="gray")
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", self.on_focus_in)
        entry.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, END)
            self.entry.configure(text_color=('black', 'white'))

    def on_focus_out(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, self.placeholder)
            self.entry.configure(text_color="gray")
