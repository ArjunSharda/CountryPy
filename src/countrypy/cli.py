import click
from countrypy.country_data import CountryData
from countrypy.ascii_art import print_ascii
import time
from colorama import Fore, Style
import os
import json

def warn_message(msg):
    click.echo(Fore.YELLOW + "[warn] " + msg + Style.RESET_ALL)

def success_message(msg):
    click.echo(Fore.GREEN + "[success] " + msg + Style.RESET_ALL)

def fail_message(msg):
    click.echo(Fore.RED + "[fail] " + msg + Style.RESET_ALL)

def loading_animation():
    click.echo(Fore.CYAN + "Loading", nl=False)
    for _ in range(3):
        time.sleep(0.5)
        click.echo(".", nl=False)
    click.echo(Style.RESET_ALL)

@click.group()
def cli():
    """CountryPy CLI: Get detailed information about any country."""
    print_ascii()


@cli.command()
@click.argument('country_code_or_name', nargs=-1)
def quickinfo(country_code_or_name):
    """Fetch and display information about a country by ISO code or name."""
    loading_animation()
    country_code_or_name = ' '.join(country_code_or_name)

    country_data = CountryData()

    country = country_data.get_country_info(country_code_or_name.upper()) or country_data.get_country_info_by_name(country_code_or_name)

    if country:
        success_message(f"Country found: {country['name']} ({country['iso_code']})")
        click.echo(f"Official Name: {Fore.YELLOW}{country['official_name']}{Style.RESET_ALL}")
        click.echo(f"Flag: {Fore.YELLOW}{country['flag']}{Style.RESET_ALL}")
        click.echo(f"Phone Code: {Fore.CYAN}{country['phone_code_root']}{Style.RESET_ALL}")
        click.echo(f"Capital: {Fore.LIGHTMAGENTA_EX}{', '.join(country['capital'])}{Style.RESET_ALL}")
        click.echo(f"TLD: {Fore.BLUE}{', '.join(country['tld'])}{Style.RESET_ALL}")
        click.echo(f"Population: {Fore.BLUE}{country['population']}{Style.RESET_ALL}")
        click.echo(f"Languages: {Fore.MAGENTA}{', '.join(country['languages'].values())}{Style.RESET_ALL}")
        click.echo(f"Timezones: {Fore.RED}{', '.join(country['timezones'])}{Style.RESET_ALL}")
        click.echo(f"Currency: {Fore.GREEN}{country['currency']}{Style.RESET_ALL}")
    else:
        fail_message(f"Country {country_code_or_name} not found.")


@cli.command()
def export():
    """List all countries and optionally export to a file in TXT or JSON format."""
    loading_animation()
    country_data = CountryData()


    countries = country_data.get_all_countries()
    success_message("Countries loaded:")


    for country in countries:
        click.echo(Fore.CYAN + country + Style.RESET_ALL)


    if click.confirm("Do you want to export the list to a file? (Press Enter for Yes)", default=True):
        click.echo(Fore.YELLOW + "Note: Default export format is TXT." + Style.RESET_ALL)

        format_choice = click.prompt("Choose the export format (txt, json)", type=str, default="txt").strip().lower()

        if format_choice not in ["txt", "json"]:
            click.echo(Fore.RED + "Invalid format choice. Defaulting to 'txt'." + Style.RESET_ALL)
            format_choice = "txt"

        include_codes = click.confirm("Include country codes? (Press Enter for Yes)", default=True)


        file_name = click.prompt("Enter the name for the file (without extension)", type=str)


        file_extension = '.txt' if format_choice == 'txt' else '.json'
        if not file_name.lower().endswith(file_extension):
            file_name += file_extension
            click.echo(
                Fore.YELLOW + f"File name updated to {file_name} (defaulting to {file_extension})." + Style.RESET_ALL)


        file_path = os.path.join(os.getcwd(), file_name)

        if os.path.exists(file_path):
            if (file_path.lower().endswith('.txt') and format_choice != 'txt') or (
                    file_path.lower().endswith('.json') and format_choice != 'json'):
                click.echo(
                    Fore.RED + f"Error: File extension and format choice mismatch. File: {file_path}, Chosen format: {format_choice}" + Style.RESET_ALL)
                if not click.confirm("Do you want to overwrite it with the new format?", default=False):
                    click.echo(Fore.YELLOW + "File export aborted." + Style.RESET_ALL)
                    return

            click.echo(
                Fore.YELLOW + f"Warning: The file '{file_path}' already exists. It will be overwritten." + Style.RESET_ALL)

        try:
            with open(file_path, 'w') as file:
                if format_choice == "txt":
                    for country in countries:
                        try:
                            country_info = country_data.get_country_info_by_name(country)
                            if include_codes:
                                code = country_info.get('iso_code', 'Data unavailable')
                                file.write(f"{country} ({code})\n")
                            else:
                                file.write(f"{country}\n")
                        except KeyError:
                            click.echo(
                                Fore.RED + f"Warning: Country data for {country} could not be fetched." + Style.RESET_ALL)
                            if include_codes:
                                file.write(f"{country} (Data unavailable)\n")
                            else:
                                file.write(f"{country}\n")
                elif format_choice == "json":
                    data = {
                        "countries": [
                            {
                                "name": country,
                                "code": country_data.get_country_info_by_name(country).get('iso_code',
                                                                                           None) if include_codes else None
                            }
                            for country in countries
                        ]
                    }
                    json.dump(data, file, indent=4)

            click.echo(Fore.GREEN + f"Countries exported successfully to {file_path}" + Style.RESET_ALL)
        except Exception as e:
            click.echo(Fore.RED + f"Failed to write to file: {e}" + Style.RESET_ALL)
    else:
        click.echo(Fore.YELLOW + "No file exported." + Style.RESET_ALL)


@cli.command()
@click.option('--commands', is_flag=True, help="List all available fields for the specified country.")
@click.argument('country_code_or_name', required=False)
@click.argument('field', required=False)
def search(commands, country_code_or_name, field):
    """Search and display specific data about a country."""
    if commands:
        if not country_code_or_name:
            fail_message("Please provide a country name or ISO code to see available fields.")
            return


        country_data = CountryData()
        country = country_data.get_country_info(country_code_or_name.upper()) or country_data.get_country_info_by_name(country_code_or_name)
        loading_animation()

        if country:
            success_message(f"Available fields for {country['name']}:")
            for key in country.keys():
                click.echo(f"- {key}")
        else:
            fail_message(f"Country {country_code_or_name} not found.")
        return

    if not country_code_or_name or not field:
        fail_message("Please provide both a country name or ISO code and a field to search for. Use '--commands' to see available fields.")
        return

    country_data = CountryData()
    country = country_data.get_country_info(country_code_or_name.upper()) or country_data.get_country_info_by_name(country_code_or_name)
    loading_animation()

    if country:
        if field in country:
            result = country[field]
            success_message(f"Data for {field} in {country['name']}:")

            if isinstance(result, (list, tuple)):
                for item in result:
                    click.echo(Fore.CYAN + str(item) + Style.RESET_ALL)
            elif isinstance(result, dict):
                for key, value in result.items():
                    click.echo(Fore.CYAN + f"{key}: {value}" + Style.RESET_ALL)
            else:
                click.echo(Fore.CYAN + str(result) + Style.RESET_ALL)
        else:
            fail_message(f"Field '{field}' not found in {country['name']}. Use '--commands' to see available fields.")
    else:
        fail_message(f"Country {country_code_or_name} not found.")

if __name__ == '__main__':
    cli()
