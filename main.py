import logging
import json
import requests
import pyfiglet

# Print DAVID in ascii
print(pyfiglet.figlet_format("DAVID"))

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_phone_details(phone_number):
    """
    This function takes a phone number as an argument and returns a dictionary
    containing the geo location, name, ISP, and IP associated with the phone number.

    Args:
        phone_number (str): The phone number to be tracked.

    Returns:
        dict: A dictionary containing the geo location, name, ISP, and IP associated with
        the phone number.
    """
    # Make API request
    url = f"https://api.phonenumbers.info/phone/{phone_number}"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Error making API request: {response.status_code}")
        return None

    # Parse response
    data = json.loads(response.text)
    details = {
        "geo_location": data["geo_location"],
        "name": data["name"],
        "isp": data["isp"],
        "ip": data["ip"]
    }

    return details

if __name__ == "__main__":
    # Get phone number
    phone_number = input("Please enter a phone number: ")

    # Get phone details
    details = get_phone_details(phone_number)
    if details is not None:
        print(details)
    else:
        logging.error("Error getting phone details")
