import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data extraction
data = pd.read_csv('https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv')

# Checking for missing values
# print(f"Missing values : {data.isnull().sum()}\n")
data = data.fillna("Unknown")

# Checking for duplicates and converting date in a consistent format
# print(f"Number of duplicates :{data.duplicated().sum()}\n")
data['date'] = pd.to_datetime(data['date'])

# Handling inconsistent data
data['address'] = data['address'].str.title()
data['city'] = data['city'].str.title()
data['county'] = data['county'].str.title()
data['category_name'] = data['category_name'].str.title()
data['vendor_name'] = data['vendor_name'].str.title()
data['item_description'] = data['item_description'].str.title()

# Filtering the data in the timeframe 2016 - 2019
data['year'] = pd.to_datetime(data['date']).dt.year
data_2016_2019 = data[(data['year'] >= 2016) & (data['year'] <= 2019)]
sorted_data_2016_2019 = data_2016_2019.sort_values(by='date')  # an optional sort of the dates in 2016-2019 timeframe

# Discerning the most popular item per zip code
most_popular_items_per_zipcode = data_2016_2019.groupby(['zip_code', 'item_description'])\
                                    ['bottles_sold'].sum().reset_index()
most_popular_items_per_zipcode = int(most_popular_items_per_zipcode.loc[most_popular_items_per_zipcode
                                 .groupby('zip_code')['bottles_sold'].idxmax()])

print("\n------MOST POPULAR ITEM PER ZIP CODE IN THE TIMEFRAME 2016-2019------\n")
print(most_popular_items_per_zipcode)

# Visualization of the most popular item per zip code , based on bottles sold
sns.set_style("darkgrid")
plt.figure(figsize=(12, 8))
sns.barplot(data=most_popular_items_per_zipcode, x='zip_code', y='bottles_sold', hue='item_description')
plt.title('Most Popular Item per Zip Code (2016-2019)')
plt.xlabel('Zip Code')
plt.ylabel('Total Bottles Sold')
plt.xticks(rotation=45)
plt.legend(title='Items', bbox_to_anchor=(1.1, 1.1), loc='upper left')
plt.tight_layout()
plt.show()


# Computing the sales percentage per store
total_sales_per_store = sorted_data_2016_2019.groupby('store_name')['sale_dollars'].sum()
total_sales = total_sales_per_store.sum()
sales_percentage_per_store = round((total_sales_per_store / total_sales) * 100, 2)

print("\n------SALES PERCENTAGE PER STORE IN THE TIMEFRAME 2016-2019------\n")
print(sales_percentage_per_store)

# Visualization of the sales percentage per store in the 2016-2019 timeframe using a bar plot
# For visualization purposes we will use in the plotting phase only the stores that have at least 0.5% sales percentage
filtered_sales_percentage_per_store = sales_percentage_per_store[sales_percentage_per_store >= 0.5]
filtered_sales_percentage_per_store_sorted = filtered_sales_percentage_per_store.sort_values(ascending=False)

plt.figure(figsize=(10, 8))
plt.barh(filtered_sales_percentage_per_store_sorted.index[::-1],
         filtered_sales_percentage_per_store_sorted.values[::-1],
         color='blue')

plt.xlabel('Sales Percentage (%)')
plt.ylabel('Store Name')
plt.title('Sales Percentage per Store (with at least 0.5%)')
plt.tight_layout()
plt.show()