# Software Requirement Specification for "Comprehensive Customer Insights"

## Objective: 
Create a comprehensive customer insights table by joining multiple real-time datasets to analyze customer behavior, transactions, and demographics.

## Dataset Schema:

### 1. Customer Information :
	CustomerID
	FirstName
	LastName
	Email
	Phone
	Address
	City
	State
	ZipCode
	DateOfBirth
	Gender

### 2. Transactions :
	TransactionID
	CustomerID
	TransactionDate
	ProductID
	Quantity
	Price

### 3. Product Information :
	ProductID
	ProductName
	Category
	Brand 
	Price 

### 4. Customer Feedback:
	ReviewID
	CustomerID
	ProductID 
	ReviewDate
	Rating 
	ReviewText


## Requirements for the New Table :

1. Table Name: CustomerInsights
2. Columns:
	```
	CustomerID: Unique identifier for each customer (from Customer Information)
	FirstName: First name of the customer (from Customer Information)
	LastName: Last name of the customer (from Customer Information)
	Email: Email of the customer (from Customer Information)
	Phone: Phone number of the customer (from Customer Information)
	City: City of the customer (from Customer Information)
	State: State of the customer (from Customer Information)
	DateOfBirth: Date of birth of the customer (from Customer Information)
	Gender: Gender of the customer (from Customer Information)
	TotalSpent: Total amount spent by the customer (from Transactions, calculated field)
	TotalTransactions: Total number of transactions made by the customer (from Transactions, calculated field)
	AverageTransactionValue: Average value per transaction (from Transactions, calculated field)
	FavoriteCategory: Most frequently purchased product category (from Transactions and Product Information, calculated field)
	AverageRating: Average rating given by the customer (from Customer Feedback, calculated field)
	LastPurchaseDate: Date of the most recent transaction (from Transactions)
	```

3. Derived Columns:
	```
	TotalSpent: Sum of Quantity * Price from the Transactions dataset for each customer.
	TotalTransactions: Count of TransactionID for each customer from the Transactions dataset.
	AverageTransactionValue: TotalSpent / TotalTransactions.
	FavoriteCategory: Mode of Category from the joined Transactions and Product Information datasets.
	AverageRating: Average of Rating from the Customer Feedback dataset for each customer.
	```

## Steps to Implement the Project:

1. Load the Datasets:
	- Load the Customer Information, Transactions, Product Information, and Customer Feedback datasets into separate tables.

2. Join the Datasets:
	- Join the Transactions table with the Customer Information table on CustomerID.
	- Join the Transactions table with the Product Information table on ProductID.
	- Join the resulting table with the Customer Feedback table on CustomerID and ProductID.

3. Create the Derived Columns:
	- Calculate the TotalSpent, TotalTransactions, AverageTransactionValue, FavoriteCategory, and AverageRating based on the joined data.

4. Create the Final Table:
	- Create the CustomerInsights table with the required columns and insert the calculated data.

5. Verification and Validation:
	- Verify the data for correctness and consistency.
	- Validate the insights by cross-checking with the original data.