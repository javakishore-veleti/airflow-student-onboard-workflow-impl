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
- **PostgreSQL**: Used as the database to store student and course information.
- **Azure Event Hub**: Used for logging onboarding events.
- **Grafana**: Used for logging and monitoring detailed logs of the onboarding process.

### Extensibility:

- The branch is designed for extensibility. New tasks and workflows can be added with minimal changes, thanks to the modular design.
- Each task in the workflow is implemented as a separate Python class, following the `OnboardWfTask` interface, which ensures that new tasks can be easily integrated.

### How to Run:

1. **Set Up Airflow**:
   - Use the provided Docker Compose setup to run Airflow and its services.
   - Shell scripts (`start_airflow.sh`, `stop_airflow.sh`, `terminate_airflow.sh`) are provided in the `cicd/ephemeral/` directory to manage Airflow.

2. **Invoke the Workflow**:
   - Once Airflow is up, the **Main_DAG** will trigger the **BP_DAG** for each row of the student data.

3. **Monitor the Workflow**:
   - Use the Airflow web interface to monitor DAG runs and task statuses.
   - Detailed logs are sent to Azure Event Hub and Grafana for real-time monitoring.




