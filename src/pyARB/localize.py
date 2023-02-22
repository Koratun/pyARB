import json
import os
from typing import Type
from enum import Enum
from logging import Logger
import re

from .exceptions import InvalidFormat

log = Logger("pyARB")

# Allowed types at the moment: String, int, double, num


class Placeholder:
    def __init__(self, name: str):
        self.name = name
        self.example = None
        self.description = None

    def get_docstring(self) -> str:
        return " " * 12 + self.name + ": String\n"

    def get_code(self) -> str:
        return " " * 12 + f'Placeholder("{self.name}").set({self.name}),\n'

    def set(self, value: str):
        self.value = value
        return self

    def get(self) -> str:
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
        super().__init__(name)
        self.format = format
        self.num_type = num_type
        self.optional_parameters = kwargs

    def get_docstring(self) -> str:
        if not self.format:
            return " " * 12 + self.name + f": {self.num_type.name}\n"
        doc = " " * 12 + self.name + ": {\n"
        doc += " " * 16 + f"type: {self.num_type.name}\n"
        doc += " " * 16 + f"format: {self.format.name}\n"
        if self.example:
            doc += " " * 16 + f"example: {self.example}\n"
        if self.description:
            doc += " " * 16 + f"description: {self.description}\n"
        if self.optional_parameters:
            doc += " " * 16 + "optionalParameters: {\n"
            for k, v in self.optional_parameters.items():
                doc += " " * 20 + f"{k}: {v}\n"
            doc += " " * 16 + "}\n"
        return doc + " " * 12 + "}\n"

    def get_code(self) -> str:
        args = [f'"{self.name}"']
        if self.format:
            args.append(f"format=NumFormat.{self.format.name}")
        if self.num_type != NumType.num:
            args.append(f"num_type=NumType.{self.num_type.name}")
        if self.optional_parameters:
            args.extend(
                k + "=" + (f'"{v}"' if isinstance(v, str) else str(v)) for k, v in self.optional_parameters.items()
            )
        return " " * 12 + f'Placeholder({", ".join(_ for _ in args)}).set({self.name}),\n'

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
        double_check = self._round_or_int(value, digits)
        if double_check >= 1000:
            u += 1
            double_check /= 1000
        return str(self._round_or_int(double_check, digits)) + units[u]

    def _readable_long(self, value, digits):
        return f"{value:,.{digits}f}"

    def set(self, value: float):
        self.value = value
        return self

    def get(self) -> str:
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


def read_translations(arb_location: str, languages: Type[Enum]):
    translations: dict[Type[Enum], dict[str, str]] = {}
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
                    # purify whitespace
                    purified = ""
                    layer = 0
                    for c in v:
                        if layer % 2 == 1 and c in {" ", "\n", "\t"}:
                            continue
                        if c == "{":
                            layer += 1
                        elif c == "}":
                            layer -= 1
                        if layer < 0:
                            raise InvalidFormat(f"`{lang} -> {k} -> {v}` has invalid brackets")
                        purified += c
                    if layer != 0:
                        raise InvalidFormat(f"`{lang} -> {k} -> {v}` has invalid brackets")
                    translations[lang][k] = purified
    return translations


def _split_select_cases(selectable: str):
    """
    Could be passed a string with content beyond the end of the select cases
    such as `male{He}female{She}other{They}} went to {storeName}.`

    Will return: {
        male: "He"
        female: "She"
        other: "They"
    }

    It is an error to not specify the `other` case in any select.
    """
    brackets = 1
    end = 0
    cases = {}
    buffer = ""
    key = ""
    # Check if there is an offset for plurals
    offset = 0
    if m := re.match(r"^offset:([-\d]\d*)", selectable):
        offset = int(m.groups()[0])
        end = len(m.group())

    while brackets > 0:
        if selectable[end] == "{":
            brackets += 1
            if brackets == 2:
                key = buffer
                buffer = ""
            else:
                buffer += "{"
        elif selectable[end] == "}":
            brackets -= 1
            if brackets == 1:
                cases[key] = buffer
                buffer = ""
            else:
                buffer += "}"
        else:
            buffer += selectable[end]
        end += 1
    return cases, end, offset


def inject_placeholders(text: str, *placeholders: Placeholder, num_shorthand: PlaceholderNum = None):
    if num_shorthand:
        text = re.sub(r"(?<!\\)(#)", num_shorthand.get(), text)
        text = text.replace("\\#", "#")
    for var in placeholders:
        if "{" + var.name + "}" in text:
            text = text.replace("{" + var.name + "}", var.get())
        # Check for Selects or Plurals
        elif (l := text.find("{" + var.name)) >= 0:
            l += len(var.name) + 2
            select_type = text[l : (case_start := text.find(",", l))]
            if select_type == "select":
                cases, select_end, offset = _split_select_cases(text[case_start + 1 :])
                if offset != 0:
                    raise InvalidFormat(f"Only a plural may specify an offset. Offset found in `{text}`.")
                if var.value not in cases:
                    log.warn(f"Select in `{text}` does not have a case for `{var.value}`; using `other`")
                    inner = inject_placeholders(cases["other"], *placeholders)
                else:
                    inner = inject_placeholders(cases[var.value], *placeholders)
            elif select_type == "plural":
                cases, select_end, offset = _split_select_cases(text[case_start + 1 :])
                exact = f"={var.value}"
                if exact in cases:
                    inner = inject_placeholders(cases[exact], *placeholders, num_shorthand=var)
                else:
                    val = abs(var.value - offset)
                    if val == 0:
                        offseted = "zero"
                    elif val == 1:
                        offseted = "one"
                    elif val == 2:
                        offseted = "two"
                    elif val < 20:
                        offseted = "few"
                    else:
                        offseted = "many"
                    if offseted not in cases:
                        # log.warn(f"Plural in `{text}` does not have a case for `{var.value}`; using `other`")
                        inner = inject_placeholders(cases["other"], *placeholders, num_shorthand=var.set(val))
                    else:
                        inner = inject_placeholders(cases[offseted], *placeholders, num_shorthand=var.set(val))
            else:
                raise InvalidFormat(f"Expected select or plural but got `{select_type}` in `{text}`")
            text = text[: l - (len(var.name) + 2)] + inner + text[case_start + 1 + select_end :]
    return text
