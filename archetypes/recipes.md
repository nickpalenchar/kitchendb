---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
---

HELLO?
{{< recipe-list url="data/recipes/{{ replace (replace .Name "-" " " | title) " " "" }}.json">}}
