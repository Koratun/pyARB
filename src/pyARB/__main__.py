import argparse
import sys
from localization_generator import generate_localizations


def main():
    parser = argparse.ArgumentParser(description="pyARB command line tool")
    subparsers = parser.add_subparsers(dest="command")

    # Define the "help" command
    help_parser = subparsers.add_parser("help", help="Display help information")
    help_parser.add_argument("command", nargs="?", help="The command to display help information for.")

    # Define other commands here...
    arb_parser = subparsers.add_parser(
        "l10ns", help="Generate the python code for the localizations based on the primary arb file"
    )
    arb_parser.add_argument("arb_location", help="The directory containing the arb files.")
    arb_parser.add_argument(
        "target_directory",
        nargs="?",
        help="Location of the generated py file. Defaults to the directory above arb_location.",
    )

    args = parser.parse_args()

    # Handle the "help" command
    if args.command == "help":
        if args.command:
            # Display help information for the specified command
            subparsers.choices[args.command].print_help()
        else:
            # Display general help information
            parser.print_help()

    # Handle other commands here...
    if args.command == "l10ns":
        locales = []
        print(
            "\n\u001b[34mpyARB Localization Generator\u001b[0m\n\n"
            "Enter a list of locales one at a time such as en_US.\n"
            "Input the same entry twice to remove it from the list.\n"
            "The first entered will be considered the primary locale:\n"
        )

        while True:
            inp = input("\u001b[33m>> \u001b[0m")
            if inp == "":
                break
            if inp not in locales:
                locales.append(inp)
            else:
                locales.remove(inp)

            print("\u001b[32mLocales:", *locales, "\u001b[0m")

        print("\u001b[32mLocales:", *locales, "\u001b[0m\n")

        generate_localizations(args.arb_location, locales, target_directory=args.target_directory)


if __name__ == "__main__":
    main()
