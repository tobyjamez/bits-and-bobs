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
            "To find blablacars to a city, prefix the city name with"\
            " \"#t\", eg #tBerlin.\n"\
            "\nThe program sometimes interprets weird strings as"\
            "cities.\nThis is on blablacar's end.\n"


def parse_results(response: requests.models.Response,
                  to=False) -> dict:
    """
    Parse a response from a requests.get call into a suitable dictionary
    for links.
    Prints each option.

    :param response: The response from a requests.get call to blablacar.
    :type response: requests.models.Response.
    :param to: If True, prints departure cities for each car, rather
               than arrivals.
    :type to: bool.

    :returns: A dictionary of letters and urls to blablacar.
    :rtype: dict.
    """

    places = ['arrival_place', 'departure_place']

    url_dict = {}

    results = response.json()
    print("Interpreted your input as: ",
          results['trips'][0][places[int(~to)]]['city_name'].strip(), '.')
    print("The following trips are available:\n")

    for index, trip in enumerate(results['trips']):
        print("  [%s]" % ALPHABET[index],
              trip[places[int(to)]]['city_name'], ":")

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

    if origin.lower() == 'q':
        exit()

    if origin.lower() == 'help':
        print(HELP_TEXT)
        origin = input("Please enter a city:\n$ ").title()

    params = dict(de=datetime.datetime.today().strftime('%Y-%m-%d'),
                  limit=25)

    if origin[0] == '#':
        if origin[1].lower() == 't':
            origin = origin[2:].title()
            params['tn'] = origin
            place = 'tn'
            to = True

        else:
            place = 'fn'
            to = False

    else:
        params['fn'] = origin
        place = 'fn'
        to = False

    while True:
        response = requests.get(API_URL,
                                params=params,
                                headers=dict(Key=key))

        if response.status_code != 200:
            params[place] = input("Sorry, I couldn't find city. %r \n"
                                  "Please enter another.\n$ " % origin).title()
        else:
            break

    try:
        url_dict = parse_results(response, to=to)
    except(IndexError):
        print("Sorry. No trips found.")
        exit()

    next_step = input("> ")

    if next_step.lower() == 'q':
        exit()
    else:
        webbrowser.open(url_dict[next_step[0].upper()])
