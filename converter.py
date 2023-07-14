import pretty_midi
import pandas as pd

import argparse
import os

parser = argparse.ArgumentParser(description="Convert MIDI to JSON/JSON_FOR_XML")
parser.add_argument("input", help="Input MIDI file")
parser.add_argument("-r", "--resolution", help="Resolution of the output JSON in milliseconds", default=100, type=int) 

args = parser.parse_args()
resolution = args.resolution

filepath = args.input
filename = os.path.basename(filepath).split(".")[0]

midi_data = pretty_midi.PrettyMIDI(filepath)

full_data = pd.DataFrame()

for instrument in midi_data.instruments:
    control_change_events = instrument.control_changes

    data = {"time": [], instrument.name: []}

    for control_change in control_change_events:
        if control_change.number == 4:
            data["time"].append(control_change.time)
            data[instrument.name].append(control_change.value)

    df = pd.DataFrame(data)

    df["time"] = pd.to_datetime(df["time"], unit="s")
    df = df.set_index("time")
    df = df.groupby("time").agg({instrument.name: "first"})
    df = df.resample(str(resolution) + "L").ffill()

    if full_data.empty:
        full_data = df
    else:
        full_data = pd.concat([full_data, df], axis=1)

full_data.to_csv("output/" + filename + ".csv")

import json

json_data = {"name": "Notification-1", "patterns": []}

for column in full_data.columns:
    if column == "time":
        continue
    json_data["patterns"].append([])

for column in full_data.columns:
    if column == "time":
        continue
    for index, row in full_data.iterrows():
        column_index = int(column.split(" ")[1]) - 1

        remapped_value = (row[column] / 127) * 100
        pattern = {
            "functionType": "Still",
            "duration": resolution,
            "initVal": remapped_value,
            "finalVal": remapped_value,
            "curve": "Linear",
            "step": 1,
        }

        json_data["patterns"][column_index].append(pattern)


with open("output/" + filename + ".json", "w") as outfile:
    json.dump(json_data, outfile)


with open("output/" + filename + ".txt", "w") as outfile:
    json_string = json.dumps(json_data)
    json_string = json_string.replace('"', "&quot;")
    json_string = json_string.replace(" ", "")

    outfile.write(json_string)