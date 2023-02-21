import json
import os
from typing import Type, TypeVar
from enum import Enum
from logging import Logger

from exceptions import UnsupportedFormat

log = Logger("pyARB")

# Allowed types at the moment: String, int, double, num


class Placeholder:
    def __init__(self, name: str, format=None):
        self.name = name
        self.format = format

    def set(self, value: str):
        self.value = value
        return self

    def get(self):
        return self.value


class NumFormat(Enum):
    compact = "compact"
    compactCurrency = "compactCurrency"
    compactSimpleCurrency = "compactSimpleCurrency"
    # compactLong = "compactLong"
    currency = "currency"
    decimalPattern = "decimalPattern"
    decimalPercentPattern = "decimalPercentPattern"
    percentPattern = "percentPattern"
    scientificPattern = "scientificPattern"
    simpleCurrency = "simpleCurrency"


class NumType(Enum):
    num = "num"
    int = "int"
    double = "double"


class PlaceholderNum(Placeholder):
    def __init__(self, name: str, format: NumFormat = None, num_type: NumType = NumType.num, **kwargs):
        super().__init__(name, format=format)
        self.num_type = num_type
        self.optional_parameters = kwargs

    def _round_or_int(self, value: float, digits: int, recurse=True):
        if value == int(value):
            return int(value)
        if recurse:
            return self._round_or_int(round(value, digits), digits, recurse=False)
        return round(value, digits)

    def _compact(self, value, digits):
        units = ["", "k", "M", "B", "T"]
        u = 0
        while value >= 1000:
            u += 1
            value /= 1000
        return str(self._round_or_int(value, digits)) + units[u]

    def _readable_long(self, value, digits):
        return f"{value:,.{digits}f}"

    def set(self, value: float):
        self.value = value
        return self

    def get(self):
        value = self.value
        if self.format == NumFormat.compact:
            return self._compact(value, 1)
        elif self.format == NumFormat.compactCurrency:
            options = {"name": "USD", "decimalDigits": 2}
            options.update(self.optional_parameters)
            return options["name"] + self._compact(value, options["decimalDigits"])
        elif self.format == NumFormat.compactSimpleCurrency:
            options = {"symbol": "$", "decimalDigits": 2}
            options.update(self.optional_parameters)
            return options["symbol"] + self._compact(value, options["decimalDigits"])
        elif self.format == NumFormat.currency:
            options = {"name": "USD", "decimalDigits": 2}
            options.update(self.optional_parameters)
            return options["name"] + self._readable_long(value, options["decimalDigits"])
        elif self.format == NumFormat.decimalPattern:
            options = {"decimalDigits": 2}
            options.update(self.optional_parameters)
            return self._readable_long(value, options["decimalDigits"])
        elif self.format == NumFormat.decimalPercentPattern:
            options = {"decimalDigits": 2}
            options.update(self.optional_parameters)
            return self._readable_long(value * 100, options["decimalDigits"]) + "%"
        elif self.format == NumFormat.percentPattern:
            return self._readable_long(value * 100, 0) + "%"
        elif self.format == NumFormat.scientificPattern:
            return f"{value:.2e}"
        elif self.format == NumFormat.simpleCurrency:
            options = {"symbol": "$", "decimalDigits": 2}
            options.update(self.optional_parameters)
            return options["symbol"] + self._readable_long(value, options["decimalDigits"])
        return f"{value:,}"


T = TypeVar("T", Type[Enum])


def read_translations(arb_location: str, languages: T):
    translations: dict[T, dict[str, str]] = {}
    for lang in languages:
        arb_file = arb_location + "/" + lang.name + ".arb"
        if not os.path.exists(arb_file):
            log.warn(f"{lang.name}.arb not found in {arb_location}; using fallback lang")
        else:
            translations[lang] = {}
            with open(arb_file, "r") as f:
                arb: dict[str, str] = json.loads(f.read())
            for k, v in arb.items():
                if "@" not in k:
                    translations[lang][k] = v
    return translations


def translate(text: str, *placeholders: Placeholder):
    pass
