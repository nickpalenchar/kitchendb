---
title: '{{ replace .Name "-" " " | title }}' #$TITLE$
date: {{ .Date }} #$DATE$
categories: [] #$CATEGORIES$
summary: " " #$SUMMARY$
#$AUTHOR$
prepTime: 0
cookTime: 0
difficulty: 0
featured_image: ""
description: How to make {{ replace .Name "-" " " | title }} from the free online cookbook
diets: []
cuisines: []
---
{{< recipe-data url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
{{< recipe-summary url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
{{< recipe-list url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
