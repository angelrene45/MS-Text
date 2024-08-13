Overview of the Solution
Business Function
Transformit is an in-house data ingestion framework built in Python, designed to ingest data into Snowflake on the cloud and transform it as per business requirements. It supports data extraction from various sources, processing and loading into Snowflake, executing SQL transformations, and downstream data consumption.

1. Executive Summary
Overview
Transformit provides a robust and flexible framework for data ingestion and transformation, leveraging Snowflake's cloud-based data warehousing capabilities.

High-Level Business Goals

Streamline data ingestion processes.
Ensure data consistency and accuracy.
Facilitate data transformation and integration.
High-Level Cloud Business Goals

Utilize cloud resources to scale data ingestion and processing.
Leverage Snowflake's cloud data warehouse for efficient data storage and query performance.
Enable seamless data integration with other cloud services.
High-Level Technology Goals

Implement a modular and extensible architecture.
Ensure high performance and reliability.
Provide detailed logging and monitoring capabilities.
2. Requirements
Business Function or Ecosystem

Ingest data from diverse sources including Web APIs, MQ, Sybase, DB2, Salesforce, OFL.
Transform and load data into Snowflake for business consumption.
Business Functional Requirements

Extract data from various sources.
Process files and upload to Snowflake internal stages.
Load data into Snowflake tables.
Execute SQL transformations.
Generate files for downstream consumption.
Architecturally Significant Constraints

Must integrate with existing Snowflake infrastructure.
Ensure data security and compliance with regulations.
Maintain high availability and fault tolerance.
Salient Cross-Functional Requirements (Architecture Characteristics)

Scalability
Performance
Reliability
Security
3. Current State Architecture
Current State Logical View

Data is currently ingested and processed using legacy systems with limited automation and scalability.
4. Target State Architecture
Logical View

Modular architecture with separate modules for data pulling, polling, staging, transformation, and downstream processing.
Data View

Data sources: Web APIs, MQ, Sybase, DB2, Salesforce, OFL.
Data targets: Snowflake tables and other databases.
Deployment View

Deploy Transformit in containerized environments for scalability.
Utilize cloud-native services for monitoring and logging.
Security View

Implement authentication and authorization for data access.
Ensure data encryption at rest and in transit.
Regular audits and compliance checks.
5. Interim States
Gradual migration from legacy systems to Transformit framework.
Phased implementation of Transformit modules.
6. Related ADRs
N/A
7. Related Cloud Pipelines
Data ingestion pipeline from source systems to Snowflake.
Transformation and loading pipeline within Snowflake.
Downstream data consumption pipeline to other databases or file systems.
