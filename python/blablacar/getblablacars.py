"""
Quick program to get all blablacars leaving a given city today.
"""
import requests
import datetime
import json
import webbrowser
from auth import key

API_URL = "https://public-api.blablacar.com/api/v2/trips?"
ALPHABET = "ABCDEFGHIJKLMNOPRSTUVWXYZ"
HELP_TEXT = "\nType your origin city.\n"\
            "If any of the options interest you, enter their letter\n"\
            "to view the webpage.\n"\
            "Else, enter q to quit.\n"\
            "\nThe program sometimes interprets weird strings as"\
            "cities.\nThis is on blablacar's end.\n"


def parse_results(response: requests.models.Response) -> dict:
    """
    Parse a response from a requests.get call into a suitable dictionary
    for links.
    Prints each option.

    :param response: The response from a requests.get call to blablacar.
    :type: response: requests.models.Response.

    :returns: A dictionary of letters and urls to blablacar.
    :rtype: dict.
    """

    url_dict = {}

    results = response.json()
    print("Interpreted your input as: ",
          results['trips'][0]['departure_place']['city_name'].strip(), '.')
    print("The following trips are available:\n")

    for index, trip in enumerate(results['trips']):
        print("  [%s]" % ALPHABET[index],
              trip['arrival_place']['city_name'], ":")

        print("    Costs:",
              "%.2f" % float(trip['price_with_commission']['value'] + 1),
              trip['price_with_commission']['currency'])

        print("    Leaves at:",
              trip['departure_date'])

        url_dict[ALPHABET[index]] = trip['links']['_front']

    return url_dict

# ----------------------------------------------------------------------

if __name__ == "__main__":

    origin = input("Please enter a city or type help for help:\n$ ").title()

    if origin.lower() == 'help':
        print(HELP_TEXT)
        origin = input("Please enter a city:\n$ ").title()

    params = dict(fn=origin,
                  de=datetime.datetime.today().strftime('%Y-%m-%d'),
                  limit=25)

    while True:
        response = requests.get(API_URL,
                                params=params,
                                headers=dict(Key=key))

        if response.status_code != 200:
            params['fn'] = input("Sorry, I couldn't find that city.\n"
                                 "Please enter another.\n$ ")
        else:
            break

    try:
        url_dict = parse_results(response)
    except(IndexError):
        print("Sorry. No trips found.")
        exit()

    next_step = input("> ")

    if next_step.lower() == 'q':
        exit()
    else:
        webbrowser.open(url_dict[next_step[0].upper()])
