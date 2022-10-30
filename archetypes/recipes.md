---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
---

{{< recipe-summary url="data/recipes/{{ .Name }}.json">}}
<!--more-->
{{< recipe-list url="data/recipes/{{ .Name }}.json">}}
