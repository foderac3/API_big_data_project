# Big Data API Project

## Description

This project is a REST API designed for managing data related to establishments using their SIRET number. It includes full CRUD (Create, Read, Update, Delete) operations with added traceability through an audit log and logging system.

## Features

- **CRUD operations**: 
  - Create: Add new records to the database.
  - Read: Retrieve specific records using the SIRET number or all records.
  - Update: Modify details of an existing record.
  - Delete: Remove records from the database.
- **Audit logging**: Tracks all actions (GET, POST, PUT, DELETE) in a dedicated MongoDB collection for traceability.
- **Request logging**: Maintains a detailed log file of all API interactions.
- **Robust error handling**: Validates SIRET inputs and returns appropriate error messages.

## Technologies Used

- **Flask** and **Flask-RESTful**: For building and structuring API routes.
- **MongoDB**: As the database for storing records.
- **PyMongo**: For connecting Flask with MongoDB.
- **Logging**: To create logs for requests and actions.
- **Postman**: For testing and validating API endpoints.

## Requirements

- Python 3.8+
- MongoDB
- Required Python packages (specified in `requirements.txt`)

## Installation

1. **Clone the repository**
2. **Install Dependencies**: pip install -r requirements.txt
3. **Set up MongoDB**: Ensure MongoDB is running locally on localhost:27017 and create a database named API_bigdata with collections bigdata and audit_logs and loading data file
4. **Run the application**: python app.py
5. **Access the API**: http://localhost:5000

## Endpoints

GET	/siret/<siret_id>	Retrieve a record by SIRET number.
GET	/siret	Retrieve all records.
POST	/siret	Add a new record.
PUT	/siret/<siret_id>	Update an existing record.
DELETE	/siret/<siret_id>	Delete a record by SIRET number.

## Testing

- Postman was used to test all endpoints.
Example scenarios:
      - Retrieving valid and invalid SIRET records.
      - Adding new records with and without required fields.
      - Updating and deleting specific SIRET records.

## Logs and Traceability

Log file: Stores all API requests and results in api.log.
Audit log: Maintains a history of CRUD operations in the audit_logs collection in MongoDB.

NGATCHOU Serena
DIEDHIOU Fodé
TABTI Anya
DECHAMBOST Gabriel
