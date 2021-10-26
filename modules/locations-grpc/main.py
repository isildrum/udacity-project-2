import time
from concurrent import futures

import logging
import grpc
import locations_pb2
import locations_pb2_grpc
from kafka import KafkaProducer
import json

#Kafka Parameters
TOPIC_NAME = 'udaconnect-locations'
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9092'

class LocationServicer(locations_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        print("Received a message!")

        request_value = {
            "id": request.id,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "creation_time": request.creation_time,
            "person_id": request.person_id
        }
        print(request_value)

        #Send Kafka Message
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        producer.send(TOPIC_NAME, json.dumps(request_value).encode('utf-8'))
        producer.flush()
        return locations_pb2.LocationMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
locations_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)