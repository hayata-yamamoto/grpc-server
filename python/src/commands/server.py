from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from src.proto import route_guide_pb2_grpc, route_guide_pb2
from src.server import RouteGuideServicer


def main() -> None:
    executors = futures.ThreadPoolExecutor(max_workers=10)
    server = grpc.server(executors)
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server)

    SERVICE_NAMES = (
        route_guide_pb2.DESCRIPTOR.services_by_name['RouteGuide'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    main()
