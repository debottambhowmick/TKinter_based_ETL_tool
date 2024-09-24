from tkinter import *
from tkinter import ttk, messagebox
import csv



class DelimiterPage(Frame):
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

        # Delimiter change frame
        self.delimiter_change = Frame(self, relief="solid", borderwidth=1)
        self.delimiter_change.pack(fill="both", expand=True, padx=50, pady=50)

        # Input file settings
        self.input_frame = ttk.Labelframe(self.delimiter_change, text="Input File Settings", padding=10)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

        self.input_file_lbl = ttk.Label(self.input_frame, text='Input file path:')
        self.input_file_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.input_file_entry = ttk.Entry(self.input_frame)
        self.input_file_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.input_encoding_lbl = ttk.Label(self.input_frame, text="Input Encoding:")
        self.input_encoding_lbl.grid(row=1, column=0, padx=5, pady=15, sticky="w")

        self.input_encoding = ttk.Combobox(self.input_frame, values=["UTF-8", "ISO-8859-1", "ASCII"], state="readonly")
        self.input_encoding.set("UTF-8")
        self.input_encoding.grid(row=1, column=1, padx=5, pady=15, sticky="ew")

        self.input_delimiter_lbl = ttk.Label(self.input_frame, text="Input Delimiter:")
        self.input_delimiter_lbl.grid(row=1, column=2, padx=5, pady=20, sticky="w")

        self.input_delimiter = ttk.Combobox(self.input_frame, values=[",", ";", "|", "\t"], state="readonly")
        self.input_delimiter.set(",")
        self.input_delimiter.grid(row=1, column=3, padx=5, pady=20, sticky="ew")

        # Output file settings
        self.output_frame = ttk.Labelframe(self.delimiter_change, text="Output File Settings", padding=10)
        self.output_frame.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

        self.output_file_lbl = ttk.Label(self.output_frame, text='Output file path:')
        self.output_file_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.output_file_entry = ttk.Entry(self.output_frame)
        self.output_file_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.output_encoding_lbl = ttk.Label(self.output_frame, text="Output Encoding:")
        self.output_encoding_lbl.grid(row=1, column=0, padx=5, pady=15, sticky="w")

        self.output_encoding = ttk.Combobox(self.output_frame, values=["UTF-8", "ISO-8859-1", "ASCII"], state="readonly")
        self.output_encoding.set("UTF-8")
        self.output_encoding.grid(row=1, column=1, padx=5, pady=15, sticky="ew")

        self.output_delimiter_lbl = ttk.Label(self.output_frame, text="Output Delimiter:")
        self.output_delimiter_lbl.grid(row=1, column=2, padx=5, pady=20, sticky="w")

        self.output_delimiter = ttk.Combobox(self.output_frame, values=[",", ";", "|", "\t"], state="readonly")
        self.output_delimiter.set(",")
        self.output_delimiter.grid(row=1, column=3, padx=5, pady=20, sticky="ew")

        # Set equal column weight for expanding the input fields
        self.input_frame.columnconfigure(1, weight=1)
        self.input_frame.columnconfigure(3, weight=1)
        self.output_frame.columnconfigure(1, weight=1)
        self.output_frame.columnconfigure(3, weight=1)

        # Change Delimiter Button
        change_btn = ttk.Button(self.delimiter_change, text="Change Delimiter", command=self.change_delimiter)
        change_btn.grid(row=2, column=0, sticky='nsew', padx=20, pady=10)

        # Make the delimiter_change frame expand with window resizing
        self.delimiter_change.grid_rowconfigure(0, weight=1)
        self.delimiter_change.grid_rowconfigure(1, weight=1)
        self.delimiter_change.grid_rowconfigure(2, weight=0)  # Change button row doesn't need to expand
        self.delimiter_change.grid_columnconfigure(0, weight=1)

    def change_delimiter(self):
        try:
            input_file = self.input_file_entry.get()
            input_encoding = self.input_encoding.get()
            input_delimiter = self.input_delimiter.get()

            output_file = self.output_file_entry.get()
            output_encoding = self.output_encoding.get()
            output_delimiter = self.output_delimiter.get()

            if input_delimiter == "\\t":
                input_delimiter = "\t"
            if output_delimiter == "\\t":
                output_delimiter = "\t"

            try:
                with open(input_file, 'r', encoding=input_encoding) as infile:
                    reader = csv.reader(infile, delimiter = input_delimiter)
                    data = list(reader)
            except FileNotFoundError:
                messagebox.showerror(title="File Not Found Error!!", message="File not found in the path, Please check the path carefully")
                return
            except UnicodeDecodeError:
                messagebox.showerror(title="Encoding Error!!", message="The input encoding You have choosen is not compatible with the csv file")
                return
            except Exception as e:
                messagebox.showerror("Unexpected Error", f"An unexpected error occurred while writing the file: {e}")
                return
               
            try:
                with open(output_file, 'w' ,encoding=output_encoding) as outfile:
                    writer = csv.writer(outfile, delimiter=output_delimiter)
                    writer.writerows(data)           
            except IOError:
                messagebox.showerror(title="Write Error!!", message="An error occuerd while writing the output file. Please check if you have the write permission or if the file is in use") 
                return
            except Exception as e:
                messagebox.showerror("Unexpected Error", f"An unexpected error occurred while writing the file: {e}")
                return
            messagebox.showinfo(title="Success", message=f"File has been successfully saved to: {output_file}")
        except EXCEPTION as e:
            messagebox.showerror(title="Unexpected Error!!", message=f'exception raised: {e}')
