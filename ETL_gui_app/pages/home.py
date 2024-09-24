from tkinter import *
from tkinter import ttk, messagebox, filedialog
import time
import pandas as pd
from sqlalchemy import create_engine

class HomePage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tree = None
        self.scrollbar_x = None
        # Initialize a BooleanVar to track the checkbutton state
        self.checkbox_var = False

        # A frame for navigation menu buttons
        self.btn_frame1 = Frame(self, bg="light blue")
        self.btn_frame1.pack(side='top', fill=X)

        # Button to navigate to theme page
        self.button2 = ttk.Button(self.btn_frame1, text='Delimiter Handle', style='TButton', command=lambda: controller.show_frame("DelimiterPage"))
        self.button2.grid(row=0, column=0, padx=5, pady=5)

        # Button to navigate to theme page
        self.button2 = ttk.Button(self.btn_frame1, text='Goto theme page', style='TButton', command=lambda: controller.show_frame("ThemePage"))
        self.button2.grid(row=0, column=2, padx=5, pady=5)


        #Button to quit the app
        self.button3 = ttk.Button(self.btn_frame1, text="Quit", style='TButton', command=lambda:controller.quit_app())
        self.button3.grid(row=0,column=3, padx=5, pady=5)

        # Separate windows using PanedWindow
        self.panedwin1 = PanedWindow(self, height=300, width=600, orient=HORIZONTAL)
        self.panedwin1.pack(fill=BOTH, expand=True)

        # Defining separate frames for both windows
        frame1 = Frame(self.panedwin1, width=300, relief="solid")
        frame2 = Frame(self.panedwin1, width=300, relief='solid', borderwidth=1)

        self.panedwin1.add(frame1)
        self.panedwin1.add(frame2)

        # Extraction
        self.extract_frame = ttk.Labelframe(frame1, text="Extraction", padding=10)
        self.extract_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Label on top of the buttons
        self.extract_label = ttk.Label(self.extract_frame, text='No file selected', wraplength=250)
        self.extract_label.pack(pady=(0, 10))  # Add some space below the label

        # Create a frame for the buttons to appear side by side
        self.button_frame2 = Frame(self.extract_frame)
        self.button_frame2.pack()

        # "Select File" button on the left
        self.extract_button = ttk.Button(self.button_frame2, text='Select File', command=lambda: self.extract_data())
        self.extract_button.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # "Reset" button on the right
        self.reset_button = ttk.Button(self.button_frame2, text="Reset", command=lambda: self.etl_reset())
        self.reset_button.grid(row=0, column=1, padx=10, pady=5, sticky='w')


        # Create a frame to contain the treeview and scrollbar
        self.tree_frame = Frame(frame2)
        self.tree_frame.pack(fill=BOTH, expand=True)

        # -----------------Transform------------------------
        self.transform_frame = ttk.LabelFrame(frame1, text="Transform", padding=10)
        self.transform_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Transform options
        self.checkbox_frame = Frame(self.transform_frame)
        self.checkbox_frame.pack()

        # Variables for checkboxes
        self.drop_duplicates_var = BooleanVar(value=False)
        self.drop_na_var = BooleanVar(value=False)
        self.drop_column_var = BooleanVar(value=False)
        self.rename_column_var = BooleanVar(value=False)

        self.transform_drop_duplicate_chk = ttk.Checkbutton(self.checkbox_frame, text= "Drop Duplicates", takefocus=0, variable=self.drop_duplicates_var).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.transform_drop_duplicate_apply = ttk.Button(self.checkbox_frame,text="apply",command=lambda:self.apply_transform()).grid(row=0,column=1, padx=5, pady=2, sticky='w')

        self.transform_drop_na_chk = ttk.Checkbutton(self.checkbox_frame, text= "Drop NA values", takefocus=0, variable=self.drop_na_var).grid(row=1,column=0, padx=10, pady=5, sticky='w')
        self.transform_drop_na_apply = ttk.Button(self.checkbox_frame, text="apply",command=lambda:self.apply_transform()).grid(row=1,column=1, padx=5, pady=2, sticky='w') 

        self.tansform_drop_column_chk = ttk.Checkbutton(self.checkbox_frame, text= "Drop column", takefocus=0, variable=self.drop_column_var).grid(row=2,column=0, padx=10, pady=5, sticky='w')
        self.tansform_drop_column_apply = ttk.Button(self.checkbox_frame, text="apply", command=lambda:self.apply_transform()).grid(row=2,column=1, padx=5, pady=2, sticky='w')

        self.transform_rename_column_chk = ttk.Checkbutton(self.checkbox_frame, text= "Rename Column", takefocus=0,variable=self.rename_column_var).grid(row=3,column=0, padx=10, pady=5, sticky='w')
        self.transform_rename_column_apply = ttk.Button(self.checkbox_frame, text="apply", command=lambda:self.apply_transform()).grid(row=3,column=1, padx=5, pady=2, sticky='w')
        
        self.transform_button = ttk.Button(self.transform_frame, text="Apply Transformations", command=lambda:self.transform_data_preview())
        self.transform_button.pack()

        # -------------------Load------------------------------
        self.load_frame = ttk.LabelFrame(frame1, text="Load", padding=10)
        self.load_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        self.load_options = ttk.Combobox(self.load_frame,values=["save as csv", 'load to mysql', 'load to postgresql', 'load to mssql'], state='readonly')
        self.load_options.pack(pady=20)
        self.load_button = ttk.Button(self.load_frame, text="Save as CSV", command=lambda:self.load_data())
        self.load_button.pack()


        # Configure frame1 to be resizable
        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_rowconfigure(0, weight=1)
        frame1.grid_rowconfigure(1, weight=1)
        frame1.grid_rowconfigure(2, weight=1)

        # Configure frame2 to be resizable
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_rowconfigure(0, weight=1)

    def initialize_treeview(self, parent_frame):
        """Initialize Treeview and scrollbar"""
        if self.tree is None or self.scrollbar_x is None:
            # Create the Treeview widget
            self.tree = ttk.Treeview(parent_frame, columns=("data"), show='headings')

            # Create a horizontal scrollbar
            self.scrollbar_x = ttk.Scrollbar(parent_frame, orient=HORIZONTAL, command=self.tree.xview)
            self.tree.configure(xscrollcommand=self.scrollbar_x.set)

            # Pack scrollbar and treeview
            self.scrollbar_x.pack(side=BOTTOM, fill=X)
            self.tree.pack(fill=BOTH, expand=True)

    def update_treeview(self, df):
        """Update Treeview with new data and initialize if not created"""
        
        # Ensure Treeview is initialized before updating
        if not self.tree or not self.scrollbar_x:
            self.initialize_treeview(self.tree_frame)

        # Clear the existing data in Treeview
        if self.tree or self.scrollbar_x:
            for item in self.tree.get_children():
                self.tree.delete(item)
        
        # Update the columns
        self.tree["columns"] = list(df.columns)
        
        # Configure the Treeview column headings and set column width
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, stretch=False)  # Set fixed column width

        # Insert new data into the Treeview
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Adjust column widths after setting data (optional, but helps maintain uniformity)
        self.adjust_treeview_column_widths()

    def adjust_treeview_column_widths(self):
        """Optionally adjust column widths dynamically"""
        for col in self.tree["columns"]:
            self.tree.column(col, width=150)  # Set a default width, adjust if needed

    def extract_data(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("CSV files", "*.csv"), ("JSON file", "*.json")])
        if file_path:
            # Progress bar
            pb1 = ttk.Progressbar(self.extract_frame, orient=HORIZONTAL, length=300, mode='determinate')
            pb1.pack()
            for i in range(5):
                self.update_idletasks()
                pb1['value'] += 20
                time.sleep(1)
            pb1.destroy()
            self.extract_label.config(text=f"Selected {file_path}")

            # Load files into pandas dataframe
            if file_path.endswith(".csv"):
                self.df = pd.read_csv(file_path)
            elif file_path.endswith(".json"):
                self.df = pd.read_json(file_path)
            

            self.update_treeview(self.df)

    def load_data(self):
        load_option = self.load_options.get()
        if hasattr(self, 'df'):
            if load_option == "save as csv": 
                file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
                if file_path:
                    self.df.to_csv(file_path, index=False)
                    messagebox.showinfo("Save", f"Data saved to {file_path}")
            elif load_option == "load to mysql":
                self.load_to_mysql()
            elif load_option == "load to postgresql":
                messagebox.showinfo("Comming Soon !!")
            elif load_option == "load to mssql":
                messagebox.showinfo("comming soon!!")
        else:
            messagebox.showwarning("Error", "No data available. Please extract data first.")
        
    def load_to_mysql(self):
        popup_window = Toplevel(self)
        popup_window.title("Mysql database parameters")
        popup_window.geometry("280x200")
        
        self.option_frame = LabelFrame(popup_window,text="Mysql parameters to load the data", relief="solid", borderwidth=1)
        self.option_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.lbl1 = ttk.Label(self.option_frame,text="username:").grid(row=0,column=0,padx=5,pady=5)
        self.username = ttk.Entry(self.option_frame)
        self.username.grid(row=0, column=1, padx=5, pady=5,sticky='ew')

        self.lbl2 = ttk.Label(self.option_frame,text="password:").grid(row=1,column=0,padx=5,pady=5)
        self.password = ttk.Entry(self.option_frame, show="*")
        self.password.grid(row=1, column=1, padx=5,pady=5,sticky='ew')

        self.lbl3 = ttk.Label(self.option_frame,text="Host:").grid(row=2,column=0,padx=5,pady=5)
        self.host = ttk.Entry(self.option_frame)
        self.host.grid(row=2, column=1, padx=5,pady=5,sticky='ew')

        self.lbl4 = ttk.Label(self.option_frame,text="Database:").grid(row=3,column=0,padx=5,pady=5)
        self.database = ttk.Entry(self.option_frame)
        self.database.grid(row=3, column=1, padx=5,pady=5,sticky='ew')

        ok_button = ttk.Button(self.option_frame, text="ok", command=lambda:on_ok())
        ok_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        
        self.option_frame.rowconfigure(index=[0,1,2,3], weight=1)

        def on_ok():
            username = self.username.get()
            password = self.password.get()
            host = self.host.get()
            database = self.database.get()

            # checking for blank values 
            if not username or not password or not host or not database:
                messagebox.showerror(title="Input Error!!", message="All fileds are required")
                return
            try:
                connection = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')
                self.df.to_sql('laptops', con=connection, index=True, if_exists='replace')
                messagebox.showinfo(title="success!!", message="csv data uploaded to MySQL successfully!")
            except Exception as e:
                messagebox.showerror(title="Unexpected Error!!", message=f"There is an issue while making the connection {e}")
        self.wait_window(popup_window)


    def apply_transform(self):
        """Apply one selected transformation based on checkbox states."""
        if hasattr(self, 'df'):
            # Apply drop duplicates if the checkbox is checked
            if self.drop_duplicates_var.get():
                self.df.drop_duplicates(inplace=True)
                messagebox.showinfo("Transformation", "Removed duplicates")
            
            # Apply drop NA if the checkbox is checked
            elif self.drop_na_var.get():
                self.df.dropna(inplace=True)
                messagebox.showinfo("Transformation", "Removed NA values")
            
            # Apply drop specific columns if the checkbox is checked
            elif self.drop_column_var.get():
                columns_to_drop = self.get_selected_columns()  # Get selected columns
                if columns_to_drop:
                    self.df.drop(columns=columns_to_drop, inplace=True)
                    messagebox.showinfo("Transformation", f"Dropped columns: {', '.join(columns_to_drop)}")
                    print(columns_to_drop)
                else:
                    messagebox.showwarning("Error", "No columns selected to drop.")
            
            # Apply rename columns 
            elif self.rename_column_var.get():
                rename_mapping = self.get_rename_mapping()  # Get a dictionary of column renames
                if rename_mapping:
                    self.df.rename(columns=rename_mapping, inplace=True)
                    messagebox.showinfo("Transformation", f"Renamed columns: {rename_mapping}")
                else:
                    messagebox.showwarning("Error", "No columns provided to rename.")
            
            # Apply datatype changes if the checkbox is checked
            elif self.change_datatype_var.get():
                dtype_mapping = self.get_dtype_mapping()  # Get a dictionary of dtype changes
                if dtype_mapping:
                    self.df = self.df.astype(dtype_mapping)
                    messagebox.showinfo("Transformation", f"Changed datatypes: {dtype_mapping}")
            else:
                    messagebox.showwarning("Error", "Please check the option!!")
        else:
            messagebox.showwarning("Error", "No data available. Please extract data first.")

    def get_selected_columns(self):
        popup_window = Toplevel(self)
        popup_window.title("Column Selection")
        popup_window.geometry("200x300")
        heading = ttk.Label(popup_window, text="Select columns to drop")
        heading.grid(row=0, column=0, padx=5,pady=5)

        chk_var = {}
        for i,col in enumerate(self.df.columns):
            var = BooleanVar(value=False)
            chk = ttk.Checkbutton(popup_window,text=f"{col}",variable=var)
            chk.grid(row=i+1, column=0, padx=5, pady=2, sticky="nswe")
            chk_var[col] = var

        def on_ok():
            self.selected_columns = [col for col,var in chk_var.items() if var.get() is True ]
            popup_window.destroy()
                
        btn = ttk.Button(popup_window, text="ok", command=on_ok)
        btn.grid(row=len(self.df.columns)+1, column=0, padx=5, pady=5)

        self.wait_window(popup_window)
        return self.selected_columns


    def get_rename_mapping(self):
        popup_window = Toplevel(self)
        popup_window.title("Column Selection")
        popup_window.geometry("200x300")

        heading = ttk.Label(popup_window, text="Rename columns")
        heading.grid(row=0, column=0, padx=5,pady=5)
        
        column_vars = {col: StringVar(value=col) for col in self.df.columns}

        for i, col in enumerate(self.df.columns):
             lbl = ttk.Label(popup_window, text=f"{col}")
             lbl.grid(row=i+1, column=0, padx=5, pady=5)
             
             entry = ttk.Entry(popup_window, textvariable=column_vars[col])
             entry.grid(row=i+1, column=1, padx=5, pady=5)
       

        def on_ok():
            self.new_columns = {col:column_vars[col].get() for col in self.df.columns}
            popup_window.destroy()
                
        btn = ttk.Button(popup_window, text="ok", command=on_ok)
        btn.grid(row=len(self.df.columns)+1, column=0, padx=5, pady=5)

        self.wait_window(popup_window)
        return self.new_columns


    def transform_data_preview(self):
        if hasattr(self, 'df'):
            self.update_treeview(self.df)
        else:
            messagebox.showwarning("Error", "No data available. Please extract data first.")

    def etl_reset(self):
        if hasattr(self, 'df'):
            del self.df
            self.extract_label.config(text='No file selected')
            
            # Safely destroy the treeview and scrollbar if they exist
            if self.tree is not None:
                self.tree.destroy()
                self.tree = None  # Set to None after destroying
            if self.scrollbar_x is not None:
                self.scrollbar_x.destroy()
                self.scrollbar_x = None  # Set to None after destroying
        else:
            messagebox.showwarning(title="Error", message="No data available. Please extract data first.")