import grpc
import locations_pb2
import locations_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = locations_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = locations_pb2.LocationMessage(
    id = 29,
    latitude = "-122.290524",
    longitude = "37.553441",
    creation_time = "2020-08-18T10:37:06",
    person_id = 1
)


response = stub.Create(location)
print(response)
