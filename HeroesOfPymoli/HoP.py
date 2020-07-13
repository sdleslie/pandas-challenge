# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)

#--------------------------------------
# Player Count
# Set players to count rows
# Create dataframe with one summary field
players_df = pd.DataFrame({"Total Players":[players]})
players_df

#--------------------------------------
## Purchasing Analysis (Total)
# Calculate Summary Stats
# unique_items = len(purchase_data['Item ID'].unique())
# unique_players = len(purchase_data['SN'].unique())

purchases = purchase_data['Item ID'].count()
unique_items = purchase_data['Item ID'].nunique(dropna=True)
player_count = purchase_data['SN'].nunique(dropna=True)

# average_price = purchase_data.groupby('Price').mean()
average_price = purchase_data['Price'].mean()
total_revenue = purchase_data['Price'].sum()
summary_df = pd.DataFrame({'Number of Unique Items':[unique_items],
#                           'Player Count': [player_count],
                           'Average Price': [average_price],
                           'Number of Purchases':[purchases],
                           'Total Revenue':[total_revenue]})
summary = summary_df.style.format({'Average Price':'${:.2f}','Total Revenue':'${:,.2f}'})
summary

#--------------------------------------
## Gender Demographics
gender_df = purchase_data.groupby(['Gender'])
player_total = purchase_data['SN'].nunique(dropna=True)
player_count = gender_df['SN'].nunique(dropna=True)
percent_gender = player_count / player_total
gender_summary = pd.DataFrame({'Total Count':player_count,'Percentage of Players':percent_gender})
gender_summary = gender_summary.sort_values('Total Count',ascending=False)
gender_summary = gender_summary.style.format({'Percentage of Players':'{:.2%}'})
gender_summary

#--------------------------------------
## Purchasing Analysis (Gender)
gender_df = purchase_data.groupby(['Gender'])
purchase_count = gender_df['Purchase ID'].count()
player_total = purchase_data['SN'].nunique(dropna=True)
player_count = gender_df['SN'].nunique(dropna=True)
average_price = gender_df['Price'].sum() / gender_df['Purchase ID'].count()
# Sum the pices by gender and divide by the number of unique customers by gender
total_price_per = gender_df['Price'].sum() / player_count
gender_df = pd.DataFrame({'Purchase Count':purchase_count
                           ,'Average Purchase Price':average_price
                           ,'Avg Total Purchase/Person':total_price_per})
gender_df = gender_df.sort_values('Purchase Count',ascending=False)
gender_df = gender_df.style.format({'Average Purchase Price':   '${:,.2f}',
                                        'Avg Total Purchase/Person':'${:,.2f}'})
gender_df

#--------------------------------------
## Purchasing Analysis (Age) - Bins Setup
bins = [0,9.9,14,19,24,29,34,39,100]
bin_names = ['<10','10-14','15-19','20-24','25-29','30-34','35-39','40+']
purchase_data['Age Group'] = pd.cut(purchase_data['Age'], bins, labels=bin_names)
age_groups = purchase_data.groupby('Age Group')
#--------------------------------------
## Age Demographics
player_total = purchase_data['SN'].nunique(dropna=True)
player_count = age_groups['SN'].nunique(dropna=True)
percent_players = player_count/player_total
age_df = pd.DataFrame({'Total Count':player_count,
                       'Percentage of Players':percent_players})
age_df['Percentage of Players'] = age_df['Percentage of Players'].map('{:,.2%}'.format)

#--------------------------------------
## Purchasing Analysis (Age) - calculations and output
purchase_count = age_groups['Purchase ID'].count()
player_count = age_groups['SN'].nunique(dropna=True)
average_price = age_groups['Price'].sum() / age_groups['Purchase ID'].count()
total_purchase = age_groups['Price'].sum()
# Sum the pices by gender and divide by the number of unique customers by age group
total_purchase_per = age_groups['Price'].sum() / player_count

purch_age_df = pd.DataFrame({'Purchase Count':purchase_count
                      ,'Average Purchase Price':average_price
                      ,'Total Purchase Value':total_purchase
                      ,'Avg Total Purchase/Person':total_purchase_per})

purch_age_df = purch_age_df.style.format({'Average Purchase Price':   '${:,.2f}',
                                          'Total Purchase Value':     '${:,.2f}',
                                          'Avg Total Purchase/Person':'${:,.2f}'})
purch_age_df

#--------------------------------------
## Top Spenders
# Solution 2 - map to do formatting, this one is cleaner
player_df = purchase_data.groupby(['SN'])
purchase_count = player_df['Purchase ID'].count()
total_purchases = player_df['Price'].sum()
# player_total = purchase_data['SN'].nunique(dropna=True)
average_price = player_df['Price'].sum() / player_df['Purchase ID'].count()

player_df = pd.DataFrame({'Purchase Count':purchase_count
                         ,'Average Purchase Price':average_price
                         ,'Total Purchase Value':total_purchases
                         })

player_df = player_df.sort_values('Total Purchase Value',ascending=False)

player_df['Average Purchase Price'] = player_df['Average Purchase Price'].map('${:,.2f}'.format)
player_df['Total Purchase Value']   = player_df['Total Purchase Value'].map('${:,.2f}'.format)

player_df.head()

#--------------------------------------
## Most <Attribute> Items Setup
# Set up the Dataframe
item_df = purchase_data.loc[:,['Item ID','Item Name','Price']]
item_df = item_df.groupby(['Item ID','Item Name'])
purchase_count = item_df['Item ID'].count()
total_purchases = item_df['Price'].sum()
price = item_df['Price'].mean()
average_price = item_df['Price'].sum() / purchase_count
item_df = pd.DataFrame({'Purchase Count':purchase_count
                       ,'Item Price':price
                       ,'Total Purchase Value':total_purchases
                         })
#--------------------------------------
## Most Popular Items
# Sort by Purchase Count and format
item_df1 = item_df.sort_values('Purchase Count',ascending=False)
item_df1['Purchase Count']         = item_df1['Purchase Count'].map('{:,.0f}'.format)
item_df1['Item Price']             = item_df1['Item Price'].map('${:,.2f}'.format)
item_df1['Total Purchase Value']   = item_df1['Total Purchase Value'].map('${:,.2f}'.format)

item_df1.head()
#--------------------------------------
## Most Profitable Items
# Sort by Total Purchase Value and format
item_df2 = item_df.sort_values('Total Purchase Value',ascending=False)

item_df2['Purchase Count']         = item_df2['Purchase Count'].map('{:,.0f}'.format)
item_df2['Item Price']             = item_df2['Item Price'].map('${:,.2f}'.format)
item_df2['Total Purchase Value']   = item_df2['Total Purchase Value'].map('${:,.2f}'.format)

item_df2.head()