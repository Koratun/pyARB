import os
import shutil
import json
from tqdm import tqdm

from pyARB.localize import Placeholder, PlaceholderNum, NumFormat, NumType, snake_case
from pyARB.exceptions import UnsupportedFormat, DuplicateKey


def tab(n: int):
    return " " * n * 4


class ArbKey:
    def __init__(self, key: str, native_value: str):
        self.key = key
        self.snake_key = snake_case(key)
        self.native_value = native_value
        self.description: str = None
        self.placeholders: list[Placeholder] = None

    def method_signature(self, static=False):
        signature = tab(1)
        if static:
            signature += "@staticmethod\n" + tab(1)
        signature += "def " + self.snake_key
        if static:
            signature += "_static(lang: Lang"
        else:
            signature += "(self"
        if self.placeholders:
            signature += ", " + ", ".join(p.get_parameter() for p in self.placeholders)
        signature += "):\n"
        return signature

    def docstring(self):
        doc = tab(2) + f'"""\n{tab(2)}`{self.native_value}`\n'

        if self.description:
            doc += f"\n{tab(2)}Description: {self.description}\n"

        if self.placeholders:
            doc += f"\n{tab(2)}Placeholders:\n"
            for p in self.placeholders:
                doc += tab(3) + p.name + ": "
                if type(p) is Placeholder:
                    doc += "String\n"
                elif type(p) is PlaceholderNum:
                    if not p.format:
                        doc += p.get_type_string() + "\n"
                    else:
                        doc += "{\n" + tab(4) + "type: " + p.get_type_string() + "\n"
                        doc += tab(4) + "format: " + p.format.name + "\n"
                        if p.example:
                            doc += tab(4) + "example: " + p.example + "\n"
                        if p.description:
                            doc += tab(4) + "description: " + p.description + "\n"
                        if p.optional_parameters:
                            doc += tab(4) + "bakedParameters: {\n"
                            for k, v in p.optional_parameters.items():
                                doc += tab(5) + f"{k}: {v}\n"
                            doc += tab(4) + "}\n"
                        doc += tab(3) + "}\n"

        doc += tab(2) + '"""\n'
        return doc

    def method_return(self, static=False):
        ret = tab(2) + "return "
        if static:
            ret += "Translator._localize("
            if self.placeholders:
                ret += "\n" + tab(3) + "lang,\n" + tab(3) + f'"{self.key}",\n'
                for p in self.placeholders:
                    ret += tab(3) + p.get_code() + "\n"
                ret += tab(2) + ")\n"
            else:
                ret += f'lang, "{self.key}")\n'
        else:
            ret += f"self.{self.snake_key}_static(self.lang"
            if self.placeholders:
                ret += ", " + ", ".join(p.name for p in self.placeholders)
            ret += ")\n"
        return ret

    def print_methods(self):
        methods = "\n" + self.method_signature() + self.docstring() + self.method_return()
        methods += "\n" + self.method_signature(static=True) + self.docstring() + self.method_return(static=True)
        return methods

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
    arb_location = arb_location.replace("\\", "/")
    if arb_location.endswith("/"):
        arb_location = arb_location[:-1]

    if not os.path.exists(arb_location):
        raise FileNotFoundError(arb_location + " does not exist")

    if not target_directory:
        target_directory = os.path.dirname(arb_location)
    elif not os.path.exists(target_directory):
        target_directory = target_directory.replace("\\", "/")
        if target_directory.endswith("/"):
            target_directory = target_directory[:-1]
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
            if k in keys:
                raise DuplicateKey(f"Key {k} found twice in {primary_arb}")
            keys[k] = ArbKey(k, v)
        elif k[1:] in keys:
            keys[k[1:]].process_metadata(v)
        else:
            raise UnsupportedFormat(f"Expected to find `@{k}` after original `{k}`")

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
        print("Generating localizations...")
        for v in tqdm(keys.values(), ncols=50):
            f.write(v.print_methods())

    # Check if other locales have arb files, if so, leave them, if not, create them.
    for l in locales[1:]:
        if not os.path.exists(new_arb := os.path.join(arb_location, l + ".arb")):
            shutil.copy(primary_arb, new_arb)
