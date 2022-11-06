---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }} #$DATE$
draft: true
categories: [] #$CATEGORIES$
---

{{< recipe-summary url="data/recipes/{{ .Name }}.json">}}
<!--more-->
{{< recipe-list url="data/recipes/{{ .Name }}.json">}}
