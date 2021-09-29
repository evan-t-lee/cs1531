import pickle, json

pickle_in = open("shapecolour.p", "rb")
raw_data = pickle.load(pickle_in)
colour_data = [pair['colour'] for pair in raw_data]
shape_data =[pair['shape'] for pair in raw_data]

info = {
    "mostCommon" : {
        "colour" : max(set(colour_data), key=colour_data.count),
        "shape" : max(set(shape_data), key=shape_data.count)
    },
    "rawData" : raw_data
}

with open("processed.json", "w") as out:
    json.dump(info, out)