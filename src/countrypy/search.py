from countrypy import CountryData

class Search:
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