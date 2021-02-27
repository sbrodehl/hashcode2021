import json
from pathlib import Path

from .parsing import parse_input


def convert(in_fp: str, out_fp: str):
    in_fp = Path(in_fp).resolve().absolute()
    out_fp = Path(out_fp).resolve().absolute()
    if out_fp.is_dir():
        out_fp = out_fp / in_fp.name.replace("".join(in_fp.suffixes), ".json")
    (d, i, s, v, f), streets, cars, intersections = parse_input(str(in_fp))

    _street_names = {v.name: v.id for k, v in streets.items()}
    data = {
        "d": d,
        "f": f,
        "v": [c.__dict__ for c in cars],
        "s": [v.__dict__ for k, v in streets.items()],
        "i": [i.__dict__ for i in intersections],
    }
    del streets, intersections, cars, d, i, s, v, f
    # delete not needed members
    for s in data["s"]:
        s["source"] = s["begin_intersection"]
        s["target"] = s["end_intersection"]
        s["t"] = s["travel_time"]
        s["n"] = s["name"]
        del s["visits"]
        del s["starting_cars"]
        del s["begin_intersection"]
        del s["end_intersection"]
        del s["travel_time"]
        del s["name"]
    for i in data["i"]:
        i["in"] = [_street_names[s] for s in i["incoming"]]
        i["out"] = [_street_names[s] for s in i["outgoing"]]
        i["w"] = len(i["in"]) + len(i["out"])
        del i["incoming"]
        del i["outgoing"]
        del i["has_schedule"]
    for c in data["v"]:
        c["s"] = [_street_names[s] for s in c["streets"]]
        del c["streets"]
    with open(out_fp, "w") as fp:
        json.dump(data, fp, separators=(',', ':'))
