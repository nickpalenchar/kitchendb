import sys
from .commands.add_recipe_from_form import add_new_recipes

help = """
Commands available:

next-recipe <csv-file> - parses one recipe from a csv file
build-content - builds the content from the output data jsons.
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
      print(help)
      sys.exit()
    
    cmd = sys.argv[1]

    if cmd == 'next-recipe':
      add_new_recipes(*sys.argv[2:])
    elif cmd == 'build-content':
      pass
    else:
      print(help)
      sys.exit()