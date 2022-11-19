
import re
import typing as t
from recibundler.reciparcer.constants import FRAC_CHARS_TO_DEC


def _format_amount_item(m: str) -> str:
    m = re.sub("\s+", " ", m.strip())
    leading = "0"

    if " " in m:
        leading, m = m.split(" ")

    if m in FRAC_CHARS_TO_DEC.keys():
        return leading + str(FRAC_CHARS_TO_DEC[m])

    try:
        float(m)
        return str(int(leading) + round(float(m), 2))
    except ValueError:
        if "/" in m:
            num, den = m.split("/")
            return leading + str(round(int(num) / int(den), 2))
        raise Exception("could not parse amount")

def _format_amount(m: t.Union[str, t.List[str]]) -> t.List[str]:
    """
    attempts to parse the measurement for the `amount` into its decimal form
    """
    return [_format_amount_item(el) for el in m]
