# Detect, Evaluate and Automate: AIOps with Ansible and OpenShift AI

## Overview

This project demonstrates a powerful, event-driven architecture that leverages Red Hat OpenShift AI to automate IT incident response. By integrating Event-Driven Ansible (EDA) with an AI/ML pipeline, this solution can automatically detect issues, gather diagnostics, generate incident reports, and create ignition remediation playbooks that engineers can use to serve as a starting point to write their remediation playbook instead of writing it from scratch.



### Use Case

![User Journey Diagram](/assets/user_journey.png)

In modern IT environments, responding to system failures quickly and effectively is crucial. This proof of concept demo showcases how AIOps can be incorporated into the workflow that begins with a Incident Alert (like a web server failure) and lead to a faster closure. This AIOps approach aims to automate the writing of initial incident report and initial remdiation playbook leading to quicker escalation and remediation of an Incident Alert.

### Architecture

![Architecture Diagram](/assets/architecture_diagram.png)

The primary components are:

- **Web Server**: The monitored application host where events originate.
- **Event-Driven Ansible (EDA)**: Listens for events from the Web Server. EDA rulebooks define the conditions under which an action should be taken.
- **Ansible Automation Platform (AAP)**: The central automation engine that executes tasks based on triggers from EDA.
- **Amazon S3 (or similar object storage)**: Used as a central repository for storing raw logs, incident reports, and generated playbooks.
- **Red Hat OpenShift AI**: A platform for managing the lifecycle of predictive and generative AI (gen AI) models, at scale, across hybrid cloud environments. In this architecture, it runs a pipeline to process event data and generate intelligent responses.

The entire process is orchestrated as a seamless, automated workflow, as illustrated by the numbered steps in the diagram:

**1. Event Occurs**

An issue, such as a service failure or an error, occurs on the Web Server.

**2. Event Detection**

Event-Driven Ansible (EDA) is configured with rulebooks to monitor the Web Server. It detects the event in real-time.

**3. Task Execution by AAP**

Upon receiving the event trigger from EDA, the Ansible Automation Platform (AAP) initiates a pre-defined job. This job consists of two main tasks:
- **3.1: Gather Error Logs**: AAP connects to the affected Web Server and collects the relevant raw error logs for analysis.
- **3.2: Upload Logs to S3**: The collected logs are then uploaded to an S3 bucket, making them accessible for the AI pipeline.

**4. Red Hat OpenShift AI Pipeline**
We can trigger the Red Hat OpenShift AI pipeline now that we have the raw error logs of the Web Server, the pipeline performs the following steps:
- **4.1: Retrieve Raw Error Log**: The pipeline retrieves the raw error log from the S3 bucket.
- **4.2: Generate Incident Report**: Using a locally deployed LLM model on OpenShift AI, the pipeline analyzes the log data to understand the root cause and generates a human-readable incident report.
- **4.3: Generate Ansible Playbook**: Based on its analysis, the LLM model generates a new, tailored Ansible Playbook designed to remediate the specific issue that was detected.

### Demo

#### EDA Demo
[TODO]
#### Pipeline Demo
[TODO]
