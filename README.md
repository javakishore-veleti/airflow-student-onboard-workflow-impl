# Apache Airflow Student Onboard Workflow Implementation

## Introduction
This repository contains Apache Airflow Directed Acyclic Graphs (DAGs) designed to automate the onboarding process for students enrolling in courses. The solution involves two primary DAGs: the **Main_DAG** and the **BP_DAG** (Business Process DAG), working in tandem to streamline student data processing and course enrollment.

## Purpose
This project automates repetitive onboarding tasks, ensuring smooth and efficient student enrollment, reducing human error, and integrating monitoring tools like Azure Event Hub and Grafana for end-to-end visibility.

## Main_DAG Behavior
The Main_DAG reads an input Excel file, which contains key student information such as SSN, First Name, Last Name, Date of Birth, Email, Confirmed Course ID, Payment ID, Payment Amount, and Payment Date. This Excel file may have up to 10,000 rows, each representing a student. For every student record, the Main_DAG invokes the BP_DAG to carry out specific tasks required for onboarding.

## BP_DAG Behavior
The BP_DAG is responsible for executing the following sequential tasks:

1. Task_01: Check if the SSN is already registered for the course.
2. Task_02: Retrieve subjects associated with the course.
3. Task_03: Calculate the total cost of the subjects.
4. Task_04: Create a new student record in the system.
5. Task_05: Register the student for the course.
6. Task_06: Register the student for individual course subjects.
7. Task_07: Send a welcome email to the student.
8. Task_08: Send a message to Azure Event Hub confirming onboarding.
9. Task_09: Log detailed information to Grafana for monitoring.
10. Task_10: Closing dummy task for process finalization.


