#!/usr/bin/env python3
"""Load a CARLA map and report what was loaded.

Examples
--------
    python3 load_town04.py                    # load Town04
    python3 load_town04.py --map Town05
    python3 load_town04.py --host 192.168.1.10

Requires a running CARLA server and the matching client library::

    pip3 install carla==0.9.16
"""

import argparse
import sys

try:
    import carla
except ImportError:
    sys.exit("The 'carla' package is not installed. Run: pip3 install carla==0.9.16")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--host", default="localhost",
                        help="CARLA server host (default: localhost)")
    parser.add_argument("--port", type=int, default=2000,
                        help="CARLA RPC port (default: 2000)")
    parser.add_argument("--map", default="Town04",
                        help="map to load (default: Town04)")
    parser.add_argument("--timeout", type=float, default=60.0,
                        help="seconds to wait for the server (default: 60)")
    args = parser.parse_args()

    client = carla.Client(args.host, args.port)
    client.set_timeout(args.timeout)

    # Ask the server what it has before trying to load anything. This turns a
    # confusing 60-second timeout into an immediate, specific error.
    try:
        available = [m.split("/")[-1] for m in client.get_available_maps()]
    except RuntimeError:
        print(f"No CARLA server answered at {args.host}:{args.port}.", file=sys.stderr)
        print("Start it with:   docker start carla-server", file=sys.stderr)
        print("Check it is up:  docker ps --filter name=carla-server", file=sys.stderr)
        return 1

    if args.map not in available:
        print(f"'{args.map}' is not available on this server.", file=sys.stderr)
        print("Available maps: " + ", ".join(sorted(available)), file=sys.stderr)
        return 1

    print(f"Loading {args.map}. This can take up to a minute.")
    world = client.load_world(args.map)

    carla_map = world.get_map()
    print(f"Map:          {carla_map.name}")
    print(f"Spawn points: {len(carla_map.get_spawn_points())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
