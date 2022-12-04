# Adding a new recipe

Make sure you have a csv file from the form saved.

1. in scripts, activate the virtual env

```
cd scripts && python -m pipenv shell
```

2. Build the recipe from csv to json 

```
python add_new_recipes.py
```

3. Rebuild site from recipes (to include new one)

```shell
cd .. && hugo -D
# or
cd .. && hugo server -D # (live preview)
```

4. Commit new recipe and save point
```shell
git add data/recipes # one new file should be created
git add add_new_recipes_since
```
