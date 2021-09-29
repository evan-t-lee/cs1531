import sys, json, yaml

if sys.argv[1] == "data_1":
    with open("data_1.json", "r") as json_file, open("data_1.yml", "w") as out:
            yaml.safe_dump(json.load(json_file), out, default_flow_style=False)
elif sys.argv[1] == "data_2":
    with open("data_2.yml", "r") as yaml_file, open("data_2.json", "w") as out:
            json.dump(yaml.safe_load(yaml_file), out, indent=2)