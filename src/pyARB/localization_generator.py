import os
import json

from .localize import Placeholder, PlaceholderNum, NumFormat, NumType
from .exceptions import UnsupportedFormat


class ArbKey:
    def __init__(self, key: str, native_value: str):
        self.key = key
        self.native_value = native_value

    def process_metadata(self, data: dict):
        if "description" in data:
            self.description = data["description"]
        if "placeholders" in data:
            self.placeholders = []
            for k, v in data["placeholders"].items():
                if (t := v.get("type")) == "String" or not t:
                    self.placeholders.append(Placeholder(k))
                elif t in {"int", "double", "num"}:
                    p = PlaceholderNum(
                        k,
                        format=NumFormat(v["format"]) if v.get("format") else None,
                        num_type=NumType(t),
                        **(v.get("optionalParameters") or {}),
                    )
                    if extra := v.get("example"):
                        p.example = extra
                    if extra := v.get("description"):
                        p.description = extra
                    self.placeholders.append(p)
                else:
                    raise UnsupportedFormat(t + " is not yet a supported type")


def generate_localizations(arb_location: str, locales: list[str], target_directory: str = None):
    if not os.path.exists(arb_location):
        raise FileNotFoundError(arb_location + " does not exist")

    if not target_directory:
        target_directory = os.path.dirname(arb_location)
    elif not os.path.exists(target_directory):
        raise FileNotFoundError(target_directory + " does not exist")

    primary_arb = os.path.join(arb_location, locales[0] + ".arb")
    if not os.path.exists(primary_arb):
        raise FileNotFoundError(primary_arb + " does not exist")

    with open(primary_arb, "r") as f:
        arb: dict = json.loads(f.read())

    keys: dict[str, ArbKey] = {}
    for k, v in arb.items():
        if k == "@@locale":
            continue
        if "@" not in k:
            keys[k] = ArbKey(k, v)
        elif k[1:] in keys:
            keys[k[1:]].process_metadata(v)
        else:
            raise UnsupportedFormat(f"Expected to find `@{k}` after original `{k}`")

    def tab(n: int):
        return " " * n * 4

    with open(os.path.join(target_directory, "generated_components.py"), "w") as f:
        f.write("from enum import Enum\n")
        f.write(
            "from pyARB.localize import log, read_translations, inject_placeholders, Placeholder, PlaceholderNum, NumFormat, NumType\n\n\n"
        )

        f.write("class Lang(Enum):\n")
        for l in locales:
            f.write(tab(1) + f'{l} = "{l}"\n')

        f.write(f'\n\nTRANSLATIONS = read_translations("{arb_location}", Lang)\n')
        f.write(f"FALLBACK_LANG = Lang.{locales[0]}\n\n")

        f.write(
            """
class Translator:
    def __init__(self, lang: Lang):
        self.lang = lang

    @staticmethod
    def _key_check(lang: Lang, key: str):
        if lang in TRANSLATIONS:
            if key in TRANSLATIONS[lang]:
                return True
            log.error(f"{lang.name}.arb does not have key `{key}`")
        return False

    @staticmethod
    def _localize(lang: Lang, key: str, *placeholders: Placeholder):
        if Translator._key_check(lang, key):
            return inject_placeholders(TRANSLATIONS[lang][key], *placeholders)
        if Translator._key_check(FALLBACK_LANG, key):
            return inject_placeholders(TRANSLATIONS[FALLBACK_LANG][key], *placeholders)
        log.error(f"Key `{key}` not found in requested or fallback langs!!!")
        return key
"""
        )

        # Loop through keys to create instance and static methods
