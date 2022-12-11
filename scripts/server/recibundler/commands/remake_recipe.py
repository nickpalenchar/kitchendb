import json
import csv
import sys
from recibundler.schema.reciperow import reciperow
from recibundler import json_writing


def remake_recipe(recipejson, csvfile):
    with open(recipejson, "r") as fh:
        rdata = json.loads(fh.read())
        if "timestamp" not in rdata:
            print(f"Error, json data has no timestamp")
            sys.exit()

    with open(csvfile, "r") as fh:
        reader = csv.reader(fh)
        next(reader)

        for line in reader:
            recipe = reciperow(*line)

            if recipe.timestamp == rdata["timestamp"]:
                print("found it", recipe)
                # TODO re-add categories
                additional_keys = (
                    {"categories": rdata["categories"]}
                    if "categories" in rdata
                    else None
                )
                json_writing.write_recipe_to_json(
                    recipe, additional_keys=additional_keys
                )
