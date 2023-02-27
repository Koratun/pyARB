from pyARB.localization_generator import generate_localizations

if __name__ == "__main__":
    generate_localizations("src/pyARB/localization/arbs", ["en_US", "es_ES"])

    from pyARB.localization.generated_components import Translator, Lang

    t = Translator(Lang.en_US)
    print(t.no())
    print(t.investment_created_at("01/01/2023", "4:30 PM"))
    print(t.followers_count(1000))
    print(t.followers_count(999))
    print(t.followers_count(6513443))
    print(t.followers_count(999950))
    print(t.followers_count(10000111))
    print(t.many_items("Bob", 10))
    print(t.notification_requested_to_follow("Koratun", 1))
    print(t.notification_requested_to_follow("Koratun", 2))
    print(t.notification_requested_to_follow("Koratun", 3))
    print(t.notification_requested_to_follow("Koratun", 1254))
    print(t.stock_change("AAPL", 0.244267, "profit"))
    print(t.stock_change("AAPL", 0.244267, "profit", pnl_decimal_digits=1))
    print(t.stock_change("AAPL", 0.244267, "profit", pnl_decimal_digits=3))

    print("\nSpanish translations:")
    print(Translator.followers_count_static(Lang.es_ES, 6851651))
    t = Translator(Lang.es_ES)
    print(t.no())
    print(t.investment_created_at("01/01/2023", "4:30 PM"))
    print(t.followers_count(1550))
    print(t.followers_count(9989))
    print(t.followers_count(651443))
    print(t.followers_count(9999570))
    print(t.followers_count(100700111))
    print(t.many_items("Juan", 10))
    print(t.notification_requested_to_follow("Koratun", 1))
    print(t.notification_requested_to_follow("Koratun", 2))
    print(t.notification_requested_to_follow("Koratun", 3))
    print(t.notification_requested_to_follow("Koratun", 4254))
