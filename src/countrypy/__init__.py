import requests

API_URL = ("https://restcountries.com/v3.1/all"
           "?fields=name,flags,cca2,capital,idd,tld,population,languages,"
           "timezones,currencies,region,subregion,independent,area,"
           "landlocked,demonyms,unMember,maps,fifa,startOfWeek")


class CountryData:
    """
    A class to fetch and manage country data from the REST Countries API.
    """

    def __init__(self):
        """
        Initializes CountryData by fetching data from the API.
        """
        self.data = self.fetch_country_data()

    @staticmethod
    def fetch_country_data():
        """
        Fetches country data from the API.

        Returns:
            list: A list of country data dictionaries.
        
        Raises:
            Exception: If there is an issue with the API request.
        """
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch country data: {e}")

    def get_country_info(self, country_code):
        """
        Retrieves country information by ISO country code.

        Args:
            country_code (str): The ISO country code.

        Returns:
            dict or None: Country information dictionary, or None if not found.
        
        Raises:
            Exception: If required data fields are missing in the API response.
        """
        try:
            for country in self.data:
                if country['cca2'] == country_code:
                    return self._extract_country_info(country)
            return None
        except KeyError as e:
            raise Exception(f"Data missing in country info: {e}")

    def get_country_info_by_name(self, foreign_country_name):
        """
        Retrieves country information by country name or alternative name.

        Args:
            foreign_country_name (str): The country name or alternative name.

        Returns:
            dict or None: Country information dictionary, or None if not found.
        
        Raises:
            Exception: If required data fields are missing in the API response.
        """
        try:
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
        except KeyError as e:
            raise Exception(f"Data missing in country info by name: {e}")

    @staticmethod
    def _extract_country_info(country):
        """
        Extracts relevant country information from the API response.

        Args:
            country (dict): The country data dictionary from the API response.

        Returns:
            dict: A dictionary containing the extracted country information.
        
        Raises:
            Exception: If required data fields are missing in the API response.
        """
        try:
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
        except KeyError as e:
            raise Exception(f"Data missing while extracting country info: {e}")

    def get_number_of_countries(self):
        """
        Returns the number of countries in the dataset.

        Returns:
            int: The number of countries.
        """
        return len(self.data)


class CountryNotFoundError(Exception):
    """
    Exception raised when a country is not found.
    """
    pass


class Country:
    """
    Represents a specific country identified by either ISO country code or name.
    
    Attributes:
        data_source (CountryData): Source of country data.
        info (dict): Detailed information about the country.
    """

    def __init__(self, identifier):
        """
        Initializes a Country object and retrieves the corresponding country data.
        
        Args:
            identifier (str): ISO country code or name of the country.
            
        Raises:
            CountryNotFoundError: If the country data is not found based on the identifier.
        """
        self.data_source = CountryData()
        self.info = self._fetch_country_info(identifier)
        if not self.info:
            raise CountryNotFoundError(f"Country '{identifier}' not found.")

    def _fetch_country_info(self, identifier):
        """
        Fetches country information using the identifier (ISO code or name).
        
        Args:
            identifier (str): ISO country code or name of the country.
        
        Returns:
            dict or None: Country information dictionary, or None if not found.
        """
        try:
            country_info = self.data_source.get_country_info(identifier.upper())
            if not country_info:
                country_info = self.data_source.get_country_info_by_name(identifier)
            return country_info
        except Exception as e:
            raise Exception(f"Error fetching country info: {e}")

    @property
    def name(self):
        """
        Returns the common name of the country.

        Returns:
            str or None: Common name of the country.
        """
        return self.info.get('name') if self.info else None

    @property
    def official_name(self):
        """
        Returns the official name of the country.

        Returns:
            str or None: Official name of the country.
        """
        return self.info.get('official_name') if self.info else None

    @property
    def iso_code(self):
        """
        Returns the ISO country code.

        Returns:
            str or None: ISO country code.
        """
        return self.info.get('iso_code') if self.info else None

    @property
    def phone_code(self):
        """
        Returns the phone code root for the country.

        Returns:
            str or None: Phone code root.
        """
        return self.info.get('phone_code_root') if self.info else None

    @property
    def population(self):
        """
        Returns the population of the country.

        Returns:
            int or str: Population of the country.
        """
        return self.info.get('population') if self.info else None

    @property
    def languages(self):
        """
        Returns the languages spoken in the country.

        Returns:
            dict: Languages spoken in the country.
        """
        return self.info.get('languages') if self.info else None

    @property
    def timezone(self):
        """
        Returns the timezones of the country.

        Returns:
            list: List of timezones in the country.
        """
        return self.info.get('timezones') if self.info else None

    @property
    def currency(self):
        """
        Returns the currency code of the country.

        Returns:
            str: Currency code.
        """
        return self.info.get('currency') if self.info else None

    @property
    def capital(self):
        """
        Returns the capital city of the country.

        Returns:
            str or None: Capital city.
        """
        return self.info.get('capital') if self.info else None

    @property
    def flag(self):
        """
        Returns the flag URL of the country.

        Returns:
            str or None: URL to the country's flag image.
        """
        return self.info.get('flag') if self.info else None

    @property
    def tld(self):
        """
        Returns the top-level domains (TLDs) of the country.

        Returns:
            list: List of TLDs.
        """
        return self.info.get('tld') if self.info else None

    @property
    def region(self):
        """
        Returns the region of the country.

        Returns:
            str or None: Region of the country.
        """
        return self.info.get('region') if self.info else None

    @property
    def subregion(self):
        """
        Returns the subregion of the country.

        Returns:
            str or None: Subregion of the country.
        """
        return self.info.get('subregion') if self.info else None

    @property
    def independent(self):
        """
        Returns whether the country is independent.

        Returns:
            bool: True if the country is independent, otherwise False.
        """
        return self.info.get('independent') if self.info else None

    @property
    def area(self):
        """
        Returns the area of the country in square kilometers.

        Returns:
            float or str: Area of the country.
        """
        return self.info.get('area') if self.info else None

    @property
    def landlocked(self):
        """
        Returns whether the country is landlocked.

        Returns:
            bool: True if the country is landlocked, otherwise False.
        """
        return self.info.get('landlocked') if self.info else None

    @property
    def demonym(self):
        """
        Returns the demonym for the country.

        Returns:
            str or None: Demonym of the country.
        """
        return self.info.get('demonym') if self.info else None

    @property
    def un_member(self):
        """
        Returns whether the country is a member of the United Nations.

        Returns:
            bool: True if the country is a UN member, otherwise False.
        """
        return self.info.get('un_member') if self.info else None

    @property
    def google_maps_link(self):
        """
        Returns the Google Maps link for the country.

        Returns:
            str or None: URL to Google Maps for the country.
        """
        return self.info.get('google_maps_link') if self.info else None

    @property
    def fifa_code(self):
        """
        Returns the FIFA code of the country.

        Returns:
            str or None: FIFA code.
        """
        return self.info.get('fifa_code') if self.info else None

    @property
    def start_of_week(self):
        """
        Returns the day on which the week starts in the country.

        Returns:
            str or None: Start of the week day.
        """
        return self.info.get('start_of_week') if self.info else None
