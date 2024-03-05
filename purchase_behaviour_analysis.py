import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

# Create Pandas dataframe with QVI Purchase Data 
purchase_behaviour = pd.read_csv(r#File Path)

# Ensure you update this to set a consistent sample size for testing through the whole program
sample_size = 100

# Making all data lowercase for consistency
for column in purchase_behaviour.columns:
    for i in range(sample_size):
        try:
            purchase_behaviour[column][i] = purchase_behaviour[column][i].lower()
        except:
            pass

# Accepted values dict for validation
accepted_values = {'LIFESTAGE' : ["young singles/couples", "new families", "midage singles/couples", "retirees", "older families",
                                  "older singles/couples", "young families"],
                   'PREMIUM_CUSTOMER' : ["premium", "mainstream", "budget"]}

#Data Validation (tested in first 20 rows)
failed_rows = {} # just so I can verify that the data being removed is actually invalid
for index, row in purchase_behaviour.head(sample_size).iterrows():
    # Checks if any of the 3 required passes fail
    if not isinstance(row['LYLTY_CARD_NBR'], int) or row['LIFESTAGE'] not in accepted_values['LIFESTAGE'] or row['PREMIUM_CUSTOMER'] not in accepted_values['PREMIUM_CUSTOMER']:
        failed_rows[index] = [row['LYLTY_CARD_NBR'], row['LIFESTAGE'], row['PREMIUM_CUSTOMER']] # adds to dict so we can see the rows that failed
        purchase_behaviour = purchase_behaviour.drop(index, axis = 0) # removes the data
        
purchase_behaviour.reset_index(drop = True, inplace = True) # resets the index so gaps in data don't produce problems later
        
print('Failed Row Information:')
if not failed_rows:
    print('None. \n')
else:
    for index, info in failed_rows.items():
        print(f'Index: {index}, Info: {info}')

# Summarises each unique case of (lifestage, premium customer), listing the amount of occurences each case has ('Count')
grouped_data = purchase_behaviour.head(sample_size).groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER']).size().reset_index(name = 'Count')
total_pop = grouped_data['Count'].sum()

# Adds a column that represents the count as a percentage of the population
grouped_data['%'] = (grouped_data['Count'] / total_pop) * 100

# Plotting using Seaborn since it pairs well with pandas

# Simple count plot visulisation for the distribution of customer classification
sns.set_palette('bright') # colour scheme for aesthetics [deep, muted, bright, pastel, dark, colorblind]
ax = sns.countplot(x = 'PREMIUM_CUSTOMER', data = purchase_behaviour.head(sample_size), hue = 'PREMIUM_CUSTOMER') 
for p in ax.patches: # Puts the % of the sample_size that each type represents
    ax.annotate(f'{round(p.get_height()/sample_size * 100, 1)}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points')

plt.title("Distribution of Premium Customers")
plt.show()

# Count plot for lifestage distribution, with labels angled 45 degrees for readability and unique colours for aesthetics
ax = sns.countplot(x = 'LIFESTAGE', data = purchase_behaviour.head(sample_size), hue = 'LIFESTAGE')
for p in ax.patches:
    ax.annotate(f'{round(p.get_height()/sample_size * 100, 1)}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points')
plt.xticks(rotation = 45, ha = 'right')
plt.title('Distribution of Customer Lifestages')
plt.show()

