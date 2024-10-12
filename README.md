# Apache Airflow Student Onboard Workflow Implementation

## Introduction
This repository contains Apache Airflow Directed Acyclic Graphs (DAGs) designed to automate the onboarding process for students enrolling in courses. The solution involves two primary DAGs: the **Main_DAG** and the **BP_DAG** (Business Process DAG), working in tandem to streamline student data processing and course enrollment.

The Main_DAG reads an input Excel file, which contains key student information such as SSN, First Name, Last Name, Date of Birth, Email, Confirmed Course ID, Payment ID, Payment Amount, and Payment Date. This Excel file may have up to 10,000 rows, each representing a student. For every student record, the Main_DAG invokes the BP_DAG to carry out specific tasks required for onboarding.

The BP_DAG is responsible for executing the following sequential tasks:

Task_01: Check if the SSN is already registered for the course.
Task_02: Retrieve subjects associated with the course.
Task_03: Calculate the total cost of the subjects.
Task_04: Create a new student record in the system.
Task_05: Register the student for the course.
Task_06: Register the student for individual course subjects.
Task_07: Send a welcome email to the student.
Task_08: Send a message to Azure Event Hub confirming onboarding.
Task_09: Log detailed information to Grafana for monitoring.
Task_10: Closing dummy task for process finalization.

This project automates repetitive onboarding tasks, ensuring smooth and efficient student enrollment, reducing human error, and integrating monitoring tools like Azure Event Hub and Grafana for end-to-end visibility.
