import time
import math
import logging
from typing import List, Optional, Iterator, Any

import grpc

from src.proto.route_guide_pb2 import Feature, Point, Rectangle, RouteSummary, RouteNote
from src.proto import route_guide_pb2_grpc
from src import resources


def get_feature(feature_db: List[Feature], point: Point) -> Optional[Feature]:
    for feature in feature_db:
        if feature.location == point:
            return feature
    return None


def get_distance(start: Point, end: Point) -> float:
    coord_factor = 10000000.0
    lat_1 = start.latitude / coord_factor
    lat_2 = end.latitude / coord_factor
    lon_1 = start.longitude / coord_factor
    lon_2 = end.longitude / coord_factor
    lat_rad_1 = math.radians(lat_1)
    lat_rad_2 = math.radians(lat_2)
    delta_lat_rad = math.radians(lat_2 - lat_1)
    delta_lon_rad = math.radians(lon_2 - lon_1)

    a = (pow(math.sin(delta_lat_rad / 2), 2) +
         (math.cos(lat_rad_1) * math.cos(lat_rad_2) *
          pow(math.sin(delta_lon_rad / 2), 2)))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000
    return R * c


class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    def __init__(self) -> None:
        self.db = resources.read_route_guide_database()

    def GetFeature(self, request: Feature, context: Any) -> Feature:
        feature = get_feature(self.db, request)
        if feature is None:
            return Feature(name="", location=request)
        else:
            return feature

    def ListFeatures(self, request: Rectangle,
                     context: Any) -> Iterator[Feature]:
        left = min(request.lo.longitude, request.hi.longitude)
        right = max(request.lo.longitude, request.hi.longitude)
        top = max(request.lo.latitude, request.hi.latitude)
        bottom = min(request.lo.latitude, request.hi.latitude)

        for feature in self.db:
            if (feature.location.longitude >= left
                    and feature.location.longitude <= right
                    and feature.location.latitude >= bottom
                    and feature.location.latitude <= top):
                yield feature

    def RecordRoute(self, request_iterator: Iterator[Point],
                    context: Any) -> RouteSummary:
        point_count = 0
        feature_count = 0
        distance = 0.0
        prev_point = None

        start_time = time.time()
        for point in request_iterator:
            point_count += 1
            if get_feature(self.db, point):
                feature_count += 1
            if prev_point:
                distance += get_distance(prev_point, point)

            prev_point = point

        elapsed_time = time.time() - start_time
        return RouteSummary(point_count=point_count,
                            feature_count=feature_count,
                            distance=int(distance),
                            elapsed_time=int(elapsed_time))

    def RouteChat(self, request_iterator: Iterator[RouteNote],
                  context: Any) -> Iterator[RouteNote]:
        prev_notes: List[RouteNote] = []
        for new_note in request_iterator:
            for prev_note in prev_notes:
                if prev_note.location == new_note.location:
                    yield prev_note
            prev_notes.append(new_note)
