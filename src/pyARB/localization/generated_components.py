from enum import Enum
from pyARB.localize import log, read_translations, translate, Placeholder, PlaceholderNum, NumFormat, NumType


class Lang(Enum):
    en = "en"
    es = "es"


class Translator:
    translations = read_translations("src/pyARB/localization/arbs", Lang)
    fallback_lang = Lang.en

    def __init__(self, lang: Lang):
        self.lang = lang

    @staticmethod
    def _key_check(lang: Lang, key: str):
        if lang in Translator.translations:
            if key in Translator.translations[lang]:
                return True
            log.error(f"{lang.name}.arb does not have key `{key}`")
        return False

    @staticmethod
    def _translate(lang: Lang, key: str, *placeholders: Placeholder):
        if Translator._key_check(lang, key):
            return translate(Translator.translations[lang][key], *placeholders)
        if Translator._key_check(Translator.fallback_lang, key):
            return translate(Translator.translations[Translator.fallback_lang][key], *placeholders)
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
        return Translator._translate(lang, "no")

    def app_title(self):
        """
        `Involio`

        Description: The title of the application
        """
        return self.app_title_(self.lang)

    @staticmethod
    def app_title_(lang: Lang):
        """
        `Involio`

        Description: The title of the application
        """
        return Translator._translate(lang, "appTitle")

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
        return Translator._translate(
            lang,
            "investmentCreatedAt",
            Placeholder("date").set(date),
            Placeholder("time").set(time),
        )

    def followers_count(self, date: str, time: str):
        """
        `{amount} Followers`

        Description: Displays a position's creation date

        Placeholders:
            date: String
            time: String
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
        return Translator._translate(
            lang,
            "followersCount",
            PlaceholderNum("amount", format=NumFormat.compact, num_type=NumType.int).set(amount),
        )
