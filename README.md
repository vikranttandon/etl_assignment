# Etl_assignment

## Objective

In this assignment, you will build a streamlined **Extract, Transform, and Load (ETL)** pipeline that demonstrates **Test-Driven Development (TDD)** by performing the following tasks:

1. Extract data from a CSV file (`employee_details.csv`).
2. Transform the data according to specified business rules.
3. Load the transformed data into a PostgreSQL database.
4. Deploy the ETL pipeline using Docker Compose to containerize both the ETL application and the database.

## Requirements

- **Python 3.8+**
- **Docker Compose**
- **PostgreSQL**
- Any additional open-source libraries or tools that support ETL best practices.

## Instructions

### Step 1: Extract Data from CSV

Create a `read_csv()` function to read data from a CSV file. This function should accept a file path argument and return an in-memory data structure, such as a list of dictionaries or a Pandas DataFrame, containing the employee details.

### Step 2: Data Transformation

Implement a `transform_data()` function to apply the following transformations:

1. **Date Format Conversion:** Convert `BirthDate` from `YYYY-MM-DD` to `DD/MM/YYYY`.
2. **Data Cleaning:** Standardize the `FirstName` and `LastName` columns by removing any leading or trailing whitespace.
3. **Full Name Creation:** Combine `FirstName` and `LastName` into a new `FullName` field.
4. **Age Calculation:** Calculate each employee’s age from their `BirthDate` as of **January 1, 2023** and add an `Age` column.
5. **Salary Categorization:** Add a `SalaryBucket` column to classify employees based on their salary range:
   - `A`: Salary less than `50,000`
   - `B`: Salary between `50,000` and `100,000`
   - `C`: Salary above `100,000`
6. **Column Removal:** Drop the original `FirstName`, `LastName`, and `BirthDate` columns after processing.

### Step 3: Load Data into PostgreSQL

Develop a `load_data()` function to connect to a PostgreSQL database and load the transformed data into a target table. Ensure that necessary indexes are created on the table to enhance data retrieval performance.

### Step 4: Docker Compose Setup

- **Dockerfile:** Write a Dockerfile to build an image for the ETL application environment, including all necessary dependencies.
- **docker-compose.yml:** Configure Docker Compose with two services:
  - **ETL Service** for the Python application.
  - **PostgreSQL Service** for the database.
  Ensure that both services can communicate within the Docker network and share environment variables for configuration.

## Deliverables

The project should include the following components:

- **main.py**: The main ETL script, containing `read_csv()`, `transform_data()`, and `load_data()` functions.
- **Tests**: Use TDD principles to create test suites covering each of the ETL functions and transformations, ensuring robust functionality and error handling.
- **Dockerfile**: A Dockerfile to build the ETL application’s Docker image.
- **docker-compose.yml**: A configuration file for setting up and connecting the ETL and PostgreSQL services.
- **README.md**: Instructions for setting up, running, and testing the ETL pipeline with Docker Compose.

The final solution should enable the pipeline to read, transform, and load data from `employee_details.csv` into a PostgreSQL database using Docker Compose, with a focus on maintaining code quality and testing.

## Submission

Submit the project as a GitHub repository, containing all required files. You may create a private repository if preferred and share access as needed.

## Additional Notes

- Demonstrate TDD practices by thoroughly testing each function, transformation rule, and database interaction.
- Optional: If you have experience with an ETL orchestration tool like **Apache Airflow** or **Luigi**, feel free to integrate it into the pipeline and provide setup instructions in the README file.
