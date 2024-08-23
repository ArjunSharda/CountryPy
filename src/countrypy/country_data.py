import requests
import time

API_URL = "https://restcountries.com/v3.1/all"

class CountryData:
    def __init__(self):
        self.data = self.fetch_country_data()

    @staticmethod
    def fetch_country_data():
        time.sleep(1)
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
        return [country['name']['common'] for country in self.data]

    def get_countries_by_language(self, language_code):
        return [country['name']['common'] for country in self.data if language_code in country['languages'].values()]

    def get_countries_by_currency(self, currency_code):
        return [country['name']['common'] for country in self.data if currency_code in country.get('currencies', {})]

    def get_phone_code(self, country_code):
        for country in self.data:
            if country['cca2'] == country_code:
                return country['idd']['root']
        return None

    def get_all_timezones(self, country_code):
        for country in self.data:
            if country['cca2'] == country_code:
                return country['timezones']
        return None

    @staticmethod
    def _extract_country_info(country):
        return {
            'name': country['name']['common'],
            'official_name': country['name']['official'],
            'iso_code': country['cca2'],
            'capital': country.get('capital', ['N/A']),
            'flag': country['flags']['png'] if 'flags' in country else None,
            'phone_code_root': country['idd']['root'] if 'idd' in country else None,
            'tld': country.get('tld', []),
            'population': country.get('population', 'N/A'),
            'languages': country.get('languages', {}),
            'timezones': country.get('timezones', []),
            'currency': list(country['currencies'].keys())[0] if 'currencies' in country else 'N/A'
        }
