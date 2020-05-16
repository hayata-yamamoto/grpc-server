import grpc

from src.proto import route_guide_pb2_grpc
from src.client import *


def main() -> None:
    with grpc.insecure_channel('server:50051') as chan:
        stub = route_guide_pb2_grpc.RouteGuideStub(chan)
        print("-------------- GetFeature --------------")
        guide_get_feature(stub)
        print("-------------- ListFeatures --------------")
        guide_list_features(stub)
        print("-------------- RecordRoute --------------")
        guide_record_route(stub)
        print("-------------- RouteChat --------------")
        guide_route_chat(stub)


if __name__ == '__main__':
    import logging

    logging.basicConfig()
    main()
