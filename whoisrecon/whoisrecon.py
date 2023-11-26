import argparse, tabulate
from utils import query_iq, validate_filter, enrich_data

# Example Usage: whoisrecon --filter 

def parse_argument():
    parser = argparse.ArgumentParser(
        description="WHOIS Reconnaissance Tool",
        epilog="Example: python whoisrecon.py --filter \"Admin:Name=John Doe\" --filter \"Admin:Email=*@example.com\"")

    parser.add_argument("-e", "--enrich", action="store_true",
                        help="Enrich the data with additional WHOIS information. May increase the run time of the program significantly with larger datasets.")

    parser.add_argument("--filter", action="store",
                        help="Specify a filter for WHOIS query (e.g., 'Admin:Name=John Doe'). "
                             "Accepted options for sections: Admin, Registrant, Technical, Billing. "
                             "Accepted options for fields: Name, Organization, Email, Street, City, "
                             "State, PostalCode, Fax, Country, Telephone. You cannot use multiple filters in the same query.")
        
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0", help="Prints the current version information.")

    return parser.parse_args()


def main():
    try:
        args = parse_argument()
        filters = args.filter

        if not filters:
            raise ValueError("At least one filter must be specified. Use --filter option.")
        
        if validate_filter(filters):
            results = query_iq(filters)
        
        if len(results) <= 0:
            print("No Results Found...")
            return

        if args.enrich:
            results = enrich_data(results)
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