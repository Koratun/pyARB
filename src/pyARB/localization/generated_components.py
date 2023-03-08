from enum import Enum
from pyARB.localize import log, read_translations, inject_placeholders, Placeholder, PlaceholderNum, NumFormat, NumType


class Lang(Enum):
    en_US = "en_US"
    es_ES = "es_ES"


TRANSLATIONS = read_translations("src/pyARB/localization/arbs", Lang)
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

    def united_states(self):
        """
        `United States`
        """
        return self.united_states_static(self.lang)

    @staticmethod
    def united_states_static(lang: Lang):
        """
        `United States`
        """
        return Translator._localize(lang, "unitedStates")

    def puerto_rico(self):
        """
        `Puerto Rico`
        """
        return self.puerto_rico_static(self.lang)

    @staticmethod
    def puerto_rico_static(lang: Lang):
        """
        `Puerto Rico`
        """
        return Translator._localize(lang, "puertoRico")

    def canada(self):
        """
        `Canada`
        """
        return self.canada_static(self.lang)

    @staticmethod
    def canada_static(lang: Lang):
        """
        `Canada`
        """
        return Translator._localize(lang, "canada")

    def mexico(self):
        """
        `Mexico`
        """
        return self.mexico_static(self.lang)

    @staticmethod
    def mexico_static(lang: Lang):
        """
        `Mexico`
        """
        return Translator._localize(lang, "mexico")

    def virgin_islands_british(self):
        """
        `Virgin Islands, British`
        """
        return self.virgin_islands_british_static(self.lang)

    @staticmethod
    def virgin_islands_british_static(lang: Lang):
        """
        `Virgin Islands, British`
        """
        return Translator._localize(lang, "virginIslandsBritish")

    def virgin_islands_us(self):
        """
        `Virgin Islands, US`
        """
        return self.virgin_islands_us_static(self.lang)

    @staticmethod
    def virgin_islands_us_static(lang: Lang):
        """
        `Virgin Islands, US`
        """
        return Translator._localize(lang, "virginIslandsUS")

    def united_kingdom(self):
        """
        `United Kingdom`
        """
        return self.united_kingdom_static(self.lang)

    @staticmethod
    def united_kingdom_static(lang: Lang):
        """
        `United Kingdom`
        """
        return Translator._localize(lang, "unitedKingdom")

    def france(self):
        """
        `France`
        """
        return self.france_static(self.lang)

    @staticmethod
    def france_static(lang: Lang):
        """
        `France`
        """
        return Translator._localize(lang, "france")

    def switzerland(self):
        """
        `Switzerland`
        """
        return self.switzerland_static(self.lang)

    @staticmethod
    def switzerland_static(lang: Lang):
        """
        `Switzerland`
        """
        return Translator._localize(lang, "switzerland")

    def bulgaria(self):
        """
        `Bulgaria`
        """
        return self.bulgaria_static(self.lang)

    @staticmethod
    def bulgaria_static(lang: Lang):
        """
        `Bulgaria`
        """
        return Translator._localize(lang, "bulgaria")

    def estonia(self):
        """
        `Estonia`
        """
        return self.estonia_static(self.lang)

    @staticmethod
    def estonia_static(lang: Lang):
        """
        `Estonia`
        """
        return Translator._localize(lang, "estonia")

    def greece(self):
        """
        `Greece`
        """
        return self.greece_static(self.lang)

    @staticmethod
    def greece_static(lang: Lang):
        """
        `Greece`
        """
        return Translator._localize(lang, "greece")

    def latvia(self):
        """
        `Latvia`
        """
        return self.latvia_static(self.lang)

    @staticmethod
    def latvia_static(lang: Lang):
        """
        `Latvia`
        """
        return Translator._localize(lang, "latvia")

    def spain(self):
        """
        `Spain`
        """
        return self.spain_static(self.lang)

    @staticmethod
    def spain_static(lang: Lang):
        """
        `Spain`
        """
        return Translator._localize(lang, "spain")

    def hungary(self):
        """
        `Hungary`
        """
        return self.hungary_static(self.lang)

    @staticmethod
    def hungary_static(lang: Lang):
        """
        `Hungary`
        """
        return Translator._localize(lang, "hungary")

    def romania(self):
        """
        `Romania`
        """
        return self.romania_static(self.lang)

    @staticmethod
    def romania_static(lang: Lang):
        """
        `Romania`
        """
        return Translator._localize(lang, "romania")

    def sweden(self):
        """
        `Sweden`
        """
        return self.sweden_static(self.lang)

    @staticmethod
    def sweden_static(lang: Lang):
        """
        `Sweden`
        """
        return Translator._localize(lang, "sweden")

    def austria(self):
        """
        `Austria`
        """
        return self.austria_static(self.lang)

    @staticmethod
    def austria_static(lang: Lang):
        """
        `Austria`
        """
        return Translator._localize(lang, "austria")

    def croatia(self):
        """
        `Croatia`
        """
        return self.croatia_static(self.lang)

    @staticmethod
    def croatia_static(lang: Lang):
        """
        `Croatia`
        """
        return Translator._localize(lang, "croatia")

    def finland_aland_islands(self):
        """
        `Finland/Aland Islands`
        """
        return self.finland_aland_islands_static(self.lang)

    @staticmethod
    def finland_aland_islands_static(lang: Lang):
        """
        `Finland/Aland Islands`
        """
        return Translator._localize(lang, "finlandAlandIslands")

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

    def stock_change(self, stock: str, pnl: float, profit_loss: str, pnl_decimal_digits: int = 2):
        """
        `{stock} has received {pnl} {profitLoss, select, profit{Profit} loss{Loss}, other{Even}}`

        Description: Show when a stock has changed and by how much

        Placeholders:
            stock: String
            pnl: {
                type: float
                format: decimalPercentPattern
                example: 1,234.56%
                description: Given the example; this placeholder would have been given the double: 12.3456. It should never receive a negative number. If it would have been negative, make `profitLoss` say `loss`.
                bakedParameters: {
                    decimalDigits: 2
                }
            }
            profitLoss: String
        """
        return self.stock_change_static(self.lang, stock, pnl, profit_loss, pnl_decimal_digits=pnl_decimal_digits)

    @staticmethod
    def stock_change_static(lang: Lang, stock: str, pnl: float, profit_loss: str, pnl_decimal_digits: int = 2):
        """
        `{stock} has received {pnl} {profitLoss, select, profit{Profit} loss{Loss}, other{Even}}`

        Description: Show when a stock has changed and by how much

        Placeholders:
            stock: String
            pnl: {
                type: float
                format: decimalPercentPattern
                example: 1,234.56%
                description: Given the example; this placeholder would have been given the double: 12.3456. It should never receive a negative number. If it would have been negative, make `profitLoss` say `loss`.
                bakedParameters: {
                    decimalDigits: 2
                }
            }
            profitLoss: String
        """
        return Translator._localize(
            lang,
            "stockChange",
            Placeholder("stock").set(stock),
            PlaceholderNum("pnl", format=NumFormat.decimalPercentPattern, num_type=NumType.double, decimalDigits=pnl_decimal_digits).set(pnl),
            Placeholder("profitLoss").set(profit_loss),
        )
