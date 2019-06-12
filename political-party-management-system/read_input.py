import json

def json_readr(file):
    for line in open(file, mode="r"):
         yield json.loads(line)

def read_input(file):
	lst = list(json_readr(file))
	return lst
