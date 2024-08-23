import requests

API_URL = "https://restcountries.com/v3.1/all"

class CountryData:
    def __init__(self):
        self.data = self.fetch_country_data()

    @staticmethod
    def fetch_country_data():
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch country data")

    def get_country_info(self, country_code):
        for country in self.data:
            if country['cca2'] == country_code:
                return self._extract_country_info(country)
        return None

    def get_country_info_by_name(self, foreign_country_name):
        foreign_country_name = foreign_country_name.lower()
        for country in self.data:
            if foreign_country_name in country['name']['common'].lower() or foreign_country_name in country['name'][
                'official'].lower():
                return self._extract_country_info(country)

            native_names = country['name'].get('nativeName', {})
            for native_name_info in native_names.values():
                if foreign_country_name in native_name_info['common'].lower() or foreign_country_name in \
                        native_name_info['official'].lower():
                    return self._extract_country_info(country)

            alt_spellings = country.get('altSpellings', [])
            for alt_name in alt_spellings:
                if foreign_country_name in alt_name.lower():
                    return self._extract_country_info(country)

        return None

    @staticmethod
    def _extract_country_info(country):
        return {
            'name': country['name']['common'],
            'official_name': country['name']['official'],
            'iso_code': country['cca2'],
            'capital': country.get('capital', ['N/A'])[0],
            'flag': country['flags']['png'] if 'flags' in country else None,
            'phone_code_root': country['idd']['root'] if 'idd' in country else None,
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

    def get_number_of_countries(self):
        return len(self.data)

class CountryNotFoundError(Exception):
    """Exception raised when a country is not found."""
    pass

class Country:
    def __init__(self, identifier):
        self.data_source = CountryData()
        self.info = self._fetch_country_info(identifier)
        if not self.info:
            raise CountryNotFoundError(f"Country '{identifier}' not found.")

    def _fetch_country_info(self, identifier):
        country_info = self.data_source.get_country_info(identifier.upper())
        if not country_info:
            country_info = self.data_source.get_country_info_by_name(identifier)
        return country_info

    @property
    def name(self):
        return self.info.get('name') if self.info else None

    @property
    def official_name(self):
        return self.info.get('official_name') if self.info else None

    @property
    def iso_code(self):
        return self.info.get('iso_code') if self.info else None

    @property
    def phone_code(self):
        return self.info.get('phone_code_root') if self.info else None

    @property
    def population(self):
        return self.info.get('population') if self.info else None

    @property
    def languages(self):
        return self.info.get('languages') if self.info else None

    @property
    def timezone(self):
        return self.info.get('timezones') if self.info else None

    @property
    def currency(self):
        return self.info.get('currency') if self.info else None

    @property
    def capital(self):
        return self.info.get('capital') if self.info else None

    @property
    def flag(self):
        return self.info.get('flag') if self.info else None

    @property
    def tld(self):
        return self.info.get('tld') if self.info else None

    @property
    def region(self):
        return self.info.get('region') if self.info else None

    @property
    def subregion(self):
        return self.info.get('subregion') if self.info else None

    @property
    def independent(self):
        return self.info.get('independent') if self.info else None

    @property
    def area(self):
        return self.info.get('area') if self.info else None

    @property
    def landlocked(self):
        return self.info.get('landlocked') if self.info else None

    @property
    def demonym(self):
        return self.info.get('demonym') if self.info else None

    @property
    def un_member(self):
        return self.info.get('un_member') if self.info else None

    @property
    def google_maps_link(self):
        return self.info.get('google_maps_link') if self.info else None

    @property
    def fifa_code(self):
        return self.info.get('fifa_code') if self.info else None

    @property
    def start_of_week(self):
        return self.info.get('start_of_week') if self.info else None
