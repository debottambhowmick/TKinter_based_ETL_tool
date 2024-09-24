from tkinter import *
from tkinter import ttk
# Home Page Frame
from ETL_gui_app.pages.home import HomePage
# Delimiter handle page
from ETL_gui_app.pages.delimiter_handle import DelimiterPage
# Theme Page Frame
from ETL_gui_app.pages.theme import ThemePage



class MultiPageApp(Tk):
    def __init__(self):
        super().__init__()

        self.title("ETL GUI FREE TOOL [v:0.001]")
        self.geometry('750x600')

        # Initialize the style
        self.style = ttk.Style()
        self.configure_styles()

        # Create a container to hold all the pages
        container = Frame(self)
        container.pack(fill="both", expand=True)

        # Make the container resizable
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Dictionary to keep track of pages
        self.frames = {}

        for F in (HomePage, ThemePage, DelimiterPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Stack all the pages on top of each other
            frame.grid(row=0, column=0, sticky='nswe')

        # Show the home page first
        self.show_frame('HomePage')

    def configure_styles(self):
        # Configure the style for ttk.Button
        self.style.configure('TButton', font=('helvetica', 10), relief='flat',padding=5)
        
        # Configure the style for ttk.Label
        self.style.configure('TLabel', font=('helvetica', 10))

    def show_frame(self, page_name):
        """Bring the frame with the given page_name to the top"""
        frame = self.frames[page_name]
        frame.tkraise()
    
    def quit_app(self):
        self.quit()


if __name__ == '__main__':
    app = MultiPageApp()
    app.mainloop()
