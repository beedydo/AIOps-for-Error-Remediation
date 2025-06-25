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

### Pipeline Demo

![pipeline video](/assets/pipeline_demo.mkv)
