# Customer Segmentation using RFM Analysis
**Project:** ELEVO PATHWAYS INTERNSHIP  
**Author:** Yasser Shawky  

---

## Overview
This project focuses on **RFM (Recency, Frequency, Monetary) analysis** to segment customers based on their purchasing behavior.  
The main goal is to understand customer behavior, identify high-value segments, and propose data-driven marketing strategies.

---

## Dataset
- **Source:** Online Retail Dataset  
- **Columns include:**  
  - `InvoiceNo`: Invoice number  
  - `StockCode`: Product code  
  - `Description`: Product description  
  - `Quantity`: Number of products purchased  
  - `InvoiceDate`: Date of purchase  
  - `UnitPrice`: Price per unit  
  - `CustomerID`: Unique customer ID  
  - `Country`: Customer's country  

---

## Data Preprocessing
- Removed duplicates and rows with missing `CustomerID`  
- Filled missing descriptions with `'Unknown'` and standardized text  
- Cleaned `InvoiceNo` and `StockCode` for consistency  
- Calculated `TotalAmount = Quantity * UnitPrice`  
- Converted date columns to proper datetime formats  

---

## RFM Analysis
- **Recency (R):** Days since last purchase  
- **Frequency (F):** Number of purchases  
- **Monetary (M):** Total amount spent  

- Customers segmented into:  
  - **Champions**  
  - **Loyal Customers**  
  - **Potential Loyalists**  
  - **Big Spenders**  
  - **At-Risk Customers**  
  - **Lost Customers**  

- Segmentation implemented using `pandas.qcut` for scoring and a **custom function** for labeling.

---

## Visualizations
- **Customer Segments Distribution:** Count plot of each segment  
- **Top 5 Countries of Champions:** Bar chart with log scale and value labels  

---

## Marketing Recommendations (Formal)
| Segment             | Recommendation |
|--------------------|----------------|
| **Champions**       | Exclusive offers, loyalty programs, personalized messages |
| **Loyal Customers** | Bundle offers, point-based rewards, free shipping incentives |
| **Potential Loyalists** | Discounts on second purchase, onboarding emails, personalized recommendations |
| **Big Spenders**    | Premium product bundles, exclusive offers to increase purchase frequency |
| **At-Risk**         | “We Miss You” campaigns, limited-time discounts, personalized incentives |
| **Lost**            | Reactivation campaigns, targeted comeback offers, monitor cost efficiency |

---

## Tools & Libraries
- **Python**  
- **Pandas & NumPy**: Data cleaning and analysis  
- **Matplotlib & Seaborn**: Visualization  
- **re**: Regular expressions for data cleaning  

---

## Conclusion
RFM-based segmentation provides **insights into customer behavior**, enabling **targeted marketing strategies** that improve customer retention and increase profitability efficiently.

---

## How to Run
1. Install dependencies:  
```bash
pip install pandas numpy matplotlib seaborn openpyxl
