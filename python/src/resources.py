import json
from typing import List, Any
from pathlib import Path

from src.proto.route_guide_pb2 import Feature, Point


def read_route_guide_database() -> List[Feature]:
    feature_list = []
    with (Path(__file__).parent / 'db.json').open() as f:
        for item in json.load(f):
            feature = Feature(name=item['name'],
                              location=Point(
                                  latitude=item['location']['latitude'],
                                  longitude=item['location']['longitude']))
            feature_list.append(feature)
    return feature_list
