# import argparse
# from influxdb import InfluxDBClient
# from influxdb.client import InfluxDBClientError
# import datetime
# import time
# 
# USER = 'root'
# PASSWORD = 'root'
# DBNAME = 'SmartHome'
# HOST = 'localhost'
# PORT = 8086
# dbclient = None;
# 
# def dbWriteBme(temp, hum):
#     dbclient = InfluxDBClient(host=HOST, port=PORT, username=USER, password=PASSWORD, database=DBNAME)
#     data_point = getSensorData(temp, hum)
#     dbclient.write_points(data_point)
#     print("Written Temperature/Pressure data")
#     time.sleep(2)
#         
# def getSensorData(temp, hum):
#     now = time.gmtime()
#     pointValues = [
#         {
#             "time": time.strftime("%Y-%m-%d %H:%M:%S", now),
#             "measurement": 'reading',
#             "tags": {
#                 "nodeId": "node_1",
#             },
#             "fields": {
#                 "Temperature": float(temp),
#                 "Humidity": float(hum),
#             },
#         }
#     ]
#     
#     return(pointValues)