# whoisrecon

whoisrecon is a Python command-line tool designed for WHOIS reconnaissance, providing a streamlined way to find related domains from current and historical records (updated quarterly) based on search parameters.


[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)



## Features

- **Filtering Options**: Query for domains that match certain filters like the same Registrar, Organization or Email Domain.
- **Wildcard Searches**: Utilize wildcards (*) to broaden or narrow query results.
- **Enrich Data**: Enrich the returned domains for name servers, expiration dates, and registrar.
- **Historical Data**: Searches as historical database that is updated quarterly.


# Installation

```bash
pip install whoisrecon
```

## Usage

```bash
whoisrecon --help
```

## Example Usage
```bash
whoisrecon --filter "Registrant:Email=*@whois.com" --enrich
```

### Expected Output [^1]
```
Domain            Creation Date        Expiration Date      Registrar                                Name Servers
----------------  -------------------  -------------------  ---------------------------------------  -------------------------------
whois.com         1995-04-11 04:00:00  2028-04-12 04:00:00  PDR Ltd. d/b/a PublicDomainRegistry.com  ['ANASTASIA.NS.CLOUDFLARE.COM']
whoisdemo.com     2012-03-28 10:22:24  2024-03-28 10:22:24  PDR Ltd. d/b/a PublicDomainRegistry.com  ['ANASTASIA.NS.CLOUDFLARE.COM']
```
[^1]: Truncated for the example.

