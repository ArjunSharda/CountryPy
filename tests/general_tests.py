import unittest
from unittest.mock import patch
from countrypy import Country, CountryData

MOCK_COUNTRY_DATA = [
    {
        "flags": {
            "png": "https://flagcdn.com/w320/gd.png",
            "svg": "https://flagcdn.com/gd.svg",
            "alt": "The flag of Grenada features a large central rectangular area surrounded by a red border, with three five-pointed yellow stars centered on the top and bottom borders. The central rectangle is divided diagonally into four alternating triangular areas of yellow at the top and bottom and green on the hoist and fly sides, and a five-pointed yellow star on a red circle is superimposed at its center. A symbolic nutmeg pod is situated on the green hoist-side triangle."
        },
        "startOfWeek": "monday",
        "name": {
            "common": "Grenada",
            "official": "Grenada",
            "nativeName": {
                "eng": {
                    "official": "Grenada",
                    "common": "Grenada"
                }
            }
        },
        "tld": [".gd"],
        "cca2": "GD",
        "independent": True,
        "unMember": True,
        "currencies": {
            "XCD": {
                "name": "Eastern Caribbean dollar",
                "symbol": "$"
            }
        },
        "idd": {
            "root": "+1",
            "suffixes": ["473"]
        },
        "capital": ["St. George's"],
        "region": "Americas",
        "subregion": "Caribbean",
        "languages": {
            "eng": "English"
        },
        "landlocked": False,
        "area": 344,
        "demonyms": {
            "eng": {
                "f": "Grenadian",
                "m": "Grenadian"
            },
            "fra": {
                "f": "Grenadienne",
                "m": "Grenadien"
            }
        },
        "maps": {
            "googleMaps": "https://goo.gl/maps/rqWyfUAt4xhvk1Zy9",
            "openStreetMaps": "https://www.openstreetmap.org/relation/550727"
        },
        "population": 112519,
        "fifa": "GRN",
        "timezones": ["UTC-04:00"]
    },
    {
        "flags": {
            "png": "https://flagcdn.com/w320/ch.png",
            "svg": "https://flagcdn.com/ch.svg",
            "alt": "The flag of Switzerland is square shaped. It features a white Swiss cross centered on a red field."
        },
        "startOfWeek": "monday",
        "name": {
            "common": "Switzerland",
            "official": "Swiss Confederation",
            "nativeName": {
                "fra": {
                    "official": "Confédération suisse",
                    "common": "Suisse"
                },
                "gsw": {
                    "official": "Schweizerische Eidgenossenschaft",
                    "common": "Schweiz"
                },
                "ita": {
                    "official": "Confederazione Svizzera",
                    "common": "Svizzera"
                },
                "roh": {
                    "official": "Confederaziun svizra",
                    "common": "Svizra"
                }
            }
        },
        "tld": [".ch"],
        "cca2": "CH",
        "independent": True,
        "unMember": True,
        "currencies": {
            "CHF": {
                "name": "Swiss franc",
                "symbol": "Fr."
            }
        },
        "idd": {
            "root": "+4",
            "suffixes": ["1"]
        },
        "capital": ["Bern"],
        "region": "Europe",
        "subregion": "Western Europe",
        "languages": {
            "fra": "French",
            "gsw": "Swiss German",
            "ita": "Italian",
            "roh": "Romansh"
        },
        "landlocked": True,
        "area": 41284,
        "demonyms": {
            "eng": {
                "f": "Swiss",
                "m": "Swiss"
            },
            "fra": {
                "f": "Suisse",
                "m": "Suisse"
            }
        },
        "maps": {
            "googleMaps": "https://goo.gl/maps/uVuZcXaxSx5jLyEC9",
            "openStreetMaps": "https://www.openstreetmap.org/relation/51701"
        },
        "population": 8654622,
        "fifa": "SUI",
        "timezones": ["UTC+01:00"]
    }
]


class TestCountryPy(unittest.TestCase):

    @patch('countrypy.CountryData.fetch_country_data', return_value=MOCK_COUNTRY_DATA)
    def test_get_country_info(self, mock_fetch):
        country_info = Country("Grenada")
        self.assertEqual(country_info.name, "Grenada")
        self.assertEqual(country_info.capital, "St. George's")
        self.assertEqual(country_info.currency, "XCD")
        self.assertEqual(country_info.population, 112519)
        self.assertFalse(country_info.landlocked)

    @patch('countrypy.CountryData.fetch_country_data', return_value=MOCK_COUNTRY_DATA)
    def test_get_country_info_by_name(self, mock_fetch):
        country_info = Country("Switzerland")
        self.assertTrue(country_info.landlocked)
        self.assertEqual(country_info.capital, "Bern")
        self.assertIn(".ch", country_info.tld)
        self.assertEqual(country_info.area, 41284)

if __name__ == '__main__':
    unittest.main()