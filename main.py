import pyfiglet
import phonenumbers
from phonenumbers import geocoder, timezone, carrier
from datetime import datetime
import pytz

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

    try:
        # Validate phone number
        parsed_number = phonenumbers.parse(phone_number, None)
    except phonenumbers.NumberParseException:
        print('Invalid phone number')
        return

    # Get geo location
    try:
        geo_location = geocoder.description_for_number(parsed_number, 'en')
        print('Geo Location: {}'.format(geo_location))
    except Exception as e:
        print('Error fetching geo location:', e)

    # Get country code
    try:
        country_code = phonenumbers.region_code_for_number(parsed_number)
        print('Country Code: {}'.format(country_code))
    except Exception as e:
        print('Error fetching country code:', e)

    # Get area code
    try:
        if parsed_number.country_code != 0:
            area_code = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)[1:]
            print('Area Code: {}'.format(area_code))
        else:
            print('Area Code: Not available for this number!')
    except Exception as e:
        print('Error fetching area code:', e)

    # Get line type
    try:
        number_type = phonenumbers.number_type(parsed_number)
        print('Line Type: {}'.format(number_type))
    except Exception as e:
        print('Error fetching line type:', e)

    # Get carrier information
    try:
        carrier_info = carrier.name_for_number(parsed_number, 'en')
        print('Carrier: {}'.format(carrier_info))
    except Exception as e:
        print('Error fetching carrier information:', e)

    # Get timezone
    try:
        timezone_name = timezone.time_zones_for_number(parsed_number)[0]
        timezone_object = pytz.timezone(timezone_name)

        # Get current time and date of the location
        timezone_datetime = datetime.now(timezone_object)
        print('Current time and date: {}'.format(timezone_datetime))
    except Exception as e:
        print('Error fetching timezone:', e)

    # Perform reverse phone number lookup using phonenumbers package
    try:
        reverse_lookup(parsed_number)
    except Exception as e:
        print('Error performing reverse lookup:', e)

def reverse_lookup(parsed_number):
    """
    Performs a reverse phone number lookup using the phonenumbers package.

    Args:
        parsed_number (phonenumbers.PhoneNumber): Parsed phone number object.

    Returns:
        None
    """
    try:
        # Get the phone number in international format (e.g., +1XXXXXXXXXX)
        phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        # Replace this section with your preferred reverse lookup implementation
        # For this example, we'll print the international phone number.
        print("Reverse Lookup: {}".format(phone_number))
    except Exception as e:
        print("Error performing reverse lookup:", e)

if __name__ == '__main__':
    phone_number = input('Enter phone number in the format +1-XXX-XXX-XXXX: ')
    track_phone_number(phone_number)
