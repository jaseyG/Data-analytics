# Purchase Behaviour Analysis
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from analytics_class import Load_Excel as le # Basic class to read files and convert into dataframe
from time import perf_counter

pd.options.mode.chained_assignment = None

test_size = 100

# To ensure files are read properly
def check_read(file_name):
    if file_name.data is not None:
        print(f'Data has loaded for {file_name}')
    else:
        print('Data is empty, something probably went wrong.')

# Initialising the spreadsheets
td = le(file_path = r'C:/Users/Lololong/Desktop/Programming/Work Stuff/Quantium_Forage/QVI_transaction_data.xlsx')
le.read_file(td)
check_read(td)
le.set_lowercase(td)

pb = le(file_path = r'C:/Users/Lololong/Desktop/Programming/Work Stuff/Quantium_Forage/QVI_purchase_behaviour.csv')
le.read_file(pb)
check_read(pb)
le.set_lowercase(pb)

# Data valiation, each will be custom
pb_values = {'LYLTY_CRD_NBR': int, 'LIFESTAGE' : ["young singles/couples", "new families", "midage singles/couples", "retirees", "older families",
                                  "older singles/couples", "young families"],
                   'PREMIUM_CUSTOMER' : ["premium", "mainstream", "budget"]}

failed_rows = {}
# Validate purchase behaviour dataframe
for index, row in pb.data.iterrows():
    if not isinstance(row['LYLTY_CARD_NBR'], int) or row['LIFESTAGE'] not in pb_values['LIFESTAGE'] or row['PREMIUM_CUSTOMER'] not in pb_values['PREMIUM_CUSTOMER']:
        failed_rows[index] = [row['LYLTY_CARD_NBR'], row['LIFESTAGE'], row['PREMIUM_CUSTOMER']]
        pb.data = pb.data.drop(index, axis = 0) 

