fmt:
	find . -name "*.proto" | xargs clang-format -i

compile:
	protoc -I=. --python_out=../python/proto --grpc_out=../python/proto route_guide.proto