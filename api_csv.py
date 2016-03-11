from os.path import isfile
from parameters import SEP

class CSV(object):
    def __init__(self, filename):
        """ Params
                filename: string """
        self.filename = filename
      
    def _file_exists(self):
        """ Checks if the file exists (True) or not (False).
            Returns
                Boolean """
        return isfile(self.filename)
                
    def _file_empty(self):
        """ Checks if the file is emptied (True) or not (False).
            Returns
                empty: Boolean """
        empty = True
        f = self._retry_file()
        if f.readline():
            empty = False
        f.close()
        return empty
    
    def check_file(self):
        """ Checks if the file exists or if the file is empty.
            Raises
                UnknownSecretID """
        if not self._file_exists():
            raise Exception(self.filename+" does not exist.")
        if self._file_empty():
            raise Exception(self.filename+" does not contain any entry.")
    
    def _retry_file(self, mode='rb'):
        """ Tries to open the file, and will wait for the user to press Enter 
            before retrying if the opening did not work. 
            This is especially useful if another program is using the CSV file.
            Params
                mode: string """
        while True:
            try:
                return open(self.filename, mode)
            except IOError as e:
                print "The following error occurred when trying to access "+self.filename+" :"+str(e)
                print self.filename+" is probably opened by another program, please close it."
                raw_input('PRESS ENTER TO CONTINUE')
            
    def write_legend(self, legend):
        """ Writes the legend to the CSV file if it is not present already. """
        if not self._file_exists():
            f = self._retry_file('wb')
            f.write(legend+'\n')
            f.close()
        elif self._file_empty():
            f = self._retry_file('wb')
            f.write(legend)
            f.close()
    
    def write_new_rows(self, rows):
        """ Writes new rows to the CSV file.
            Params
                rows: list of strings """
        f = self._retry_file('ab')
        for row in rows:
            f.write(row+'\n')
        f.close()

    def read_data_rows(self):
        self.check_file()
        f = self._retry_file()
        rows = f.read().split('\n')[1:] #1 to remove legend
        f.close()
        matrix2D = [row.split(SEP[0]) for row in rows][:-1] #to remove end of line
        for row in matrix2D:
            row[-1] = row[-1][:-1] #removes the \r
        return matrix2D