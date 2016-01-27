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
    def __init__(self):
        self.X_coord
        self.X_start
        self.X_end
        self.X_points
        self.Y_coord
        self.Y_start
        self.Y_end
        self.Y_points
        self.Z_coord
        self.Z_start
        self.Z_end
        self.Z_points

        self.start_comments = ""
        self.end_comments = ""

        self.id = self.generate_id()

    def generate_id(self):
        pass
        # returns the previous experiments id+1

    def parameter_space():
        pass
        # return array to be passed as argument for parfor

    def save_dat(self, raw_data):
        pass
        # puts all the data into a .dat file that can be read by spyview
        # !!! in the final directory

    def spyview(self):
        pass
        # generates meta.txt file so that spyview can understand the data

    def ask_for_comments(self):
        pass
        # ask user to enter comments prior to simulation
        # include a "pass" with a fast keyboard shortcut
        # return comments

    def open_spyview(self):
        pass

    def generate_spyview_meta(self):
        pass
        # spyview_..._.meta.txt

    def ask_for_comments_and_png(self):
        """
        Should be possible to 
            have no comments and but a png
            have comments and no png
            discard simulation
        """
        pass
        # return comments

    def save_meta(self, t_start, t_stop):
        """
        In a JSON file, store:
            timing information
            settings
            global information from global.JSON
            start and end comments


        !!! in the final directory
        """
        pass


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

    def run(self,parfunc):
        # start timer #
        self.start_comments = self.ask_for_comments()
        raw_data = parfor(parfunc,self.parameter_space())
        self.save_dat(raw_data)
        self.generate_spyview_meta()
        self.open_spyview()
        # end timer #
        self.end_comments = self.ask_for_comments_and_png()
        self.save_meta(t_start,t_stop)
        self.log_on_ppt()
