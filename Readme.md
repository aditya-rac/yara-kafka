# YARA-Kafka Malware Detection Project

This project demonstrates how to capture real-time network traffic using Kafka, detect malware using YARA rules, and trigger email notifications upon malware detection. The project is divided into three key components: dynamic stream production, malware injection, and malware detection.

## Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
  - [Step 1: Install Kafka and Zookeeper](#step-1-install-kafka-and-zookeeper)
  - [Step 2: Set Up Python Environment](#step-2-set-up-python-environment)
  - [Step 3: Setup Docker and Run Kafka/Zookeeper](#step-3-setup-docker-and-run-kafka-zookeeper)
  - [Step 4: Setting Up Environment Variables](#step-4-setting-up-environment-variables)
  - [Step 5: Running the Project](#step-5-running-the-project)
- [Code Breakdown](#code-breakdown)
  - [1. Dynamic Stream (dynstr.py)](#1-dynamic-stream-dynstrpy)
  - [2. Malware Injection (inject.py)](#2-malware-injection-injectpy)
  - [3. Malware Detection (capstr.py)](#3-malware-detection-capstrpy)
- [What I Have Done](#what-i-have-done)
- [Future Improvements](#future-improvements)
- [License](#license)

## Project Overview

This project captures real-time network traffic, injects malware (EICAR test string), detects it using YARA rules, and sends email alerts when malware is found.

## Prerequisites

Make sure you have the following tools and modules installed on your system:
- Docker
- Kafka and Zookeeper
- Python 3.6+ with these modules:
  - kafka-python
  - yara-python
  - smtplib

You'll also need:
- WSL (Windows Subsystem for Linux) if you're running on a Windows machine.
- App Password for Gmail to enable email notifications.

## Project Setup

### Step 1: Install Kafka and Zookeeper

1. Download and install Docker from [here](https://www.docker.com/).
2. Create a `docker-compose.yml` file to run both Kafka and Zookeeper. Example:
   
   ```yaml
    version: '3'
    services:
    zookeeper:
        image: bitnami/zookeeper:latest
        environment:
        - ALLOW_ANONYMOUS_LOGIN=yes
        ports:
        - "2181:2181"
        networks:
        - kafka-net

    kafka:
        image: wurstmeister/kafka:latest
        environment:
        - KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092
        - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
        - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
        - KAFKA_BROKER_ID=1
        - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
        ports:
        - "9092:9092"
        depends_on:
        - zookeeper
        networks:
        - kafka-net

    networks:
    kafka-net:
        driver: bridge

Run Kafka and Zookeeper:

bash
    docker-compose up -d --build

Step 2: Set Up Python Environment
Install the required Python libraries:

bash
    pip install kafka-python yara-python smtplib

Step 3: Setup Docker and Run Kafka/Zookeeper
To check if Kafka and Zookeeper are running, use:

bash
    docker ps

Step 4: Setting Up Environment Variables
To avoid hardcoding sensitive credentials like your email password, use environment variables.

On Linux/WSL, set them like this:

bash
    export SENDER_EMAIL="your-email@gmail.com"
    export SENDER_PASSWORD="your-app-password"
    export RECIPIENT_EMAIL="recipient-email@gmail.com"

Replace the placeholders with your actual email and app password.
DO NOT USE YOUR ACTUAL PASSWORD, CREATE AN APP PASSWORD IF NECESSARY (browse google or ask chatgpt for instructions)

Step 5: Running the Project
    Start Kafka and zookeeper by running:

    bash 
        docker-compose up -d

    To verify the stream in Docker: 
    Topic: real-network-traffic 
    (Steps to be done after running dynstr.py):

    Enter the stream:
    bash
        docker exec -it <kafka_container_id> /bin/bash


    enter the stream:
        bash
        docker exec -it <kafka_container_id> /bin/bash

    to run stream from beginning:
    bash
        cd /opt/kafka/bin
        ./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic real-network-traffic --from-beginning


    delete the current stream: 
    bash
        kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic real-network-traffic


    recreate the current stream: 
    bash
        kafka-topics.sh --bootstrap-server localhost:9092 --create --topic real-network-traffic --partitions 1 --replication-factor 1


Run the dynamic stream producer:

bash 
    python3 dynstr.py

Inject the malware string (EICAR) into the stream:

bash 
    python3 inject.py

Run the malware detection consumer:

bash
    python3 capstr.py


 Breakdown
1. Dynamic Stream (dynstr.py)
    This script captures live network traffic from TCPDump and sends the data to a Kafka topic (real-network-traffic).

Key components:
    KafkaProducer: Streams captured network traffic into Kafka.
    tcpdump: Captures packets.

2. Malware Injection (inject.py)
This script injects a predefined EICAR test string (mimicking malware) into the Kafka stream.

3. Malware Detection (capstr.py)
This script consumes the Kafka stream, applies YARA rules to detect malware, and sends email alerts if malware is found.

What I Have Done
    Kafka Stream Setup: Captured real-time network traffic and streamed it into Kafka using Python.
    Malware Detection: Implemented YARA rules for malware detection.
    Email Notifications: Sent email alerts upon detecting malware in the stream.
    Docker Integration: Set up Kafka and Zookeeper using Docker for a clean and replicable environment.
    Future Improvements
    Enhanced Malware Detection: Add more YARA signatures for various types of malware.
    Scalability: Deploy this setup in a distributed system with real-time data pipelines.
    Visualization: Integrate a dashboard (e.g., Grafana) for monitoring the network traffic.
    License
    This project is licensed under the MIT License - see the License.txt file for details.

Future Improvements
    Enhanced Malware Detection: Add more YARA signatures for various types of malware.
    Scalability: Deploy this setup in a distributed system with real-time data pipelines.
    Visualization: Integrate a dashboard (e.g., Grafana) for monitoring the network traffic.

License
This project is licensed under the MIT License - see the License.txt file for details.
