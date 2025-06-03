# Smart-City-Real-Time-Data-Engineering

![image](https://github.com/user-attachments/assets/4cf40083-a66a-4698-a835-58ceac7fd417)

Project Setup
Docker

Kafka and Spark code and configuration


Creating zookeeper and Broker docker containers
```
SmartCityRvm touch docker-compose.yaml
```

![image](https://github.com/user-attachments/assets/93092a5c-029b-42ff-92e8-dcadb96dc689)

Zookeeper, Broker, Spark master and workers docker containers creation
![image](https://github.com/user-attachments/assets/c7c33675-3fe4-4aba-856f-d4bcdac5ddb9)

Checking Spark cluster creation
![image](https://github.com/user-attachments/assets/7e7d898a-33f1-4877-901d-3c2d31d36d3b)

Checking Spark cluster creation

![image](https://github.com/user-attachments/assets/5d174ba5-b238-44fe-b4ac-ded4e53d1a8d)

Openweather
Registration and endpoint Discovery
(after this go to the code and implement data extraction)
https://openweathermap.org/api

Free tier weather data:
https://openweathermap.org/current
Free tier air polution data:
https://openweathermap.org/api/air-pollution 
  
![image](https://github.com/user-attachments/assets/6b5be098-dd17-4f02-b6bb-6d0226cbf9e0)

![image](https://github.com/user-attachments/assets/569a5547-b434-4623-b047-ccb5a21ec449)


Api Key to call the services from your code
![image](https://github.com/user-attachments/assets/6489bb3a-2a52-4ed8-b009-7430ca1e7395)

![image](https://github.com/user-attachments/assets/5a5b651d-55e4-496d-851d-a7f740dca83d)

 ![image](https://github.com/user-attachments/assets/3230dbdf-fce2-46ef-85f8-b95c3a87aff5)

  
  
OpenWeather API Endpoints Discovery
It takes up to 2 hours been able to get a 200.Ok response.
POSTMAN COLLECTION within my Repository
![image](https://github.com/user-attachments/assets/c584a05a-12c3-4134-9cd9-e84391fbf3a4)
 




  
Getting location information from smatphone GPS Tracker: My Tracker
Note: this was my old Iphone SE with the language set in German, because I was there for five years. I still keep it and I used it to track my Motorbike driving lessons.
The records are from 2 years ago since then I was learning how to create an End-to-End project with the data. 
  



AWS
•	Create buckets and its Public policies
Empty buckets, the folders will be created as you run the code
•	Create access key 

![image](https://github.com/user-attachments/assets/ee2d6355-0b93-4de1-b1b8-146f2bfdd68e)
  
![image](https://github.com/user-attachments/assets/1630aef6-7b85-4a0d-a4cb-266c8e9cdbad)

![image](https://github.com/user-attachments/assets/636b4307-5ad3-4a3f-94b3-e996da094685)

![image](https://github.com/user-attachments/assets/a33a8a44-fb14-457f-addd-40e93c2e3aa8)

![image](https://github.com/user-attachments/assets/654c1f3e-9fa5-449f-b553-0c7d69c36d99)
  

Refresh buckets to update de policy

![image](https://github.com/user-attachments/assets/02afa3ff-f054-49af-9511-d1816d5e3daf)

 
Create an User

![image](https://github.com/user-attachments/assets/bc8feaa8-f698-45bf-8bfd-8a307055644e)

 
Add permissions to the user

![image](https://github.com/user-attachments/assets/6e789626-a023-4d8d-ade7-2dd23ae7e6fd)

 
Create Access key to the User.
That enables to load the data from spark (Docker) to the S3 buckets.
The keys will be passed in arguments withtin the code
 
![image](https://github.com/user-attachments/assets/0ca3d7b7-0839-434a-b1c3-6d457934de25)

![image](https://github.com/user-attachments/assets/4be47290-d11a-48bd-bf95-ebd516ed11cb)
  
![image](https://github.com/user-attachments/assets/82145b20-fa04-49c8-9233-0770aabfc34f)

![image](https://github.com/user-attachments/assets/79db1289-8a5b-4eaa-97ad-2e87005f0f8b)

  
Trigger the Streaming process
•	Docker compose up –d
•	Trigger kafka and send data to the topics.
Run: jobs/main.py
•	Trigger Spark to consume topics and send information to S3.
Run: docker exec -it smartcityrvm-spark-master-1 spark-submit `
--master spark://spark-master:7077 `
--packages org.apache.spark:spark-sql-kafka-0- 10_2.12:3.5.0,org.apache.hadoop:hadoop- aws:3.3.1,com.amazonaws:aws-java-sdk:1.11.469 ` jobs/spark-city.py
All the relevant commands are available into a .txt file in my 
  
  
![image](https://github.com/user-attachments/assets/1ed1f8f9-b2d6-4022-a0c8-5a117cd2de3b)

![image](https://github.com/user-attachments/assets/b67c185f-485c-4ab7-a766-5262afb0a63d)

![image](https://github.com/user-attachments/assets/a1c71663-8c19-4485-9ca3-48a9d2e7c2d0)
 
SOME FAILED TESTS 
To avoid the process to fail, I needed to set this option “failOnDataloss” to “False”.
Due to the Broker consistency and connection with Spark, it may occurs that few registers are lost, and this option doesnot allow the process to continue if there are some data missing by default.

“The ERROR:
ERROR MicroBatchExecution: Query [id = fac716d9-cdde-491c-bab8-9decd5dfa957, runId = 27662566-449f-41b6-965f-
f88387f5d424] terminated with error
java.lang.IllegalStateException: Partition weather_data-0's offset was changed from 30 to 14, some data may have been missed.
Some data may have been lost because they are not available in Kafka any more; either the data was aged out by Kafka or the topic may have been deleted before all the data in the topic was processed. If you don't want your streaming query to fail on such cases, set the source option "failOnDataLoss" to "false". “ 

![image](https://github.com/user-attachments/assets/2ea6cc75-2e1d-43e4-a9d4-6f8f9f3e8223)

Once corrected the issue before, the streaming process from spark to S3 runs properly

![image](https://github.com/user-attachments/assets/5dbad1db-ad11-4f5d-961b-c4cb346972f4)

![image](https://github.com/user-attachments/assets/549e9aa7-3740-4f92-89a1-95d2e936b896)

![image](https://github.com/user-attachments/assets/2073f9f0-a07e-46d7-b71a-5d2139c68419)

![image](https://github.com/user-attachments/assets/d3e656e1-ca56-4f8f-b115-acab2ae55dfa)
  
AFTER AROUND 35 MINUTES, ALL THE LINES FROM THE .GPX FILES WERE PROCESSED, FIRST
TO KAFKA INTO TOPICS AND AFTER CONSUMED BY SPARK TO S3
 
![image](https://github.com/user-attachments/assets/ff297875-e0d3-42a4-b0a8-7c870065b496)



AWS
•	S3 Buckets contain all the data (.parquet) and folders defined in the code 

![image](https://github.com/user-attachments/assets/b6184f22-0415-4717-91fc-056abe476b32)

![image](https://github.com/user-attachments/assets/052cea05-a296-44af-8694-51fb517b6ccf)

![image](https://github.com/user-attachments/assets/351166d8-e050-4c80-b520-5d6488e4140f)


AWS
•	Create crawlers to transform all the .parquet files into an explorable structure as tables in a database. 
 
![image](https://github.com/user-attachments/assets/77a8b762-cce1-4701-acf3-43d882c973e7)

![image](https://github.com/user-attachments/assets/e85e849e-4fe7-4c78-b1cd-ea965d96886c)

![image](https://github.com/user-attachments/assets/a2ca634f-f19e-472a-b6ab-0e7c38132934)

![image](https://github.com/user-attachments/assets/704ed410-3065-4f83-892c-782656ba917c)

![image](https://github.com/user-attachments/assets/b3083639-ff8e-4f71-9c10-0ce70a15d71c)

![image](https://github.com/user-attachments/assets/3cab77e2-c198-4d91-98ee-25d6032cf416)

![image](https://github.com/user-attachments/assets/926013cb-7401-45d0-ba72-68e56944562d)
  
You probably don’t have an IAM role created. Just create a new one.

![image](https://github.com/user-attachments/assets/e0ca14c4-1ece-4927-bf3e-99af8a97bf25)

 ![image](https://github.com/user-attachments/assets/8a7fd883-ad2a-4c1f-b7fa-75afe184834a)

![image](https://github.com/user-attachments/assets/55f336e5-b46d-41ee-9ad9-0a74a26adfcb)
  
You probably don’t have a Database created. Just create a new one.

 ![image](https://github.com/user-attachments/assets/c5956fa6-adb1-4bff-8725-4e6dae0fbebe)

![image](https://github.com/user-attachments/assets/ee343efd-05ae-43f9-abce-d6fdb83e8e99)

![image](https://github.com/user-attachments/assets/9d0f42c1-9f74-4bda-b600-eeaa578a4c91)
  
Advanced options by default, I didn’t touched it

 ![image](https://github.com/user-attachments/assets/7da32b79-af7c-4627-b292-a5f8005d1aa6)

![image](https://github.com/user-attachments/assets/4fbbfbad-7ce8-42da-ba30-73f905894068)

  
Run the crawler to start transforming the .parquet files
Run this when the streaming process is completed only!!!

 ![image](https://github.com/user-attachments/assets/fe38a627-afba-41d1-b966-37805f4f6182)

![image](https://github.com/user-attachments/assets/5cb65d69-6771-4a8e-b3bf-cd9bdae5ffc2)

![image](https://github.com/user-attachments/assets/c015d4fd-f01e-4308-8db4-eef51ca587b4)

AWS
•	Access to Glue and explore the transformed tables, available to be queried.
•	The queries and exploration are made from ATHENA as you click
on “table data” 

![image](https://github.com/user-attachments/assets/9cdc0f33-49a8-4b7f-9f3f-671e45df9fd6)

![image](https://github.com/user-attachments/assets/9225e8f3-76a9-4231-abb0-654532d33ce7)
 
You are not able to run a query against the tables until you set an output directory to the queries

![image](https://github.com/user-attachments/assets/735da45c-07ca-4380-9484-6e8cd899177a)

![image](https://github.com/user-attachments/assets/016b3bd1-ff40-493d-98d5-8241045dbfa6)

Browse your bucket address and write by hand “/output” at the end, thus a new folder will be created into S3 to save the queries results
![image](https://github.com/user-attachments/assets/30ce55c8-365a-40e8-af5f-e4856627837c)

Now you should be able to run an exploratory query to all the tables

![image](https://github.com/user-attachments/assets/c387cf8d-8ce0-4234-8280-9dca83326e3c)
 
![image](https://github.com/user-attachments/assets/5bd7e9a9-e0d2-4ba5-bdae-eccaef4b2d5b)

![image](https://github.com/user-attachments/assets/da72d8f8-8ce5-48eb-9541-386f62ddbb72)
 
![image](https://github.com/user-attachments/assets/65bd76b9-5a42-474c-9e29-3f5e63926b8f)


AWS
Redshift cluster creation, configuration and permissions 

![image](https://github.com/user-attachments/assets/5be5f0d3-169d-4eb1-9b39-ea502a145c39)

![image](https://github.com/user-attachments/assets/a17ea93c-6a0d-4e83-8570-a4ad9152acf1)
  
![image](https://github.com/user-attachments/assets/e6fa043e-f15b-4857-80b9-df28bf3df7c0)
  
![image](https://github.com/user-attachments/assets/83022623-e139-4083-a030-bbcca0d165fb)

![image](https://github.com/user-attachments/assets/88d9f5f9-de61-4a41-b36e-bfb4fd616b36)
  
![image](https://github.com/user-attachments/assets/e4db6276-af51-4218-a39b-9d87bb75730b)
  
![image](https://github.com/user-attachments/assets/bf5abf5c-980f-4a65-ae75-4fca9019e48b)

![image](https://github.com/user-attachments/assets/b867851d-7ba9-48c6-8255-c416a43571ee)
  
  
It doesnot refresh automaticaly, so you need to refresh the create cluster page and fill in all the information again.
By the iam roles you will be able to select the recently created role
![image](https://github.com/user-attachments/assets/9fbed18d-b8c9-43e2-a5bb-08a737ce9984)

 
If you don’t have any VPC. You need to create a new VPC which créate ifself automatically a security group
(default).

You need to create a Cluster subnet group (this is mandatory to create the redshift cluster). This subnet group Will be assigned to the VPC created before. See next slides
 
![image](https://github.com/user-attachments/assets/21415bff-86f2-4aa5-9ada-ca311b40b28b)

![image](https://github.com/user-attachments/assets/04f098d1-7a74-436f-a624-9aed823fca31)

![image](https://github.com/user-attachments/assets/3b2655e4-c52d-4fad-a250-2361945e04c0)

![image](https://github.com/user-attachments/assets/c4eed37b-9c13-460c-94e5-4e8359d119d7)

![image](https://github.com/user-attachments/assets/215a2712-2980-47de-99c5-31be7c1c718e)

Important:
Go to VPC console > Security Groups > security group (default)

There add an inbound rule:
Type:Custom port: 5439 source: My Ip

This allow the traffic from your IP to readshift. Without this you won’t be able to connect redshift from
your pc

![image](https://github.com/user-attachments/assets/42560c82-9c11-4c40-9543-15c03547a9a6)

![image](https://github.com/user-attachments/assets/12adf035-9571-4522-be9c-eae689caf645)
  
create a Cluster subnet group (this is mandatory to create the redshift cluster). This subnet group Will be
assigned to the VPC created before. See next slides

![image](https://github.com/user-attachments/assets/597d850a-0ff2-4a8d-b97a-99a2ffb6adf2)

![image](https://github.com/user-attachments/assets/f3b6453d-e7be-4997-8ecf-16993d87b5ea)

![image](https://github.com/user-attachments/assets/a178303f-6e77-4d75-8cfc-2afde4521af7)

![image](https://github.com/user-attachments/assets/572fb64e-1b8e-4823-9ab9-58b9ef11de4a)


After resfreshing, again fill in the the fields…
If you have read this documentation previously, you can create all the needed VPC and cluster subnet group in advance to ease the process 
  
![image](https://github.com/user-attachments/assets/afbd4688-1f2f-4cf7-9cb0-0d50b98c27ce)

![image](https://github.com/user-attachments/assets/b75970d1-3349-4662-8b1e-7323076afe85)
  
It takes around 15 minutes to be created

![image](https://github.com/user-attachments/assets/d27a1a43-63bc-4d83-babf-2c204addc808)

 
The Redshift cluster is already created, then lets explore the content and create an external schema that points to the tables on Glue. In this way you will be able to query Redshift database directly and retrieve the transformed data persisted in Glue.

To do that, just copy the jdbc connection chain and create a server connection in your computer using Dbeaver.

![image](https://github.com/user-attachments/assets/d2139707-eab4-4542-9f25-497811edd715)
 
![image](https://github.com/user-attachments/assets/4e5fa036-fc22-40a5-bf6e-dfd4f259eb50)
  
Once connected to redshift you can explore the existing schemas.
In this case, public is where we want to work in, but there aren’t tables yet.

![image](https://github.com/user-attachments/assets/0b4c1353-1020-4a79-b987-3b3b2775b79c)

Create an external schema pointing to the Glue catalog and created database. Pass your IAM role – go to IAM and select the role created before and copy the arn. This schema allows to query against redshift and retrieving the data from Glue
 
![image](https://github.com/user-attachments/assets/f968f42d-1d50-47d1-8983-a6adf5e983f7)

![image](https://github.com/user-attachments/assets/1779d354-d5cf-4168-a8f0-ef3cf1cdc7d3)

![image](https://github.com/user-attachments/assets/6d76e9b2-6cf8-4ef2-9a14-717d6079d4c3)

![image](https://github.com/user-attachments/assets/23f8cfe3-f070-4709-ae77-31f71446a366)

![image](https://github.com/user-attachments/assets/ffa652b4-24bd-4e2d-9e73-0f1b48479865)

POWER BI
•	DirectQuery or import the data from redshift
•	With a student License / Premium / PRO you are able to use the redshift-powerBI connector 
On the backgroung you can see other tables. This was the test I made before in order to prepare the dashboard a bit, to avoid overcosts for having the aws services deployed. In this way, It was just conecting, cleaning some columns and visualize.

 ![image](https://github.com/user-attachments/assets/2bb09820-fc68-4882-ab58-a807bdf846b5)






It is not a streaming intake from redshift.

The best way I found to simulate a streaming was implementing the tool “play axis” in powerbi.

This allows to represent the data sequentially. 

![image](https://github.com/user-attachments/assets/8e9282b2-e204-4bd8-a397-afb43e4b0b9e)



AWS LAMBDA
Create a Lambda function to simulate a streaming leverage.
The function queries against redshift, getting the vehicle_data table, and sending the file in little batchs to Power BI API. 

![image](https://github.com/user-attachments/assets/0ec496c4-619f-4f65-8495-ee6e5a363798)

![image](https://github.com/user-attachments/assets/fd73f6ac-b9eb-485c-8338-f5f22026a42b)


La Lambda’s layer allows to upload the libraries needed to run the function properly. This aws environment does not
have many Python libraries installed by default.
Check the Commands_and_Comments.txt file in my Repo to know hoy to create this python.zip. 

![image](https://github.com/user-attachments/assets/470906c3-9d10-4ddf-89b2-d95da4de377c)

![image](https://github.com/user-attachments/assets/8d1a63a4-78e7-4904-93c1-4e11bec3b379)



![image](https://github.com/user-attachments/assets/ace4930a-c4b9-4930-b6b1-5c7ee5342d00)






  

  





  



  







  




  
The same VPC as for Redshift.

Important:
Go to
VPC console > Security Groups
> security group (default) There add an inbound rule 
 
Wait until updating succes

And proceed adding a layer (which contains the Python libraries
 


  


  



  
Although I was able to query redshift from Lambda, unfortunately I pretended to save the table vehicle_data into a dataframe and transform it, in order to pass the data as Json to PowerBI API correctly.

That’s why the location columna in my code, retrieves a json containing latitude and longitud as key value in json format for this columna only.

the libraries needed to transform a dataframe with panda aren’t to much, the problem I found is the bunch of
libraries that work behind and ables the main library runs correctly.

I felt in an endless Flow of errors adding to the Layer all the libraries inside the Python.zip, until I reached the error below and I decided to stop and trying such streaming simulation with lambda in the next Project.
 
PowerBI API https://app.powerbi.com/groups/me/list?experience=power-bi
•	Create a new streaming data set
•	Select API
•	Give it a name and entry the fields (next slide)
 
PowerBI API
Once you add all the fields, PBI shows an example JSON schema which you must use in order to send the data to
the endpoint. 
PowerBI API
Finally you get the Endpoint URL and json schema to be used

 
PowerBI API
Create a dashboard
In my case I’m not receiving data because of the issue with the Lambda Layer and the library uploading






