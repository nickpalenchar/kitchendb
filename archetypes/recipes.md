---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
---

{{< recipe-list url="data/recipes/{{ .Name }}.json">}}
