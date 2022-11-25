---
title: '{{ replace .Name "-" " " | title }}' #$TITLE$
date: {{ .Date }} #$DATE$
draft: true
categories: [] #$CATEGORIES$
summary: " " #$SUMMARY$
#$AUTHOR$
prepTime: 0
cookTime: 0
difficulty: 0
---
{{< recipe-data url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
{{< recipe-summary url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
{{< recipe-list url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
