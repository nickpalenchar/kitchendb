---
title: '{{ replace .Name "-" " " | title }}' #$TITLE$
date: {{ .Date }} #$DATE$
draft: true
categories: [] #$CATEGORIES$
summary: " " #$SUMMARY$
#$AUTHOR$
---

{{< recipe-summary url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
<!--more-->
{{< recipe-list url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
