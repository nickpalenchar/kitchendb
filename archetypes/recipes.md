---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
---

{{< recipe-list url="data/recipes/{{ replace (replace .Name "-" " " | title) " " "" }}.json">}}
