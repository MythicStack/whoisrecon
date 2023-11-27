#!/usr/bin/env python

"""
Copyright 2023 John Christian (MythicStack)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import argparse, tabulate
from whoisrecon.utils import query_iq, validate_filter, enrich_data


def parse_argument():
    parser = argparse.ArgumentParser(
        description="WHOIS Reconnaissance Tool",
        epilog="Example: whoisrecon --filter \"Admin:Name=* Doe\"")

    parser.add_argument("--active", "-a", action="store_true",
                        help="Display only active WHOIS information. This also filters out domains unsupported by the queried WHOIS registry.")

    parser.add_argument("--count", "-c", action="store_true",
                        help="Return a count of the items found from the filter.")

    parser.add_argument("--enrich", "-e", action="store_true",
                        help="Enrich the data with additional WHOIS information. May increase the run time of the program significantly with larger datasets. Perform a --count first.")

    parser.add_argument("--filter", action="store",
                        help="Specify a filter for WHOIS query (e.g., 'Admin:Name=John Doe'). "
                             "Accepted options for 'sections': Admin, Registrant, Technical, Billing. "
                             "Accepted options for 'fields': Name, Organization, Email, Street, City, "
                             "State, PostalCode, Fax, Country, Telephone. You cannot use multiple filters in the same query.")
        
    parser.add_argument("--version", "-v", action="version", version="%(prog)s 1.0", help="Prints the current version information.")

    return parser.parse_args()


def main():
    try:
        args = parse_argument()
        filters = args.filter

        if args.count and (args.active or args.enrich or args.active):
            raise ValueError("The --count option cannot be enabled with other options.")

        if args.active and not args.enrich:
            raise ValueError("The --active option must be used with the --enrich option.")

        if not filters:
            raise ValueError("At least one filter must be specified. Use --filter option.")
        
        if validate_filter(filters):
            results = query_iq(filters)
        
        if args.count:
            print(len(results))
            return

        if len(results) <= 0:
            print("No Results Found...")
            return

        if args.enrich:
            results = enrich_data(results, args.active)
            table = tabulate.tabulate(results,headers='firstrow')
            print(table)           
        else:
            for result in results:
                print(result)
    except Exception as e:
        print(f"Error: {e}")
        print("Use the --help option for usage information.")


if __name__ == "__main__":
    main()