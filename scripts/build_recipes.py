import os
import subprocess

def build():
  """
  build takes all json files in data/recipes and builds them into content pages.

  JSON files must all be UpperCammelCase
  """
  clean()

  for file in os.listdir('data/recipes'):
    validate_file_name(file)
    mkdown_name = camel_to_snake_case(file).replace(".json", ".md")

    print(f"building {mkdown_name}...")
    subprocess.run(["hugo", "new", "--kind", "recipes", f"content/recipes/{mkdown_name}"])

def clean():
  for file in os.listdir("content/recipes"):
    os.remove(f"content/recipes/{file}")

def validate_file_name(name):
  if name[0].islower():
    raise Exception("Name must begin with upper case letter")
  if not name.endswith('.json'):
    raise Exception("name must be .json extension")
  return name

def camel_to_snake_case(name):
  return ''.join([name[0].lower()] + [c if c.islower() or c == "." else f'-{c.lower()}' for c in name[1:]])

if __name__ == '__main__':
  build()