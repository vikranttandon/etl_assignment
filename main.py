from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

def create_spark_session():

    return SparkSession.builder.appName("Employee ETL").getOrCreate()

def data_extraction(spark, file_path):
    
    df = spark.read.format('csv').option('header', 'true').load(file_path)

    return df


def data_transformation(df):

    # Removing header (as its appearing multiple times) to improve data quality
    header_values = df.columns

    for column in header_values:
        df = df.filter(col(column) != column)

    df = (df.withColumn('FirstName', trim(col('FirstName')))
           .withColumn('LastName', trim(col('  LastName  ')))
           .withColumn('Age', (datediff(to_date(lit("2023-01-01"), 'yyyy-MM-dd'), 
                                         to_date(col('BirthDate'), 'yyyy-MM-dd')) / 365).cast('int'))
           .withColumn('BirthDate', date_format(to_date(col('BirthDate'), 'yyyy-MM-dd'), "dd/MM/yyyy"))
           .drop('  LastName  '))
    
    df = (df.withColumn('FullName', concat_ws(" ", col('FirstName'), col('LastName')))
            .withColumn("SalaryBucket", 
                    when(col('Salary') < 50000, lit('A')).when((col('Salary') >= 50000) & (col('Salary') <= 100000), lit('B')).otherwise(lit('C')))
            .drop('FirstName', 'LastName', 'BirthDate'))
    
    return df

def load_data(df, url, table_name, conf):
    
    (df.write 
        .mode("overwrite") 
        .jdbc(url= url, 
              table=table_name,
              properties=conf))

def test_data(spark, df, jurl, table_name, config):
    
    query = f"(SELECT * FROM {table_name}) as tmp"

    stored = spark.read.jdbc(url=jurl, 
                    table=query, 
                    properties=config)

    # count test, this also tests the database interaction was successful
    test1 = (df.count() == stored.count())
    
    # all salaries must be postive, otherwise the derived SalaryBucket would be deviating
    test2 = (stored.filter(col('Salary')<0).count() == 0)

    # age must withing a suitable range
    test3 = (stored.filter((col('Age') <= 0) | (col('Age') > 80)).count() == 0)
    
    if test1:
        print('count test passed, this also tests the database interaction was successful')
    if test2:
        print('all salaries derived from the CSV are positive')
    if test3:
        print('all age values are well within the range')

    return (test1 and test2 and test3)

def main():

    jurl = "jdbc:postgresql://postgres:5432/etl_db"
    conf = { "user": "etl_user",
              "password": "etl_password",
              "driver": "org.postgresql.Driver"}
    table_name = 'emp_details'

    spark = create_spark_session()
   
    emp_details = data_extraction(spark, "employee_details.csv")
   
    enriched = data_transformation(emp_details)

    enriched.show()

    load_data(enriched, jurl, table_name, conf)

    test_passed = test_data(spark, enriched, jurl, table_name, conf)
    
    if test_passed:
        print("Data test passed!")
    else:
        print("Data test failed.")
    
if __name__ == "__main__":
    main()
