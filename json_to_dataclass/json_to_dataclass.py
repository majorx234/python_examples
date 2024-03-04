from dataclasses import dataclass
import dataclasses
import numpy as np
import codecs, json

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@dataclass
class Position:
    """Class for keeping pos and heading"""
    pos: np.ndarray
    heading: np.ndarray

    def from_json(json_string) -> "Position":
        json_obj = json.loads(json_string)
        return Position(np.array(json_obj["pos"]),
                        np.array(json_obj["heading"]))

    def to_json(self):
        return json.dumps(dataclasses.asdict(self), cls=NumpyEncoder)


def main():
    # json_file_name = sys.argv[1]
    mypos = Position(np.array([1, 2, 3]),np.array([0,0,0,1]))
    json_string = mypos.to_json()
    print(json_string)
    mypos_new = Position.from_json(json_string)
    print(mypos_new.__dict__)
    json_string_new = mypos_new.to_json()
    print(json_string_new)

if __name__ == '__main__':
    main()
