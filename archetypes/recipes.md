---
title: '{{ replace .Name "-" " " | title }}' #$TITLE$
date: {{ .Date }} #$DATE$
draft: true
categories: [] #$CATEGORIES$
summary: "" #$SUMMARY$
#$AUTHOR$
---

{{< recipe-summary url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
{{< recipe-list url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
