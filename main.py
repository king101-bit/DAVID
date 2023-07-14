import pyfiglet
import phonenumbers
from phonenumbers import geocoder, timezone, carrier
from datetime import datetime
import pytz
import requests

def track_phone_number(phone_number):
    """
    This function takes a phone number in the format +1-XXX-XXX-XXXX and performs various OSINT operations.
    It prints DAVID in ASCII art, tracks the phone number, and provides detailed information about it.

    Args:
        phone_number (str): Phone number in the format +1-XXX-XXX-XXXX

    Returns:
        None
    """
    # Print DAVID in ASCII art
    print(pyfiglet.figlet_format('DAVID'))

    # Validate phone number
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
    except phonenumbers.NumberParseException:
        print('Invalid phone number')
        return

    # Get geo location
    geo_location = geocoder.description_for_number(parsed_number, 'en')
    print('Geo Location: {}'.format(geo_location))

    # Get country code
    country_code = phonenumbers.region_code_for_number(parsed_number)
    print('Country Code: {}'.format(country_code))

    # Get area code
    if parsed_number.country_code != 0:
        area_code = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)[1:]
        print('Area Code: {}'.format(area_code))
    else:
        print('Area Code: Not available for this number!')

    # Get line type
    number_type = phonenumbers.number_type(parsed_number)
    print('Line Type: {}'.format(number_type))

    # Get carrier information
    carrier_info = carrier.name_for_number(parsed_number, 'en')
    print('Carrier: {}'.format(carrier_info))

    # Get timezone
    timezone_name = timezone.time_zones_for_number(parsed_number)[0]
    timezone_object = pytz.timezone(timezone_name)

    # Get current time and date of the location
    timezone_datetime = datetime.now(timezone_object)
    print('Current time and date: {}'.format(timezone_datetime))

    # Perform reverse phone number lookup
    reverse_lookup(parsed_number)

    # Check if phone number is pwned using HIBP API
    check_pwned(phone_number)

def reverse_lookup(parsed_number):
    """
    This function performs a reverse phone number lookup and provides information associated with the phone number.

    Args:
        parsed_number (phonenumbers.PhoneNumber): Parsed phone number object

    Returns:
        None
    """
    if parsed_number.country_code != 0:
        phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        url = f'https://api.telnyx.com/v1/phone_number/{phone_number}'
        headers = {'User-Agent': 'OSINT Tool'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'national_destination_code' in data:
                destination_code = data['national_destination_code']
                print('Destination Code: {}'.format(destination_code))
            if 'carrier' in data:
                carrier = data['carrier']
                print('Carrier: {}'.format(carrier))
        else:
            print('Failed to perform reverse phone number lookup. Please try again later.')
    else:
        print('Reverse phone number lookup is not available for this number.')

def check_pwned(phone_number):
    """
    This function checks if a phone number has been compromised in known data breaches using the HIBP API.

    Args:
        phone_number (str): Phone number in the format +1-XXX-XXX-XXXX

    Returns:
        None
    """
    url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{phone_number}'
    headers = {'User-Agent': 'OSINT Tool'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print('This phone number has been pwned. It has appeared in the following data breaches:')
        data_breaches = response.json()
        for breach in data_breaches:
            print(' - {}'.format(breach['Title']))
    elif response.status_code == 404:
        print('This phone number has not been pwned.')
    else:
        print('Failed to check if the phone number is pwned. Please try again later.')

if __name__ == '__main__':
    phone_number = input('Enter phone number in the format +1-XXX-XXX-XXXX: ')
    track_phone_number(phone_number)
