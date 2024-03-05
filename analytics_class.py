# Class to analyse data
import pandas as pd

class Load_Excel:
    
    # initalise object with file path and data
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        
    # reads file and creates pandas dataframe (.data)
    def read_file(self, name = None):
        try:
            if self.file_path.endswith('.xlsx'):
                self.data = pd.read_excel(self.file_path)
            elif self.file_path.endswith('.csv'):
                self.data = pd.read_csv(self.file_path)
            else:
                raise ValueError('Unsupported file type.')
        except Exception as e:
            print(f"Something went wrong. Error {e}")
        
    # Sets all string values to lowercase for consistency
    def set_lowercase(self):
        for column in self.data.columns:
            for i in range(len(self.data)):
                try:
                    self.data[column][i] = self.data[column][i].lower()
                    # This could be done better here, but there are mixed string entries and numbers, so we don't want to log failed values
                    # for every single non-pure string. 
                except:
                    pass
        
