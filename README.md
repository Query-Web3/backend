### Test 

```sh
$ go test ./...
```

### Build docker
```sh
$ docker build -t query_web3_backend .
```

### Run dev mysql with docker
```sh
$ docker run --name mysql-dev -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root123456 -e MYSQL_DATABASE=dev -e MYSQL_USER=dev -e MYSQL_PASSWORD=123456 -d mysql
```

### Run with go
```sh
$ go run server/server.go
```

### Run with docker
```sh
$ docker run --network host query_web3_backend
```