# Real-Time Data Pipeline Using Kafka and Spark

## Data Pipeline Architecture

  

![](https://lh4.googleusercontent.com/eZykZAZj43p1oYAZFf_X3CINjHx6qz1rRevNptNWWisXYmDYDEae7Fhla7ETWZ2TmGRvTECBlMtFBe6aKHWaVUac7imu_hOXgVLZwFebuvE-_O_FmSZgdb5kBJAFMAxBl3AAgsYD)

-   ### API
   
	-  	 The API mimics the water quality sensor data similar to the one shared [here](https://data.world/cityofchicago/beach-water-quality-automated-sensors).
	    
	-   The implementation is done in flask web framework and the response is as follows:
	    

		‘2020-02-17T11:12:58.765969 26.04 540.1 13.12 Montrose_Beach 758028’

		![](https://lh6.googleusercontent.com/TDsc79yE-D_GBX7hFNrbgGlnP81TaRvBESeE2JvyEb8VaFzO_h1jNezTLsTg8CRsjfMtJOFrxPJi0EkqTOuRXlpP6U0SwuSMtFg4_rYYzNF5iASjx3MFIM4jKe5fjTKlVbAm4OMK)

-   ### Kafka Producer (Topic: RawSensorData)
    
	
	-   The data from the API stream is pushed to Kafka Producer under topic: RawSensorData
	    

  

		![](https://lh6.googleusercontent.com/KqaLvzLkdC2aYar0UeQ9raBgJgf0QXLyGe9GFr6z0uT6O-sx4ZizobVCdgIMTSZ8itXtiHfIThLHc5FoAwXtkA2U_lVZRJDQdLNvcNPKAIfS1Sa6GuiaTcCiABlpSlnhrfoSqn1s)

-   ### Apache Spark and Kafka Consumer (Topic: CleanSensorData)
    

	-   The data under the topic RawSensorData is streamed through Kafka Consumer. The data is then structured and validated using Spark.
	    

	  

	-   The cleaned data is then pushed to MongoDB and Kafka Producer under topic: CleanSensorData
    

  

		![](https://lh6.googleusercontent.com/DBMkx3tX90NCtokgNYT4BkjJGujCyeZk08X4w99vo2zfsBN9Yz1YGtb38Tcc3F6_HtMbML9NLVcHPFW310MDSSLWg8G8KoTuo-sC00aApDdNW9ql1ny605pwV6r5DS-Y5D325elU)

-   ### MongoDB
    

	-   The structured data is pushed to MongoDB collection with the following schema:
	    
		```markdown
		| Keys             | Data Type |
		|------------------|-----------|
		| _id              | Object Id |
		| Beach            | String    |
		| MeasurementID    | long      |
		| BatteryLife      | Double    |
		| RawData          | String    |
		| WaterTemperature | Double    |
		| Turbidity        | Double    |
		| TimeStamp        | timestamp |
		```  
  
  

-   ### Realtime Dashboard
    

	-   The dashboard is implemented in the bokeh visualization library and data is streamed using Kafka Consumer under topic CleanSensorData.
	    

		![](https://lh5.googleusercontent.com/qtt7B4EC1FCRpqWreTOrk74gAXTDvtJ3TxTKs6KWaAbtB_5MZ5-4-GSJYkbuLGRHMEUK5Gzp4njgEiklshdTs-LbCAhOeI-u96k5g9vf0IU6Av_RQx0CiR1PXY4jbMHkmesMnNhM)

  

## How to run the code

  

-   #### Start the API (port: 3030)
    

  		 python sensor.py
	    

  

-   #### Start Zookeeper
    

		 bash /opt/zookeeper-3.4.14/bin/zkServer.sh start
    

  

-   #### Start Kafka
    

		bin/kafka-server-start.sh config/server.properties
    

  

-   #### Create RawSensorData Topic
    

		   ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic RawSensorData
    

  

-   #### Create CleanSensorData Topic
    

		 ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic CleanSensorData
    

  

-  #### Push Data From API Stream to Kafka Topic: RawSensorData
    

		python push_data_to_kafka.py
    

  

-   #### Structure and Validate Data, Push To MongoDB and Kafka Topic CleanSensorData
    

		  ./bin/spark-submit structure_validate_store.py
    

  

-  #### View RawSensorData Topic
    

		bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic RawSensorData --from-beginning
    

  

-   #### View CleanSensorData Topic
    

		bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic CleanSensorData --from-beginning
    

  

-   #### Real-Time DashBoard - Visualization
    

		bokeh serve --show dashboard.py
