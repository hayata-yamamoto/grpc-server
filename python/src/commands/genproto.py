from pathlib import Path
from grpc_tools import protoc


def main() -> None: 
    p = Path(__file__).resolve()
    protoc((
        "", 
        f"-I={str(p.parents[3] / 'proto')}",
        f"--python_out={str(p.parents[1] / 'proto')}",
        f"--grpc_out={str(p.parents[1] / 'proto')}",
        "route_guide.proto"
    ))