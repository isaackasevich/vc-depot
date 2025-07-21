# DevOps Setup Guide

This document provides step-by-step instructions to set up a PostgreSQL database, MinIO for photo storage, and Docker Compose for local development. Place this file in your project’s `project-docs/` folder for Cursor to reference.

---

## Prerequisites

* Install Docker and Docker Compose on your development machine.
* Ensure you have basic familiarity with the terminal or command-line interface.

---

## 1. Prepare Docker Compose

1. In your project root, create a file named `docker-compose.yml`.
2. Define the following services within it:

   * **PostgreSQL**: specify the official Postgres image version, set up user credentials, database name, port mapping (e.g., 5432), and a named volume for persistence.
   * **MinIO**: use the MinIO image, configure root user and password, include the server start command with console enabled, map ports for the S3 API (9000) and console (9001), and create a named volume for data storage.
   * **Backend API**: point the build context to your `./backend` directory; set environment variables for `DATABASE_URL`, MinIO endpoint and credentials, and photos bucket name; configure the server start command with host binding, port mapping (e.g., 8000), and enable code reload; declare dependencies on the Postgres and MinIO services.
   * **Frontend**: point the build context to `./frontend`; set any necessary environment variables; define the start command for your React dev server; map port 3000; mount your source code directory and the `node_modules` folder.
3. Declare named volumes at the bottom of the file to persist Postgres and MinIO data across restarts.

---

## 2. Launching Services

1. From the project root, run the Compose up command with build and detached flags (e.g., `docker-compose up --build -d`).
2. Verify that all services are up and running using the Compose ps command.
3. Confirm access to each service via its mapped port:

   * PostgreSQL on `localhost:5432`
   * MinIO API on `localhost:9000` and web console on `localhost:9001`
   * Backend API on `localhost:8000`
   * Frontend on `localhost:3000`

---

## 3. PostgreSQL Tasks

* Connect to the database using the psql CLI with the appropriate connection string.
* Apply or roll back schema migrations using your chosen migration tool.
* Create database backups using the CLI dump command.
* Restore the database from backups using the CLI restore command.

---

## 4. MinIO Tasks

* Open the MinIO web console and log in with the root credentials.
* Create a bucket named `recipe-photos`.
* In your application environment, set the MinIO endpoint URL, access key, secret key, and the bucket name.
* Use your language’s S3-compatible SDK (e.g., boto3 for Python) pointed at the MinIO endpoint for uploads and downloads.

---

## 5. Integration Tips

* Reference Compose service names (e.g., `postgres`, `minio`) in your application environment variables for internal networking.
* Leverage the default network created by Compose so services can communicate by name.
* Use named volumes to maintain data persistence between restarts.

---

## 6. Cleanup & Management

* Stop all running services using the Compose down command.
* Remove associated volumes (if you want to reset data) by including the volume flag.
* Inspect service logs in real-time with the Compose logs command.

---

## 7. Next Steps

* Automate database migrations at container startup.
* Add health checks for Postgres and MinIO in the Compose file.
* Integrate the Compose workflow into your CI/CD pipeline.
* Plan for production deployment by translating these configurations to AWS ECS/Fargate or a Kubernetes cluster.

---

*End of DevOps Setup Guide*
