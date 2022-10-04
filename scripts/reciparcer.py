import re

def parse_ingredients(s: str):
  for line in s.split('\n'):
    print(f'line: {line}')

def _parse_ingredient(m: str):
  """
  attempts to parse the measurement into its decimal form
  """

def _parse_measurement(m: str):
  """
  attempts to parse the measurement into its decimal form
  """
  m = re.sub('\s+', ' ', m.strip())

  special_chars = {
    '⅘': 0.8,
    '½': 0.5,
    '⅔': 0.67,
    '¾': 0.75,
    '⅝', 0.62,
    '⅗': 0.6,
    '⅜': 0.375,
    '⅖': 0.4,
    '⅕': 0.20
    '⅐': 0.14,
    '⅑': 0.11,
    '⅒': 0.10,
  }
  leading = '0'

  if ' ' in m:
    leading, m = m.split(' ')

  if m in special_chars.keys():
    return leading + special_chars[m]
  
  try:
    float(m)
    return int(leading) + round(float(m), 2)
  except ValueError:
    if '/' in m:
      num, den = m.split('/')
      return int(leading) + round(int / den, 2)

