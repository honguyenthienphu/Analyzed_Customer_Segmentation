# [Python] Analyze Customer Segmentation of Sprocket Central - RFM Analyze
<h2>I. Introduction</h1>
<p>SuperStore is a global retail company, so it has a large customer base. On the occasion of Christmas and New Year, the Marketing department plans to run marketing campaigns to show appreciation to customers who have supported the company over time</p>
<p>The Marketing department has not yet segmented this year’s customers because the dataset is too large to process manually as in previous years. Therefore, they have asked the Data Analytics team to assist in implementing a segmentation model for classifying each customer</p>
<p>The Marketing Director has also proposed using the RFM model and developing a segmentation evaluation workflow through Python programming</p>
<h2>II. Requirements</h2>
<ul>
  <li>Computational Thinking</li>
  <li>pandas</li>
  <li>matplotlib</li>
  <li>seaborn</li>
</ul>
<h2>III. Data Access</h2>
<h3>Computational Thinking:</h3>
<h4>1. Decomposition</h4>
<p>Break down the larger problem into smaller, manageable issues for easier handling and resolution</p>
<p><b>1.1 Data Examination and Processing: </b>Handle canceled transactions, missing data, and clean the dataset</p>
<ul>
  <li>Missing Data, Duplicates, Incorrect Data Types, and Incorrect Values</li>
  <div class="code-box">
    <pre><code>
    # Check for missing and duplicate data
    missing_data = df_cleaned.isnull().sum()
    duplicate_data = df_cleaned.duplicated().sum()
    print(f"Missing data:\n{missing_data}\n")
    print(f"Duplicate rows: {duplicate_data}\n")
    </code></pre>  
  </div>
  <img src="https://github.com/user-attachments/assets/634b389c-6b25-4a6e-b086-47e850e92694">
  <li>InvoiceNo: Remove canceled transactions (InvoiceNo starting with 'C')</li>
  <li>Quantity: Handle negative values (Quantity should be > 0)</li>
  <li>UnitPrice: Handle values equal to 0 (UnitPrice should be > 0)</li>
  <li>CustomerID: Convert data type to String</li>
  <div class="code-box">
    <pre><code>
    # Convert 'UnitPrice' to float and 'CustomerID' to object type
    df_cleaned['UnitPrice'] = df_cleaned['UnitPrice'].str.replace(',', '.').astype(float)
    df_cleaned['CustomerID'] = df_cleaned['CustomerID'].astype(object)
    </code></pre>  
   </div>
</ul>
<p><b>1.2 Calculate R, F, M Scores:</b></p>
<ul>
  <li>Recency (R): The number of days since the customer’s last purchase until 31/12/2011. Calculate by taking the difference between 31/12/2011 and the customer’s last purchase date</li>
  <li>Frequency (F): The number of transactions the customer made during the year 2011</li>
  <li>Monetary (M): The total amount spent by the customer, calculated as: Quantity * UnitPrice</li>
</ul>
<p><b>1.3 Score R, F, M, and Customer Segmentation: </b>Segment customers into 5 groups using quintiles</p>
<ul>
  <li>Score 1 is the lowest (customers with few purchases and low spending), and score 5 is the highest</li>
  <li>Calculate quintiles for each metric using pd.qcut to assign scores for R, F, and M</li>
</ul>
<p><b>1.4 Visualize and Analyze</b></p>
<ul>
  <li>Use a Histogram to show the distribution of R, F, M scores: sns.distplot</li>
  <li>Use visualizations like tree maps to display the number of customers in each segment (11 segments): squarify.plot</li>
</ul>

<h4>2. Pattern Recognition</h4>
<p>Segment customers based on their RFM Recency score</p>
<div class="code-box">
    <pre><code>
    # Compute Quintiles for R, F, and M
    rfm['R_Quintile'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm['F_Quintile'] = pd.qcut(rfm['Frequency'], 5, labels=[1, 2, 3, 4, 5])
    rfm['M_Quintile'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
    </code></pre>  
</div>

<h4>3. Abstraction</h4>
<p>Group customers into 5 levels based on the number of days since their last transaction:</p>
<ul>
  <li>Recency Score (R_Score): Group customers into 5 levels based on the number of days since their last transaction.</li>
  <li>Frequency Score (F_Score): Group customers based on the number of transactions they have made.</li>
  <li>Monetary Score (M_Score): Group customers based on their total spending.</li>
</ul>
<div class="code-box">
    <pre><code>
    # Calculate Recency, Frequency, and Monetary values for RFM analysis
    rfm = df_cleaned.groupby('CustomerID').agg(
      Recency=('InvoiceDate', lambda x: (reference_date - x.max()).days),
      Frequency=('InvoiceNo', 'count'),
      Monetary=('Quantity', lambda x: (x * df_cleaned.loc[x.index, 'UnitPrice']).sum())
    ).reset_index()
    </code></pre>  
</div>

<h4>4. Algorithm Design</h4>
<p>The final step is to design an algorithm to solve the problem:</p>
<ul>
  <li>1. Data Cleaning: Remove canceled transactions and handle rows with missing customer information.</li>
  <li>2. RFM Calculation: </li>
  <ul>
    <li>Calculate the most recent purchase date to determine the Recency value.</li>
    <li>Count the number of purchases to calculate the Frequency value.</li>
    <li>Sum up the total spending to derive the Monetary value.</li>
  </ul>
  <li>Ranking and Scoring: Divide the R, F, and M metrics into five groups using the quintile method.</li>
  <li>Customer Segmentation: Group customers based on their total RFM score into categories such as Champions, Loyal Customers, Potential Loyalists, New Customers, and more.</li>
  <li>Visualization: Present the results using charts for easy analysis and presentation.</li>
</ul>

<h3>Result:</h3>
<h4>1. Plot treemap for Customer Segments</h4>
<b>Code:</b>
<div class="code-box">
    <pre><code>
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
    </code></pre>  
</div>
<b>Result:</b>
<img src="https://github.com/user-attachments/assets/ef9b5544-a778-4873-8112-92520d2b835b" style="width: 100%;">
<b>Insight:</b>
<p>The tree map chart provides a clear visualization of the distribution of customer segments:</p>
<ul>
  <li>Both "Champions" and "Hibernating" Customers share the approximately equal quantity: 828 and 811</li>
  <li>Besides, the New customer and Potential Loyalists also have a large quantiy for Marketing team to focus</li>
  <li>The Markeing team can base in this chart to finalize the strategy for the Customer</li>
</ul>

<h4>2. Histogram distributions of Recency, Frequency, and Monetary</h4>
<b>Code:</b>
<div class="code-box">
    <pre><code>
    plt.figure(figsize=(18, 5))
    for i, col in enumerate(['Recency', 'Frequency', 'Monetary'], 1):
        plt.subplot(1, 3, i)
        sns.distplot(rfm[col], bins=20, kde=True)
        plt.title(f'{col} Distribution')
        plt.xlabel(col)
        plt.ylabel('Frequency')
    plt.tight_layout()
    </code></pre>  
</div>
<b>Result:</b>
<img src="https://github.com/user-attachments/assets/01805992-3aae-48b0-a915-99f8dd1dcc3d" style="width: 100%;">
<b>Insight:</b>
<p>The histogram chart illustrates the distribution of data for Recency, Frequency, and Monetary values, showcasing how these metrics are spread across the customer base.:</p>
<ul>
  <li>A left-skewed distribution.</li>
  <li>Most of the data is concentrated in a specific range, with limited variability.</li>
  <li>The distribution does not follow a normal distribution pattern.</li>
</ul>
