from tkinter import *
from tkinter import ttk, messagebox


class ThemePage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Top button frame
        self.btn_frm = Frame(self, background='lightblue')
        self.btn_frm.pack(side="top", fill=X)

        # Buttons
        button1 = ttk.Button(self.btn_frm, text='Go to home page', style='TButton', command=lambda: controller.show_frame("HomePage"))
        button1.grid(row=0, column=0, padx=5, pady=5)

        button2 = ttk.Button(self.btn_frm, text="Quit", style='TButton', command=lambda: controller.quit_app())
        button2.grid(row=0, column=1, padx=5, pady=5)

        # setting page frame
        self.setting_frame = Frame(self)
        self.setting_frame.pack(fill='both', expand=True)

        # Apearnace setting layout
        appearance_label = ttk.Label(self.setting_frame, text="Appearance settings", font=('helvetica',24))
        appearance_label.pack(pady=(20,5))

        theme_label = ttk.Label(self.setting_frame, text="Select Theme")
        theme_label.pack(pady=5)

        self.theme_var = StringVar(value='vista')
        self.theme_menu = ttk.Combobox(self.setting_frame, textvariable=self.theme_var, values=['winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'], state="readonly")
        self.theme_menu.pack(pady=5)

        apply_theme_button = ttk.Button(self.setting_frame, text="apply", command=self.apply_theme)
        apply_theme_button.pack(pady=5)


    def apply_theme(self):

        selected_theme = self.theme_var.get()

        if selected_theme == 'winnative':
            self.controller.style.theme_use('winnative')
        elif selected_theme == 'clam':
            self.controller.style.theme_use('clam')
        elif selected_theme == 'alt':
            self.controller.style.theme_use('alt')
        elif selected_theme == 'default':
            self.controller.style.theme_use('default')
        elif selected_theme == 'classic':
            self.controller.style.theme_use('classic')
        elif selected_theme == 'vista':
            self.controller.style.theme_use('vista')
        elif selected_theme == 'xpnative':
            self.controller.style.theme_use('xpnative')

        messagebox.showinfo(message=f"{selected_theme} has been applied !!")
