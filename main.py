import pyfiglet
import phonenumbers
from phonenumbers import geocoder, timezone
from datetime import datetime
import pytz


def track_phone_number(phone_number):
    """
    This function takes a phone number in the format +1-XXX-XXX-XXXX and prints DAVID in ascii.
    It also tracks the phone number and prints the geo location, country code, area code, and line type.
    Additionally, it prints the current time and date of the location associated with the phone number.
    
    Args:
        phone_number (str): Phone number in the format +1-XXX-XXX-XXXX
    
    Returns:
        None
    """
    # Print DAVID in ascii
    print(pyfiglet.figlet_format('DAVID'))

    # Validate phone number
    try:
        phone_number = phonenumbers.parse(phone_number, None)
    except phonenumbers.NumberParseException:
        print('Invalid phone number')
        return

    # Get geo location
    geo_location = geocoder.description_for_number(phone_number, 'en')
    print('Geo Location: {}'.format(geo_location))

    # Get country code
    country_code = phonenumbers.region_code_for_number(phone_number)
    print('Country Code: {}'.format(country_code))

    # Get area code
    location = geocoder.description_for_number(phone_number, 'en', region='US')
    location_parts = location.split(',')
    if len(location_parts) > 1:
        area_code = location_parts[1].strip()
        print('Area Code: {}'.format(area_code))
    else:
        print('Area Code: Not available')

    # Get line type
    line_type = phonenumbers.number_type(phone_number)
    print('Line Type: {}'.format(line_type))

    # Get timezone
    timezone_name = timezone.time_zones_for_number(phone_number)[0]
    timezone_object = pytz.timezone(timezone_name)

    # Get current time and date of the location
    timezone_datetime = datetime.now(timezone_object)
    print('Current time and date: {}'.format(timezone_datetime))


if __name__ == '__main__':
    phone_number = input('Enter phone number in the format +1-XXX-XXX-XXXX: ')
    track_phone_number(phone_number)
