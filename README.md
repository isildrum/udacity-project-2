# UdaConnect
## How to run

### 1) Build, Tag and Push each docker image from the modules directory
1. Persons API
```
docker build -t udaconnect-persons-api -f ./persons-api/Dockerfile ./persons-api
docker tag udaconnect-persons-api isildrum/udaconnect-persons-api:v1
docker push isildrum/udaconnect-persons-api:v1
```

2. Locations API
```
docker build -t udaconnect-locations-api -f ./locations-api/Dockerfile ./locations-api
docker tag udaconnect-locations-api isildrum/udaconnect-locations-api:v1
docker push isildrum/udaconnect-locations-api:v1
```

3. Locations gRPC
```
docker build -t udaconnect-locations-grpc -f ./locations-grpc/Dockerfile ./locations-grpc
docker tag udaconnect-locations-grpc isildrum/udaconnect-locations-grpc:v1
docker push isildrum/udaconnect-locations-grpc:v1
```

4. Locations Kafka
```
docker build -t udaconnect-locations-kafka -f ./locations-kafka/Dockerfile ./locations-kafka
docker tag udaconnect-locations-kafka isildrum/udaconnect-locations-kafka:v1
docker push isildrum/udaconnect-locations-kafka:v1
```

#### Docker Note
isildrum must be replaced by a different docker id for push testings

### Environment Setup
Vagrant with VirtualBox will be used to run K3s.

#### Initialize K3s
In this project's root, run `vagrant up`. 

#### Set up `kubectl`
1. SSH into the Vagrant environment 
2. Retrieve the Kubernetes config file used by `kubectl`. 

```bash
$ vagrant ssh
$ sudo cat /etc/rancher/k3s/k3s.yaml
```

Copy the contents from the output issued into your a new file `~/.kube/config` and paste the contents of the `k3s.yaml` output here.

Afterwards, you can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.

### Apply deployments
`kubectl apply -f deployment/`.

Note: To seed the database with dummy data, use the command `sh scripts/run_db_command.sh <POD_NAME>` against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`). 

### Verifying it Works
Once the project is up and running, you should be able to see 8 deployments and 11 services in Kubernetes:
`kubectl get pods` and `kubectl get services` - They should return something like this

```bash
kubectl get pods
NAME                                          READY   STATUS    RESTARTS   AGE
kafka-0                                       1/1     Running   0          23h
kafka-zookeeper-0                             1/1     Running   4          4d1h
postgres-5f676c995d-c8mmw                     1/1     Running   5          4d21h
udaconnect-persons-api-7bff58fd5c-l8c44       1/1     Running   4          4d1h
udaconnect-app-657bb5c8bb-tth5l               1/1     Running   5          4d21h
udaconnect-locations-grpc-cfd7566c-v877r      1/1     Running   0          22h
udaconnect-locations-api-84654bbc47-bq8pt     1/1     Running   0          73m
udaconnect-locations-kafka-6b57cf449c-rwtj6   1/1     Running   0          57m

kubectl get services
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
kubernetes                  ClusterIP   10.43.0.1       <none>        443/TCP                      10d
postgres                    NodePort    10.43.54.78     <none>        5432:30699/TCP               4d21h
udaconnect-app              NodePort    10.43.190.122   <none>        3000:30000/TCP               4d21h
udaconnect-locations-api    NodePort    10.43.59.132    <none>        5001:30001/TCP               4d21h
udaconnect-persons-api      NodePort    10.43.74.77     <none>        5002:30002/TCP               4d21h
kafka-zookeeper-headless    ClusterIP   None            <none>        2181/TCP,2888/TCP,3888/TCP   4d1h
kafka-zookeeper             ClusterIP   10.43.57.252    <none>        2181/TCP,2888/TCP,3888/TCP   4d1h
kafka-headless              ClusterIP   None            <none>        9092/TCP,9093/TCP            4d1h
kafka                       ClusterIP   10.43.183.143   <none>        9092/TCP                     4d1h
udaconnect-locations-grpc   NodePort    10.43.156.16    <none>        5005:30003/TCP               3d14h
kafka-0-external            NodePort    10.43.202.147   <none>        9094:30005/TCP               23h
```


These pages should also load on your web browser:
* `http://localhost:30001/` - OpenAPI Documentation for Location
* `http://localhost:30002/` - OpenAPI Documentation for Persons
* `http://localhost:30001/api/persons/` - Base path for Location API
* `http://localhost:30002/api/locations/` - Base path for Persons API
* `http://localhost:30000/` - Frontend ReactJS Application