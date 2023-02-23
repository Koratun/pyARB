# pyARB

[![PyPI](https://img.shields.io/pypi/v/pyARB)](https://pypi.org/project/pyARB/)
![PyPI - License](https://img.shields.io/pypi/l/pyARB)

A localization library for python utilizing the ARB format for Flutter.

[Changelog](./CHANGELOG.md)

## Usage

pyARB takes a primary .arb file and generates a python code equivalent.

```txt
pyarb l10ns [-h] [-e USE_EXISTING] arb_location [target_directory]

positional arguments:
  arb_location          The directory containing the arb files.
  target_directory      Location of the generated py file. Defaults to the directory above arb_location.

optional arguments:
  -h, --help            show this help message and exit
  -e USE_EXISTING, --use-existing USE_EXISTING
                        Use existing arb files as locale list. You must specify the primary arb here
```

`pyarb l10ns path/to/directory` will prompt the user for a list of locales. The first in the list will be considered the primary locale and it will also be set as the fallback in case there is a problem with another locale. The primary `.arb` file must be present. If other locales are missing it will create the missing `.arb` file with the contents of the primary file. If a locale is already present then it will be left as it is to preserve translations already present in that file.

`pyarb l10ns path/to/directory -e en_US` will use the existing arb files as the list of allowed locales. It will use the specified locale as the primary locale, in this case: 'en_US'.

## Example

Both of the above examples will create the `generated_components.py` file at `path/to` which you can then use in your code.

```python
from path.to.generated_components import Translator, Lang

t = Translator(Lang.en_US)
print(t.followers_count(999950))
print(t.many_items("Bob", 10))

# Also supports static references
print(Translator.followers_count_static(Lang.es_ES, 6851651))
print(Translator.many_items_static(Lang.es_ES, "Juan", 3))
```

Docstrings are also provided to show what variables are needed for the translation key so your IDE can show you exactly what each localization is, what it needs, and what it will do.

## Does not yet support

- DateTime and Object types in the .arb specification.
- The `compactLong` format for number types.
