

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
 
