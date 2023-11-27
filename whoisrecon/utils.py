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
import re, requests, whois
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import os, sys


def query_iq(filters):
    url = "https://iqwhois.com/advanced-search"

    payload = {
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
    valid_sections = ["admin", "registrant", "technical", "billing"]
    valid_fields = ["name", "organization", "email", "street", "city", "state", "postalcode", "fax", "country", "telephone"]

    
    match = re.match(r'^([a-zA-Z]+):([a-zA-Z]+)=(.+)$', filters)
    if not match:
        raise ValueError(f"Invalid filter format: {filters}. Use 'Section:Field=Value'.")

    section, field, value = match.groups()

    if section.lower() not in valid_sections:
        raise ValueError(f"Invalid section in filter: {section}. Valid sections are {', '.join(valid_sections)}.")

    if field.lower() not in valid_fields:
        raise ValueError(f"Invalid field in filter: {field}. Valid fields are {', '.join(valid_fields)}.")

    return True
 

def enrich_data(domains, display_active):
    results = [["Domain", "Creation Date", "Expiration Date", "Registrar", "Name Servers"]]
    original_out = sys.stdout

    for domain in domains:
        try:
            #WHOIS prints information to the console in some cases. This forces it to output that to NULL for a cleaner console.
            sys.stdout = open(os.devnull, 'w')
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
            if "-" in creation_date_str:
                results.append(enriched_data)
        except:
            enriched_data = [
                domain,
                "",
                "",
                "",
                "" 
            ]
            if not display_active:
                results.append(enriched_data)
            pass
    sys.stdout = original_out
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