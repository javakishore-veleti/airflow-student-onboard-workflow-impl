# Student Onboard Workflow - Apache Airflow Implementation

## Branch: `student-onboard-with-af-dags`

This branch implements the **student onboarding workflow** using **Apache Airflow DAGs**. The workflow automates the process of onboarding students to various courses, leveraging Apache Airflow's task orchestration capabilities. Each student’s data is processed from an input Excel sheet, and a series of tasks (DAGs) are executed to complete the onboarding process.

### Key Features of the Workflow:

- **Input Data**: Student information is provided via an Excel sheet that includes fields such as:
  - SSN (Social Security Number)
  - First Name, Last Name
  - Date of Birth (DOB)
  - Email
  - Confirmed Course ID
  - Payment Information (Payment ID, Amount, Date)

- **Main DAG**: 
  - The **Main_DAG** reads the input Excel sheet and triggers the **BP_DAG** for each student row. 
  - The student data is passed as configuration to the **BP_DAG** for processing.

- **BP_DAG**:
  - The **BP_DAG** consists of the following steps:
    1. **Check SSN Not Registered**: Verifies if the student is already registered in the system.
    2. **Get Course Subjects**: Retrieves the subjects for the confirmed course.
    3. **Calculate Total Cost**: Computes the total cost for the course and its subjects.
    4. **Register Student**: Registers the student and their course details in the system.
    5. **Send Welcome Email**: Sends a confirmation email to the student.
    6. **Log to Azure Event Hub**: Logs onboarding information to Azure Event Hub.
    7. **Log to Grafana**: Records detailed logs in Grafana for monitoring and troubleshooting.
  
### Technologies Used:

- **Apache Airflow**: Used for task orchestration and managing workflows.


### How to Run:

1. **Set Up Airflow**:
   - Use the provided Docker Compose setup to run Airflow and its services.
   - Shell scripts (`start_airflow.sh`, `stop_airflow.sh`, `terminate_airflow.sh`) are provided in the `cicd/ephemeral/` directory to manage Airflow.

2. **Invoke the Workflow**:
   - Once Airflow is up, the **Main_DAG** will trigger the **BP_DAG** for each row of the student data.

3. **Monitor the Workflow**:
   - Use the Airflow web interface to monitor DAG runs and task statuses.
   - Detailed logs are sent to Azure Event Hub and Grafana for real-time monitoring.

## Steps to Execute DAGs via Airflow REST API

### API Documentation for Triggering Airflow DAGs

The Airflow REST API allows you to trigger DAGs programmatically using HTTP requests. You can use tools like cURL or Postman to send requests to the Airflow API endpoints.

Ensure in your Airflow configuration file (airflow.cfg) that the following settings are enabled:
```python
#    auth_backends = airflow.api.auth.backend.session
#    authenticate = True
#    enable_experimental_api = True
```

1. Triggering Main_DAG_Distributed_Execution
Endpoint: POST /api/v1/dags/Main_DAG_Distributed_Execution/dagRuns

Request Headers:
Content-Type: application/json 
Authorization: Basic Base64(username:password) (if authentication is enabled)

Request Body:
```json
{
    "conf": {
        "execution_date": "2021-08-01T00:00:00+00:00",
        "key": "value"
    }
}
```

Example cURL Command:
```shell
curl -X POST "http://localhost:8080/api/v1/dags/Main_DAG_Distributed_Execution/dagRuns" \
    -H "Content-Type: application/json" \
    -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
    -d '{
          "conf": {
            "key": "value"
          }
        }'


```

2. Triggering Main_DAG_Local_Execution

Endpoint: POST /api/v1/dags/Main_DAG_Local_Execution/dagRuns

Request Headers:
Content-Type: application/json 
Authorization: Basic Base64(username:password) (if authentication is enabled)

Request Body:
```json
{
    "conf": {
        "execution_date": "2021-08-01T00:00:00+00:00",
        "key": "value"
    }
}
```

Example cURL Command:
```shell
curl -X POST "http://localhost:8080/api/v1/dags/Main_DAG_Local_Execution/dagRuns" \
    -H "Content-Type: application/json" \
    -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
    -d '{
          "conf": {
            "key": "value"
          }
        }'

```

### Steps to Resolve Unauthorized Error

1. Check Authentication Method:

Determine if your Airflow instance requires authentication. Airflow by default uses basic authentication unless configured otherwise.
Make sure you have the correct username and password for your Airflow instance.

2. Base64 Encoding:

If authentication is enabled, you need to include an Authorization header with your request.

To create the Basic Authentication header, encode your username and password in Base64 format using the following format: username:password.

Example:
Username: admin
Password: admin123

Command to encode: echo -n 'admin:admin123' | base64

Output: YWRtaW46YWRtaW4xMjM=

3. Add Authorization Header in Postman:

    In your Postman request, add the Authorization header:
    Key: Authorization
    Value: Basic YWRtaW46YWRtaW4xMjM= (replace this with your Base64 encoded string) 
4. Ensure API URL is Correct:
 Double-check the URL you are using to ensure it points to the correct endpoint.

5. CORS Issues:
If you are calling the API from a web application, ensure that CORS settings on the server allow requests from your origin.
 



