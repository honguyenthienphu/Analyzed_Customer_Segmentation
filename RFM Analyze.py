import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify

# Read file CSV into DataFrame
df = pd.read_csv('ecommerce retail dt.csv')

# Remove rows with missing values in 'Description' and 'CustomerID'
df_cleaned = df.dropna(subset=['Description', 'CustomerID'])

# Check for missing and duplicate data
missing_data = df_cleaned.isnull().sum()
duplicate_data = df_cleaned.duplicated().sum()
print(f"Missing data:\n{missing_data}\n")
print(f"Duplicate rows: {duplicate_data}\n")

# Convert 'UnitPrice' to float and 'CustomerID' to object type
df_cleaned['UnitPrice'] = df_cleaned['UnitPrice'].str.replace(',', '.').astype(float)
df_cleaned['CustomerID'] = df_cleaned['CustomerID'].astype(object)

# Convert 'InvoiceDate' into datetime
df_cleaned['InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'])

# Set reference date for Recency calculation
reference_date = pd.to_datetime('2011-12-31')

# Calculate Recency, Frequency, and Monetary values for RFM analysis
rfm = df_cleaned.groupby('CustomerID').agg(
    Recency=('InvoiceDate', lambda x: (reference_date - x.max()).days),
    Frequency=('InvoiceNo', 'count'),
    Monetary=('Quantity', lambda x: (x * df_cleaned.loc[x.index, 'UnitPrice']).sum())
).reset_index()

# Compute Quintiles for R, F, and M
rfm['R_Quintile'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Quintile'] = pd.qcut(rfm['Frequency'], 5, labels=[1, 2, 3, 4, 5])
rfm['M_Quintile'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

# Combine into RFM Score
rfm['RFM_Score'] = rfm['R_Quintile'].astype(str) + rfm['F_Quintile'].astype(str) + rfm['M_Quintile'].astype(str)

# Customer segmentation based on RFM_Score
def customer_segment(rfm_score):
    segment_map = {
        "Champions": ["555", "554", "544", "545", "454", "455", "445"],
        "Loyal": ["543", "444", "435", "355", "354", "345", "344", "335"],
        "Potential Loyalists": ["553", "551", "552", "541", "542", "533", "532", "531", "452", "451", "442", "441", "431", "453", "433", "432", "423", "353", "352", "351", "342", "341", "333", "323"],
        "New Customers": ["512", "511", "422", "421", "412", "411", "311"],
        "Promising": ["525", "524", "523", "522", "521", "515", "514", "513", "425", "424", "413", "414", "415", "315", "314", "313"],
        "Need Attention": ["535", "534", "443", "434", "343", "334", "325", "324"],
        "About To Sleep": ["331", "321", "312", "221", "213", "231", "241", "251"],
        "At Risk": ["255", "254", "245", "244", "253", "252", "243", "242", "235", "234", "225", "224", "153", "152", "145", "143", "142", "135", "134", "133", "125", "124"],
        "Cannot Lose Them": ["155", "154", "144", "214", "215", "115", "114", "113"],
        "Hibernating customers": ["332", "322", "233", "232", "223", "222", "132", "123", "122", "212", "211"],
        "Lost Customers": ["111", "112", "121", "131", "141", "151"]
    }
    for segment, scores in segment_map.items():
        if rfm_score in scores:
            return segment
    return 'Unknown Segment'

rfm['Customer_Segment'] = rfm['RFM_Score'].apply(customer_segment)

# Histogram distributions of Recency, Frequency, and Monetary
plt.figure(figsize=(18, 5))
for i, col in enumerate(['Recency', 'Frequency', 'Monetary'], 1):
    plt.subplot(1, 3, i)
    sns.distplot(rfm[col], bins=20, kde=True)
    plt.title(f'{col} Distribution')
    plt.xlabel(col)
    plt.ylabel('Frequency')

plt.tight_layout()

# Plot treemap for Customer Segments
segment_counts = rfm['Customer_Segment'].value_counts().reset_index()
segment_counts.columns = ['Customer_Segment', 'Count']
labels = [f'{segment}\n{count}' for segment, count in zip(segment_counts['Customer_Segment'], segment_counts['Count'])]
colors = ['#FF0000', '#00FFFF', '#FFFF00', '#A52A2A', '#800080', 
          '#00FF00', '#808000', '#FFC0CB', '#FFA500', '#FF00FF', '#736F6E']
plt.figure(figsize=(12, 8))
squarify.plot(sizes=segment_counts['Count'], label=labels, alpha=0.7, color=colors)
plt.title('RFM Segments of Customer Count', fontsize=18)
plt.axis('off')
plt.show()