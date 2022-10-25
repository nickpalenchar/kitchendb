

## Building the site

> NOTE: for now (because I am only one person), files in `content/recipes` will be committed to git. In the future, these will be ignored and automatically built from json files during via github actions, as described below:

There are additional steps before hugo.

**scripts/build_recipes** builds all content md files from data/recipes. Must run _before_ running a hugo server,
and especially before building.