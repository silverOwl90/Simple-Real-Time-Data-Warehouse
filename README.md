# Simple-Real-Time-Data-Warehouse

The goal of this repository is to provide a **starting point** for building a **simple Data Warehouse** that enables **real-time data processing** using a **Big Data technology stack**.

🔥 **Architecture for Real-Time Processing**

-   **Kafka** → Receives and transmits real-time data.
-   **Spark Streaming** → Processes incoming data and sends it to PostgreSQL.
-   **PostgreSQL** → Stores processed data for analytical queries.
-   **Metabase** → Enables real-time data visualization.
-   **Docker Compose** → Orchestrates all containerized services.
-   **ZooKeeper** → It is used as a coordination service to manage the different Kafka nodes.

## 🔹 **How to Test It**

1️⃣ **Start the containers with Docker Compose**

    docker-compose up -d

   Verify that all containers are running with:

       docker ps

2️⃣ **Create the Database in PostgreSQL**

Access PostgreSQL inside the container:

    docker exec -it postgres psql -U admin -d datawarehouse

 Create the table to store processed data:

    CREATE  TABLE realtime_data (
        id SERIAL PRIMARY KEY,
        sensor VARCHAR(50),
        valor INT, timestamp  TIMESTAMP  DEFAULT NOW()
    );

Verify that the table was created:

    \dt


3️⃣ **Simulate Data in Kafka**
To simulate streaming data in Kafka, follow these steps:

Enter the Kafka container:

    docker exec -it kafka bash 

Create a topic named `datos_realtime`:

    kafka-topics --create --topic datos_realtime --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 

Verify that the topic was created:

    kafka-topics --list --bootstrap-server kafka:9092 

Send test data to Kafka:

    kafka-console-producer --topic datos_realtime --bootstrap-server kafka:9092

Then, type some JSON messages simulating real-time data (press **Enter** after each line):

    {"id":  "1",  "sensor":  "temperature",  "valor":  25,  "timestamp":  "2025-03-05 14:30:00"} 
    {"id":  "2",  "sensor":  "humidity",  "valor":  80,  "timestamp":  "2025-03-05 14:30:10"}

4️⃣ **Run Spark Streaming**

The Spark Streaming script provided earlier must be executed from a Spark container. To test it:
Access the Spark Master container:

    docker exec -it spark-master bash

Run the Spark Streaming script:

    spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 /opt/bitnami/spark/scripts_spark/spark_streaming.py


5️⃣ **Verify That Data Is Stored in PostgreSQL**
After a few seconds, check if the Kafka data was stored in PostgreSQL:

Access PostgreSQL again:

    docker exec -it postgres psql -U admin -d datawarehouse

Query the table:

    SELECT  *  FROM realtime_data; 

🚀 **If you see the records, everything is working correctly! 🎉**

6️⃣ **Visualize Data in Metabase**
Access **Metabase** in your browser:  
👉 **[http://localhost:3000](http://localhost:3000)**

Configure **PostgreSQL** as a data source:

-   Click on **Add Database**.
-   Type: **PostgreSQL**.
-   **Host**: `postgres`
-   **Database**: `datawarehouse`
-   **User**: `admin`
-   **Password**: `admin123`

Create a **Dashboard** to visualize real-time data.

7️⃣ **Clean Up Containers When Done**
If you want to stop and remove the containers:

    docker-compose down -v


## 🔥 **Benefits of This Approach**  
✅ **Low Latency** → Data is processed in seconds or milliseconds.  
✅ **Scalability** → Kafka and Spark handle large volumes of data.  
✅ **SQL & Advanced Analytics** → PostgreSQL or ClickHouse optimize queries.  
✅ **Real-Time Visualization** → Metabase/Superset dynamically update dashboards.


## 🚀 **Optional Improvements**  
🔹 Replace **PostgreSQL** with **ClickHouse** for faster queries.  
🔹 Add **Apache Flink** for lower-latency processing than Spark.  
🔹 Set up **Airflow** to automate pipelines.




