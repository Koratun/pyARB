# Changelog

## Version 1.2.0 - March 14, 2023

### Features

- Allow Translator class to be instantiated and its static methods to called with the string equivalents of the `Lang` enum containing the accepted localizations. For example:

```python
# Previously only this was allowed
t = Translator(Lang.en_US)
Translator.many_items_static(Lang.en_US, "Bob", 4)

# Now accepts either the below or the above
t = Translator("en_US")
Translator.many_items_static("en_US", "Bob", 4)
```

## Version 1.1.1 - March 8, 2023

### Bug Fixes

- Loading translation files now uses UTF-8 encoding to allow for characters outside the English alphabet.

## Version 1.1.0 - February 27, 2023

### Features

- Added ability to override the optional parameters of the placeholders from python. Allowing for some dynamic formatting if desired.

### Bug Fixes

- Fixed some edge cases with converting camelCase to snake_case.
- Parameter names in localization methods are now converted to snake_case instead of staying in camelCase.

## Version 1.0.5 - February 23, 2023

### Requirement Fix

- Found that pyARB does not function before python 3.8.

## Version 1.0.3 & 1.0.4 - February 23, 2023

### Documentation

- Clarified the readme and removed a debug statement in the release.

## Version 1.0.2 - February 23, 2023

### Features

- Added the ability to use existing `.arb` files as the list of allowed locales.

## Version 1.0.1 - February 23, 2023

### Bug Fix

- Fixed a critical import error that did not allow the library to run on any system other than mine.

## Version 1.0.0 - February 23, 2023

### Features

- All of them! First release!
