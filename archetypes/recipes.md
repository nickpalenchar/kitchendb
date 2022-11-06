---
title: '{{ replace .Name "-" " " | title }}'
date: {{ .Date }} #$DATE$
draft: true
categories: [] #$CATEGORIES$
---

{{< recipe-summary url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
<!--more-->
{{< recipe-list url="data/recipes/{{ replace .Name "\"" "\\\"" }}.json">}}
