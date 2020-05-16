## Python gRPC server

### Usage 
#### Server

**Local**

```bash 
make server 
```

**Docker**

```bash 
docker build -t grpc-server .
docker run -it -p 50051:50051 grpc-server
```

#### Client 

**Local**

```bash 
make client 
```

```bash
docker build -t grpc-server .
docker run -it -p 50051:50051 grpc-server src/commands/client.py
```

### Tools 

**poetry**

```bash
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
$ poetry self update
$ poetry config virtualenvs.in-project true
$ poetry install
```

To start server and call it by client is the below.

```bash 
make server 
make client 
```

**protobuf & gPRC**

```bash
$ brew install protobuf
$ brew install grpc
```

After started server, 

```bash 
$ grpc_cli ls localhost:50051
```