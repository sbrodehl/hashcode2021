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
        "i": i,
        "s": s,
        "v": v,
        "f": f,
        "cars": {c.id: c.__dict__ for c in cars},
        "streets": {v.id: v.__dict__ for k, v in streets.items()},
        "intersections": {i.id: i.__dict__ for i in intersections},
    }
    del streets, intersections, cars, d, i, s, v, f
    # delete not needed members
    for s in data["streets"]:
        del data["streets"][s]["id"]
        del data["streets"][s]["visits"]
        del data["streets"][s]["starting_cars"]
        data["streets"][s]["b"] = data["streets"][s]["begin_intersection"]
        data["streets"][s]["e"] = data["streets"][s]["end_intersection"]
        data["streets"][s]["t"] = data["streets"][s]["travel_time"]
        data["streets"][s]["n"] = data["streets"][s]["name"]
        del data["streets"][s]["begin_intersection"]
        del data["streets"][s]["end_intersection"]
        del data["streets"][s]["travel_time"]
        del data["streets"][s]["name"]
    for i in data["intersections"]:
        del data["intersections"][i]["id"]
        del data["intersections"][i]["has_schedule"]
        data["intersections"][i]["in"] = [_street_names[s] for s in data["intersections"][i]["incoming"]]
        data["intersections"][i]["out"] = [_street_names[s] for s in data["intersections"][i]["outgoing"]]
        del data["intersections"][i]["incoming"]
        del data["intersections"][i]["outgoing"]
    for c in data["cars"]:
        del data["cars"][c]["id"]
        data["cars"][c]["s"] = [_street_names[s] for s in data["cars"][c]["streets"]]
        del data["cars"][c]["streets"]
    with open(out_fp, "w") as fp:
        json.dump(data, fp, separators=(',', ':'))
