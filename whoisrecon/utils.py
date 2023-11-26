# whoisrecon/utils.py
import re, requests, whois
from datetime import datetime, timezone
from bs4 import BeautifulSoup


def query_iq(filters):
    url = "https://iqwhois.com/advanced-search"

    payload = {
        '_token': '65jmzKmOk5Mp9vrd88NT9RkhbICROo2xd8Atjbml',
        'expiration': 0,
        'registered': 0,
        'updated': 0
    }
    
    section, field_value = filters.split(":", 1)
    field, value = field_value.split("=")
    
    payload['Whois_Section[]'] = section
    payload['Field[]'] = field
    payload['searchTerm[]'] = value

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        domain_name_elements = soup.select('.iq-connected-domain-name .conn-domain-name-class')
        
        domain_names = [element.get_text() for element in domain_name_elements]
        return domain_names
    else:
        return f"Error: {response.status_code}"


def validate_filter(filters):
    valid_sections = ["Admin", "Registrant", "Technical", "Billing"]
    valid_fields = ["Name", "Organization", "Email", "Street", "City", "State", "PostalCode", "Fax", "Country", "Telephone"]

    
    match = re.match(r'^([a-zA-Z]+):([a-zA-Z]+)=(.+)$', filters)
    if not match:
        raise ValueError(f"Invalid filter format: {filters}. Use 'Section:Field=Value'.")

    section, field, value = match.groups()

    if section not in valid_sections:
        raise ValueError(f"Invalid section in filter: {section}. Valid sections are {', '.join(valid_sections)}.")

    if field not in valid_fields:
        raise ValueError(f"Invalid field in filter: {field}. Valid fields are {', '.join(valid_fields)}.")

    return True


def enrich_data(domains):
    results = [["Domain", "Creation Date", "Expiration Date", "Registrar", "Name Servers"]]


    for domain in domains:
        try:
            info = whois.whois(domain)

            try:
                creation_date_str = format_datetime(info.creation_date)  
            except:
                creation_date_str = "Unsupported TLD/Unregistered"
            try:
                expiration_date_str = format_datetime(info.expiration_date)
            except:
                expiration_date_str = "Unsupported TLD/Unregistered"
            
            enriched_data = [
                domain,
                creation_date_str,
                expiration_date_str,
                info.registrar,
                info.name_servers
            ]

            results.append(enriched_data)
        except Exception as e:
            enriched_data = [
                domain,
                "",
                "",
                "",
                "" 
            ]
            results.append(enriched_data)
    return results


"""
WHOIS occasionally provides a list of DateTimes instead of a single item, 1-2 of which include TimeZone information.

The DateTime's are all the same and in UTC(it seems) so this just normalizes the output into a single DateTime.
"""
def format_datetime(dt):
    if isinstance(dt, list):
        if dt[0].tzinfo is not None:
            dt_utc = dt[0].astimezone(timezone.utc)
            return dt_utc.strftime('%Y-%m-%d %H:%M:%S %Z')
        else:
            return dt[0].strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(dt, datetime):
        if dt.tzinfo is not None:
            dt_utc = dt.astimezone(timezone.utc)
            return dt_utc.strftime('%Y-%m-%d %H:%M:%S %Z')
        else:
            return dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None