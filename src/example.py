from pyARB.localization.generated_components import Translator, Lang

if __name__ == "__main__":
    t = Translator(Lang.en)
    print(t.no())
    print(t.investment_created_at("01/01/2023", "4:30 PM"))
    print(t.followers_count(1000))
    print(t.followers_count(999))
    print(t.followers_count(6513443))
    print(t.followers_count(999950))
    print(t.followers_count(10000111))
    print(t.notification_requested_to_follow("Koratun", 1))
    print(t.notification_requested_to_follow("Koratun", 2))
    print(t.notification_requested_to_follow("Koratun", 3))
    print(t.notification_requested_to_follow("Koratun", 1254))
