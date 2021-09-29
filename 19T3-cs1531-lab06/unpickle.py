import pickle

pickle_in = open("shapecolour.p", "rb")
data = [(pair['colour'], pair['shape']) for pair in pickle.load(pickle_in)]
common = max(set(data), key=data.count)
print(f"Colour: {common[0]}\nShape: {common[1]}")