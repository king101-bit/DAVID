import pyfiglet
import phonenumbers
from phonenumbers import geocoder, timezone, carrier
from datetime import datetime
import pytz
import requests

# Define the Truecaller API endpoint
TRUECALLER_API_URL = "https://api4.truecaller.com/v1/lookup"

def get_truecaller_api_key():
    """
    Function to prompt the user for their Truecaller API key.

    Returns:
        str: The user's Truecaller API key.
    """
    api_key = input("Enter your Truecaller API key: ")
    return api_key

def reverse_lookup(parsed_number, api_key):
    """
    Performs a reverse phone number lookup using the Truecaller API.

    Args:
        parsed_number (phonenumbers.PhoneNumber): Parsed phone number object.
        api_key (str): User's Truecaller API key.

    Returns:
        None
    """
    try:
        # Get the phone number in international format (e.g., +1XXXXXXXXXX)
        phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

        # Make the API request
        params = {
            "phoneNumber": phone_number,
            "countryCode": str(parsed_number.country_code),
            "apikey": api_key,
        }

        response = requests.get(TRUECALLER_API_URL, params=params)
        data = response.json()

        # Extract and print information from the API response
        if data["spam"] is False:
            print("Number not marked as spam on Truecaller.")
            if data["name"]:
                print("Name: {}".format(data["name"]))
            if data["city"]:
                print("City: {}".format(data["city"]["name"]))
            if data["carrier"]:
                print("Carrier: {}".format(data["carrier"]["name"]))
        else:
            print("Number marked as spam on Truecaller.")
    except Exception as e:
        print("Error performing reverse lookup:", e)

# Rest of the code remains the same...

if __name__ == '__main__':
    # Get Truecaller API key from the user during installation
    truecaller_api_key = get_truecaller_api_key()

    # Now you can use the obtained API key for reverse lookup
    phone_number = input('Enter phone number in the format +1-XXX-XXX-XXXX: ')
    track_phone_number(phone_number, truecaller_api_key)
