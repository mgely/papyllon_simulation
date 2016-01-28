import os
from utility import byteify,gen_timestamp
from subprocess import Popen
from Tkinter import *
import ttk

class PapyllonSimulation(object):
    """
    - Provides default functions useful in simulations:
        - Spyview compatible files
        - 2D plotting (+background)
        - parralelising functions
    - Provides a way to archive all simulations
        - ask for user to write comments prior and after simulation has run
        - ask user to generate a good png that is representative of the simulation
        - Log everything in a power point       

    """
    def __init__(self,path, settings_list):
        with open("global.json","r") as f:
            self.global_setup =  byteify(json.load(f))


        self.arg_list = settings_variables +
            ['X_name','X_coord','X_start','X_end','X_points',
            'Y_name','Y_coord','Y_start','Y_end','Y_points',
            'Z_name','Z_coord','Z_start','Z_end','Z_points']
        self.load_settings()

        self.start_commentsgithub = ""
        self.end_comments = ""

        self.ask_for_setup_info()
        generate_relevant_paths()

    def generate_relevant_paths(self,path):

        # Extract relevant paths
        manager_path = os.path.split(__file__)[0]
        scripts_path = os.path.split(path)[0]
        simulation_type_path = os.path.split(scripts_path)[0]

        # Generate stamp
        stamp = ""
        stamp += gen_timestamp()
        stamp += "__"

        self.script_name = os.path.split(path)[1].split('.')[0]
        stamp += self.script_name
        stamp += "__"

        stamp += self.detail

        # Fill in relevant paths
        self.settings_file_path = os.path.join(manager_path,"settings.json")
        self.simulation_data_path = os.path.join(simulation_type_path,"data",stamp)
        self.spyview_path = self.global_setup["spyview_path"]
        
    def set_parameters(self,p):
        setattr(self, X_name, p[0])
        setattr(self, Y_name, p[1])
        setattr(self, Z_name, p[2])

    def load_settings(self):
        with open(self.settings_file_path,"r") as f:
            settings =  byteify(json.load(f)) # to parse unicodes to strings

        # Apply specified settings
        for arg in self.arg_list:
            try:
                value = settings[arg]
            except:
                raise KeyError('No value for argument '+arg+' found in arg_list')

            setattr(self, arg, value)

    def parameter_space():
        parameter_space = []
        for X in np.linspace(X_start,X_end,X_coord):
            for Y in np.linspace(Y_start,Y_end,Y_coord):
                for Z in np.linspace(Z_start,Z_end,Z_coord):
                    parameters.append([X,Y,Z])
        return parameter_space

    def save_dat(self, raw_data): 
        filename = os.path.join(self.simulation_data_path,
                                "output.dat")
        output = np.c_[parameters, data]
        np.savetxt(filename, output)

    def ask_for_comments(self):
        root = Tk()
        root.title("Comments?")
        root.lift()
        mainframe = ttk.Frame(root,padding = (3,3,3,3))
        mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S))

        mainframe.columnconfigure(0,weight = 1)
        mainframe.rowconfigure(0,weight = 1)

        ttk.Label(mainframe,
            text = "Please enter comments for the logging powerpoint..."
            ).grid(column = 0, row = 0, sticky = E)

        comments_entry = Text(mainframe,
            height = 13,
            font = ("Arial", "9"))
        comments_entry.grid(column = 0, row = 0, sticky = (W, E))

        ttk.Button(mainframe,
            text = "Done",
            command = root.destroy
            ).grid(column = 0, row = 1)
        root.mainloop()

        root.bind('<Return>',root.destroy)

        return str(comments_entry.get("1.0",'end-1c'))

    def open_spyview(self):
        filename = os.path.join(self.simulation_data_path,
                                "output.dat")
        p = Popen([self.spyview_path,filename])

    def generate_spyview_meta(self):
        filename = os.path.join(self.simulation_data_path,
                                "output.meta.txt")
        with open(filename,'w') as meta:
            meta.write("#inner loop"+"\n")
            meta.write(str(X_points)+"\n")
            meta.write(str(X_start)+"\n")
            meta.write(str(X_end)+"\n")
            meta.write(X_coord+"\n")
            meta.write("#outer loop"+"\n")
            meta.write(str(Y_points)+"\n")
            meta.write(str(Y_start)+"\n")
            meta.write(str(Y_end)+"\n")
            meta.write(Y_coord+"\n")
            meta.write("#outer most loop"+"\n")
            meta.write(str(Z_points)+"\n")
            meta.write(str(Z_start)+"\n")
            meta.write(str(Z_end)+"\n")
            meta.write(Z_coord+"\n")
            meta.write("#values"+"\n")
            meta.write(str(1)+"\n")
            meta.write("Computed"+"\n")
        pass

    def ask_for_png(self):
        
        root = Tk()
        root.title("Waiting for png...")
        root.lift()
        mainframe = ttk.Frame(root,padding = (3,3,3,3))
        mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S))

        mainframe.columnconfigure(0,weight = 1)
        mainframe.rowconfigure(0,weight = 1)

        ttk.Label(mainframe,
            text = "Please generate a png file for the logging powerpoint..."
            ).grid(column = 0, row = 0, sticky = E)

        ttk.Button(mainframe,
            text = "Done",
            command = root.destroy
            ).grid(column = 0, row = 1)
        root.mainloop()

        root.bind('<Return>',root.destroy)

    def save_meta(self, t_start, t_stop):
        """
        In a JSON file, store:
            timing information
            settings
            global information from global.JSON
            start and end comments
        """
        filename = os.path.join(self.simulation_data_path,
                                "meta.json")
        with open(filename,"w") as f:
            json.dump(self.__dict__, f, sort_keys=True, indent=4, separators=(',', ': '))

    def log_on_ppt(self):
        """
        In order of importance, include:
            filename/id
            png 
            settings
            before-after comment
            timing
        """
        pass

    def ask_for_setup_info(self):
                
        entry_width = 60

        root = Tk()
        root.title("Start simulation")
        root.lift()

        # Put a main frame in the root, which has a padding (NWES)
        mainframe = ttk.Frame(self.root,padding = (3,3,3,3))

        # Put it in column 0, row 0 of the root and have it stick 
        # to all sides upon resizing
        mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S))

        mainframe.columnconfigure(0,weight = 1)
        mainframe.rowconfigure(0,weight = 1)

        ttk.Label(mainframe,
            text = "Simulation detail: "
            ).grid(column = 0, row = 0, sticky = E)

        detail = StringVar()
        detail_entry = ttk.Entry(mainframe,
            width = entry_width,
            textvariable = self.detail)
        detail_entry.grid(column = 1, row = 0, sticky = (W, E))



        ttk.Label(mainframe,
            text = "Comments: "
            ).grid(column = 0, row = 1, sticky = E)

        comments_entry = Text(mainframe,
            height = 13,
            font = ("Arial", "9"))
        comments_entry.grid(column = 1, row = 1, sticky = (W, E))
        # To get text use: comments = comments_entry.get("1.0",'end-1c')


        ttk.Label(mainframe,
            text = "Data saved in .../simulation_type/data/(time_stamp)_script_detail"
            ).grid(columnspan = 2, row = 2, sticky = W)

        

        # Button that calls the function
        ttk.Button(mainframe,
            text = "Start",
            command = root.destroy
            ).grid(column = 2, row = 3, sticky = W)

        # # Keyboard shortcut for start
        root.bind('<Return>',root.destroy)

        # Configure all the widgets to have the same padding
        for child in mainframe.winfo_children():
            child.grid_configure(padx = 5, pady = 5)

        # Define where the cursor will be initially
        detail_entry.focus()

        # All of the expansion will happen in the middle when you expand
        # the window
        mainframe.columnconfigure(1,weight = 1)

        # Go
        root.mainloop()

        self.start_comments = str(comments_entry.get("1.0",'end-1c'))
        self.detail = str(detail.get())

    def generate_timing_info(self,t0,t1):

        self.start_str = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t0)))
        self.end_str = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t1)))
        self.duration = str(datetime.timedelta(seconds=t1 - t0))

        print "Started: "+start_str
        print "Ended: "+end_str
        print "Measurement time: "+duration

    def run(self,parfunc):
        t0 = time.time()
        raw_data = parfor(parfunc,self.parameter_space())
        self.save_dat(raw_data)
        self.generate_spyview_meta()
        self.open_spyview()
        t1 = time.time()
        self.generate_timing_info(t0,t1)
        self.end_comments = self.ask_for_comments()
        self.ask_for_png()
        self.save_meta()
        self.log_on_ppt()
