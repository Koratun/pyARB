# pyARB

![PyPI](https://img.shields.io/pypi/v/pyARB)
![PyPI - License](https://img.shields.io/pypi/l/pyARB)

A localization library for python utilizing the ARB format for Flutter.

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

`pyarb l10ns path/to/directory` will prompt the user for a list of locales. The first in the list will be considered the primary locale and will be set as the fallback locale in case there is a problem localizing for another locale. The primary `.arb` file must be present, but if other locales specified are missing it will create the missing `.arb` file with the contents of the primary file. If a locale is already present then it will be left as it to preserve translations already present in the file.

`pyarb l10ns path/to/directory -e en_US` will use the existing arb files as the list of allowed locales. It will use the specified locale as the primary locale, in this case: 'en_US'.
