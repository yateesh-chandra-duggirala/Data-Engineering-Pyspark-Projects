# Databricks notebook source
# MAGIC %md
# MAGIC # Customer Insights

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Data Collection

# COMMAND ----------

# Create a Database named market and use it as default database
spark.sql("DROP DATABASE IF EXISTS market CASCADE;")
spark.sql("CREATE DATABASE market;")
spark.sql("USE DATABASE market;")

# COMMAND ----------

# This function is used to save the loaded data frames into tables
def read_df(file_info) : 

    # The table name is set same as the file name
    table_name = file_info.name.split(".csv")[0]

    # Read each the file into Dataframe
    df = spark.read.format("csv")\
        .option("header", "true")\
        .option("inferSchema", "true")\
            .load(file_info.path)
        
    # Save the table that is loaded into dataframes with mode overwrite
    df.write.format("delta").mode("overwrite").saveAsTable(f"{table_name}")
    return f"{table_name} is created"

# COMMAND ----------

# Provide the path of the folder that contains files as the parameter to the below function
def create_tables(folder_path):

    # Read the list of files present in the below specified folder
    list_files = dbutils.fs.ls(folder_path)
    
    # Loop through the list of files
    for f in list_files : 

        # calling the function to create tables
        read_df(f)
    return "All Tables created successfully"

# COMMAND ----------

# customer_insights_data folder is passed as the parameter to the create_tables() function and calling the function
create_tables("dbfs:/FileStore/customer_insights_data")

# COMMAND ----------

spark.sql("show tables").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Load Tables into Data Frames

# COMMAND ----------

df_customer = spark.sql("SELECT * from customer_information")
df_product = spark.sql("SELECT * from product")
df_transactions = spark.sql("SELECT * from transactions")
df_feedback = spark.sql("SELECT * from customer_feedback")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Joining Tables

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3.1. Join Product and Transactions 
# MAGIC Add a new column that provides the "transaction_amt"  

# COMMAND ----------

from pyspark.sql.functions import expr, lit

# COMMAND ----------

# Join the Tables Transactions and Products on product_id and make the product of quantity and price as transaction_amt
df_trans_sku = df_transactions.join(df_product, "product_id")\
    .select(
        col("transaction_id"), 
        col("transaction_date"), 
        col("customer_id"), 
        col("product_name"),
        col("quantity"),
        (col("quantity") * col("price")).alias("transaction_amt")
        )

# COMMAND ----------

# Display the transaction_sku dataframe
df_trans_sku.display()

# COMMAND ----------

# Create a table named "transaction_sku"
df_trans_sku.write.format("delta").mode("overwrite").saveAsTable("transaction_sku")

# COMMAND ----------

# MAGIC %sql
# MAGIC select t.transaction_id, t.transaction_date, t.customer_id, p.product_name, t.quantity, (t.quantity * p.price) as transaction_amt from transactions t join product p on t.product_id = p.product_id

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3.2. Join Customers, Product and Transactions 
# MAGIC customer details who had made more transactions
