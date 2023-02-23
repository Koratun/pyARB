from enum import Enum
from pyARB.localize import log, read_translations, inject_placeholders, Placeholder, PlaceholderNum, NumFormat, NumType


class Lang(Enum):
    en_US = "en_US"
    es_ES = "es_ES"


TRANSLATIONS = read_translations("./src/pyARB/localization/arbs", Lang)
FALLBACK_LANG = Lang.en_US


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

    def investment_created_at(self, date: str, time: str):
        """
        `Opened: {date} at {time}`

        Description: Displays a position's creation date

        Placeholders:
            date: String
            time: String
        """
        return self.investment_created_at_static(self.lang, date, time)

    @staticmethod
    def investment_created_at_static(lang: Lang, date: str, time: str):
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

    def followers_count(self, amount: int):
        """
        `{amount} Followers`

        Description: Displays user's follower count

        Placeholders:
            amount: {
                type: int
                format: compact
            }
        """
        return self.followers_count_static(self.lang, amount)

    @staticmethod
    def followers_count_static(lang: Lang, amount: int):
        """
        `{amount} Followers`

        Description: Displays user's follower count

        Placeholders:
            amount: {
                type: int
                format: compact
            }
        """
        return Translator._localize(
            lang,
            "followersCount",
            PlaceholderNum("amount", format=NumFormat.compact, num_type=NumType.int).set(amount),
        )

    def no(self):
        """
        `No`
        """
        return self.no_static(self.lang)

    @staticmethod
    def no_static(lang: Lang):
        """
        `No`
        """
        return Translator._localize(lang, "no")

    def cancel(self):
        """
        `Cancel`

        Description: Cancel button
        """
        return self.cancel_static(self.lang)

    @staticmethod
    def cancel_static(lang: Lang):
        """
        `Cancel`

        Description: Cancel button
        """
        return Translator._localize(lang, "cancel")

    def joined_date(self, date: str):
        """
        `Joined {date}`

        Description: When a user signed up

        Placeholders:
            date: String
        """
        return self.joined_date_static(self.lang, date)

    @staticmethod
    def joined_date_static(lang: Lang, date: str):
        """
        `Joined {date}`

        Description: When a user signed up

        Placeholders:
            date: String
        """
        return Translator._localize(
            lang,
            "joinedDate",
            Placeholder("date").set(date),
        )

    def many_items(self, first: str, count: int):
        """
        `{first} and {count} others`

        Placeholders:
            first: String
            count: int
        """
        return self.many_items_static(self.lang, first, count)

    @staticmethod
    def many_items_static(lang: Lang, first: str, count: int):
        """
        `{first} and {count} others`

        Placeholders:
            first: String
            count: int
        """
        return Translator._localize(
            lang,
            "manyItems",
            Placeholder("first").set(first),
            PlaceholderNum("count", num_type=NumType.int).set(count),
        )

    def notification_requested_to_follow(self, username: str, count: int):
        """
        `@{username} {count, plural, offset:1 zero{has requested to follow you} one{and 1 other user have requested to follow you} other{and # other users have requested to follow you}}!`

        Description: When 1 or more users request to follow someone they receive this notification

        Placeholders:
            username: String
            count: {
                type: int
                format: compact
            }
        """
        return self.notification_requested_to_follow_static(self.lang, username, count)

    @staticmethod
    def notification_requested_to_follow_static(lang: Lang, username: str, count: int):
        """
        `@{username} {count, plural, offset:1 zero{has requested to follow you} one{and 1 other user have requested to follow you} other{and # other users have requested to follow you}}!`

        Description: When 1 or more users request to follow someone they receive this notification

        Placeholders:
            username: String
            count: {
                type: int
                format: compact
            }
        """
        return Translator._localize(
            lang,
            "notificationRequestedToFollow",
            Placeholder("username").set(username),
            PlaceholderNum("count", format=NumFormat.compact, num_type=NumType.int).set(count),
        )
