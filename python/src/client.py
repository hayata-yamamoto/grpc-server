import random
import logging
from typing import Any, Iterator

import grpc

from src.proto import route_guide_pb2, route_guide_pb2_grpc
from src.resources import read_route_guide_database


def make_route_note(message: Any, latitude: int,
                    longitude: int) -> route_guide_pb2.RouteNote:
    return route_guide_pb2.RouteNote(message=message,
                                     location=route_guide_pb2.Point(
                                         latitude=latitude,
                                         longitude=longitude))


def guide_get_one_feature(stub: route_guide_pb2_grpc.RouteGuideStub,
                          point: route_guide_pb2.Point) -> None:
    feature = stub.GetFeature(point)
    if not feature.location:
        print('server returned incomplete feature')
        return

    if feature.name:
        print("Feature called %s at %s" % (feature.name, feature.location))
    else:
        print('Found no feature at %s' % feature.location)


def guide_get_feature(stub: route_guide_pb2_grpc.RouteGuideStub) -> None:
    guide_get_one_feature(
        stub, route_guide_pb2.Point(latitude=409146138, longitude=-746188906))
    guide_get_one_feature(stub, route_guide_pb2.Point(latitude=0, longitude=0))


def guide_list_features(stub: route_guide_pb2_grpc.RouteGuideStub) -> None:
    rectangle = route_guide_pb2.Rectangle(
        lo=route_guide_pb2.Point(latitude=400000000, longitude=-750000000),
        hi=route_guide_pb2.Point(latitude=420000000, longitude=-730000000))

    print('looking for features between 40, -75 and 42, -73')

    features = stub.ListFeatures(rectangle)

    for feature in features:
        print("Feature called %s at %s" % (feature.name, feature.location))


def generate_route(feature_list: Any) -> Iterator[route_guide_pb2.Point]:
    for _ in range(0, 10):
        random_feature = feature_list[random.randint(0, len(feature_list) - 1)]
        print("visiting point %s" % random_feature.location)
        yield random_feature.location


def guide_record_route(stub: route_guide_pb2_grpc.RouteGuideStub) -> None:
    feature_list = read_route_guide_database()
    route_iterator = generate_route(feature_list)
    route_summary = stub.RecordRoute(route_iterator)
    print("Finished trip with %s points " % route_summary.point_count)
    print("Passed %s features " % route_summary.feature_count)
    print("Travelled %s meters " % route_summary.distance)
    print("It took %s seconds " % route_summary.elapsed_time)


def generate_messages() -> Iterator[route_guide_pb2.RouteNote]:
    messages = [
        make_route_note("First message", 0, 0),
        make_route_note("Second message", 0, 1),
        make_route_note("Third message", 1, 0),
        make_route_note("Fourth message", 0, 0),
        make_route_note("Fifth message", 1, 0),
    ]
    for msg in messages:
        print("Sending %s at %s" % (msg.message, msg.location))
        yield msg


def guide_route_chat(stub: route_guide_pb2_grpc.RouteGuideStub) -> None:
    responses = stub.RouteChat(generate_messages())
    for response in responses:
        print("Received message %s at %s" %
              (response.message, response.location))
