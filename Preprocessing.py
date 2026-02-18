from weakref import ref
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import re

pd.set_option('display.max_columns', None) 
pd.set_option('display.max_rows', None) 
### Reading the dataset
df = pd.read_excel("data/Online Retail.xlsx")
df_copy = df.copy() 
df.drop_duplicates(inplace=True)
df.dropna(subset=['CustomerID'], inplace=True)
## Checking the dataset
# print(df.head())
# print(df.info())

# ### Checking for missing values
# print(df.isnull().sum())

##data cleaning and preprocessing
df['Description'] = df['Description'].fillna('Unknown').str.title()
df['StockCode'] = df['StockCode'].str.upper().replace(r'[^A-Z0-9_]', '', regex=True)
df['InvoiceNo'] = df['InvoiceNo'].replace(r'[^0-9]', '', regex=True).astype(int)

df['CustomerID'] = df['CustomerID'].astype(int)


for col in df.columns :
    if df[col].dtype == 'object' or df[col].dtype == 'str' :
        df[col] = df[col].str.strip()
        df[col] = df[col].astype('string')
        df[col] = df[col].fillna('Unknown')


df['InvoiceDate'] = df['InvoiceDate'].dt.date
df['Country'] = df['Country'].replace(['Unspecified', 'EIRE'], ['Unknown' , 'Ireland'])
df['Quantity'] = df['Quantity'].fillna(0).astype(int)
df['TotalAmount'] = df['UnitPrice'] * df['Quantity']

Ref_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
RFM_df = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x : (Ref_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'TotalAmount': 'sum' ,
    'Country': 'first'
})
RFM_df.columns = ['Recency', 'Frequency' , 'Monetary', 'Country']
RFM_df = RFM_df.sort_values(['Recency', 'Frequency', 'Monetary'], ascending=[True, False, False])

### Segmentation 
RFM_df['R'] = pd.qcut(RFM_df['Recency'].rank(method='first'),5, labels=[5,4,3,2,1])
RFM_df['F'] = pd.qcut(RFM_df['Frequency'].rank(method='first'),5, labels=[1,2,3,4,5])
RFM_df['M'] = pd.qcut(RFM_df['Monetary'].rank(method='first'),5, labels=[1,2,3,4,5])

seg_map = {
    r'5[4-5][4-5]': 'Champions',
    r'[3-4][4-5][3-5]': 'Loyal Customers',
    r'4[2-3][2-4]': 'Potential Loyalists',
    r'[2-5][2-5]5': 'Big Spenders',
    r'[1-2][4-5][2-5]': 'At Risk',
    r'1[1-2][1-2]': 'Lost'
}

RFM_df['score'] = RFM_df['R'].astype(str) + RFM_df['F'].astype(str) + RFM_df['M'].astype(str)


def segmentation(row):
    
    R = row['R']
    F = row['F']
    M = row['M']
    
    # Champions
    if R >= 4 and F >= 4 and M >= 4:
        return 'Champions'
    
    # Loyal Customers
    elif R >= 3 and F >= 3:
        return 'Loyal Customers'
    
    # Big Spenders
    elif M >= 4:
        return 'Big Spenders'
    
    # Potential Loyalists
    elif R >= 4 and F >= 2:
        return 'Potential Loyalists'
    
    # At Risk
    elif R <= 2 and F >= 3:
        return 'At Risk'
    
    # Lost
    elif R <= 2 and F <= 2:
        return 'Lost'
    
    else:
        return 'Others'


RFM_df['Segment'] = RFM_df.apply(segmentation, axis=1)

### Visualize the distribution of customer segments
plt.figure(figsize=(10,6))
ax = sns.countplot(data=RFM_df, x='Segment', order=RFM_df['Segment'].value_counts().index, palette='viridis')
plt.title("Customer Segments Distribution")

for i in ax.containers:
    ax.bar_label(i, fmt='%.0f', padding=3)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

### Analyze the characteristics of each segment
segment_analysis = RFM_df.groupby('Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean'
})

print(segment_analysis)

### Visualize Top 5 countries with the highest number of champion customers
country_champions = (
    RFM_df[RFM_df['Segment'] == 'Champions']
    .groupby('Country')
    .size()
    .sort_values(ascending=False)
    .head(5)
    .reset_index(name='Count')
)


plt.figure(figsize=(10,6))


ax = sns.barplot(data=country_champions, x='Country', y='Count', palette='magma')

plt.yscale('log')  
plt.title("Top 5 Countries with Highest Champion Customers (Log Scale)")
plt.ylabel("Number of Champions (Log Scale)")
plt.xticks(rotation=45)


for i in ax.containers:
    ax.bar_label(i, fmt='%.0f', padding=3)

plt.tight_layout()
plt.show()
