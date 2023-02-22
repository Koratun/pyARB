from enum import Enum
from pyARB.localize import log, read_translations, inject_placeholders, Placeholder, PlaceholderNum, NumFormat, NumType


class Lang(Enum):
    en = "en"
    es = "es"


TRANSLATIONS = read_translations("src/pyARB/localization/arbs", Lang)
FALLBACK_LANG = Lang.en


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
        log.error(f"key `{key}` not found in requested or fallback langs!!!")
        return key

    def no(self):
        """
        `No`
        """
        return self.no_(self.lang)

    @staticmethod
    def no_(lang: Lang):
        """
        `No`
        """
        return Translator._localize(lang, "no")

    def investment_created_at(self, date: str, time: str):
        """
        `Opened: {date} at {time}`

        Description: Displays a position's creation date

        Placeholders:
            date: String
            time: String
        """
        return self.investment_created_at_(self.lang, date, time)

    @staticmethod
    def investment_created_at_(lang: Lang, date: str, time: str):
        """
        `Opened: {date} at {time}`

        Description: Displays a position's creation date

        Placeholders:
            date: String
            time: String
        """
        return Translator._localize(
            lang,
            "investmentCreatedAt",
            Placeholder("date").set(date),
            Placeholder("time").set(time),
        )

    def followers_count(self, date: str, time: str):
        """
        `{amount} Followers`

        Description: Displays user's follower count

        Placeholders:
            amount: {
                "type": "int"
                "format": "compact"
            }
        """
        return self.followers_count_(self.lang, date, time)

    @staticmethod
    def followers_count_(lang: Lang, amount: int):
        """
        `{amount} Followers`

        Description: Displays user's follower count

        Placeholders:
            amount: {
                "type": "int"
                "format": "compact"
            }
        """
        return Translator._localize(
            lang,
            "followersCount",
            PlaceholderNum("amount", format=NumFormat.compact, num_type=NumType.int).set(amount),
        )
