import requests
import time

API_URL = "https://restcountries.com/v3.1/all"

class CountryData:
    """Class to fetch and manage country data from an external API."""
    
    def __init__(self):
        self.data = self.fetch_country_data()

    @staticmethod
    def fetch_country_data():
        """Fetch country data from the API."""
        time.sleep(1)
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        raise Exception("Failed to fetch country data")

    def get_country_info(self, country_code):
        """Retrieve country information by ISO code."""
        for country in self.data:
            if country['cca2'] == country_code:
                return self._extract_country_info(country)
        return None

    def get_country_info_by_name(self, foreign_country_name):
        """Retrieve country information by name."""
        foreign_country_name = foreign_country_name.lower()
        for country in self.data:
            if (foreign_country_name in country['name']['common'].lower() or
                    foreign_country_name in country['name']['official'].lower()):
                return self._extract_country_info(country)

            native_names = country['name'].get('nativeName', {})
            for native_name_info in native_names.values():
                if (foreign_country_name in native_name_info['common'].lower() or
                        foreign_country_name in native_name_info['official'].lower()):
                    return self._extract_country_info(country)

            alt_spellings = country.get('altSpellings', [])
            for alt_name in alt_spellings:
                if foreign_country_name in alt_name.lower():
                    return self._extract_country_info(country)
        return None

    def get_all_countries(self):
        """Get a list of all country names."""
        return [country['name']['common'] for country in self.data]

    def get_countries_by_language(self, language_code):
        """Retrieve countries by language code."""
        return [country['name']['common'] for country in self.data if language_code in country['languages'].values()]

    def get_countries_by_currency(self, currency_code):
        """Retrieve countries by currency code."""
        return [country['name']['common'] for country in self.data if currency_code in country.get('currencies', {})]

    def get_phone_code(self, country_code):
        """Retrieve the phone code for a country by ISO code."""
        for country in self.data:
            if country['cca2'] == country_code:
                return country['idd']['root']
        return None

    def get_all_timezones(self, country_code):
        """Retrieve all timezones for a country by ISO code."""
        for country in self.data:
            if country['cca2'] == country_code:
                return country['timezones']
        return None

    @staticmethod
    def _extract_country_info(country):
        """Helper function to extract and structure country information."""
        phone_code = None
        if 'idd' in country:
            root = country['idd'].get('root', '')
            suffixes = country['idd'].get('suffixes', [])
            if len(suffixes) == 1:
                phone_code = f"{root}{suffixes[0]}"
            elif len(suffixes) > 1:
                phone_code = root
            else:
                phone_code = root

        return {
            'name': country['name']['common'],
            'official_name': country['name']['official'],
            'iso_code': country['cca2'],
            'capital': country.get('capital', ['N/A'])[0],
            'flag': country['flags']['png'] if 'flags' in country else None,
            'phone_code_root': phone_code,
            'tld': country.get('tld', []),
            'population': country.get('population', 'N/A'),
            'languages': country.get('languages', {}),
            'timezones': country.get('timezones', []),
            'currency': list(country['currencies'].keys())[0] if 'currencies' in country else 'N/A',
            'region': country.get('region', 'N/A'),
            'subregion': country.get('subregion', 'N/A'),
            'independent': country.get('independent', False),
            'area': country.get('area', 'N/A'),
            'landlocked': country.get('landlocked', False),
            'demonym': country['demonyms']['eng']['m'] if 'demonyms' in country else 'N/A',
            'un_member': country.get('unMember', False),
            'google_maps_link': country['maps']['googleMaps'] if 'maps' in country else None,
            'fifa_code': country.get('fifa', 'N/A'),
            'start_of_week': country.get('startOfWeek', 'N/A')
        }


class Search:
    """Class to search for countries based on specific attributes."""
    
    name = 'name'
    official_name = 'official_name'
    iso_code = 'iso_code'
    capital = 'capital'
    flag = 'flag'
    phone_code_root = 'phone_code_root'
    tld = 'tld'
    population = 'population'
    languages = 'languages'
    timezones = 'timezones'
    currency = 'currency'
    region = 'region'
    subregion = 'subregion'
    independent = 'independent'
    area = 'area'
    landlocked = 'landlocked'
    demonym = 'demonym'
    un_member = 'un_member'
    google_maps_link = 'google_maps_link'
    fifa_code = 'fifa_code'
    start_of_week = 'start_of_week'

    def __init__(self, attribute, value):
        self.data_source = CountryData()
        self.attribute = attribute
        self.value = value.lower() if isinstance(value, str) else value
        self.results = self._search()

    def _search(self):
        """Perform the search based on the attribute and value."""
        matching_countries = []

        for country in self.data_source.data:
            country_info = self.data_source._extract_country_info(country)

            if self.attribute not in country_info:
                continue

            country_value = country_info[self.attribute]

            if isinstance(country_value, (str, bool, int, float)) and self._compare_values(country_value):
                matching_countries.append(country_info)
            elif isinstance(country_value, list) and any(self._compare_values(item) for item in country_value):
                matching_countries.append(country_info)
            elif isinstance(country_value, dict) and any(self._compare_values(item) for item in country_value.values()):
                matching_countries.append(country_info)
            elif self.attribute == Search.languages and any(self._compare_values(item) for item in country_value.values()):
                matching_countries.append(country_info)

        if not matching_countries:
            raise ValueError(f"No countries found with {self.attribute} = {self.value}")

        return matching_countries

    def _compare_values(self, country_value):
        """Helper function to compare country value with search value, case-insensitive for strings."""
        if isinstance(country_value, str):
            return country_value.lower() == self.value
        return country_value == self.value

    def __str__(self):
        return "\n".join([country['name'] for country in self.results])
