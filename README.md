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
