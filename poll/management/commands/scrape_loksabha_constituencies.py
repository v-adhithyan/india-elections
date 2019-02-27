import csv
import json
from pathlib import Path
from urllib.request import urlopen

import yaml
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from indiaelections.settings import PROJECT_ROOT

WIKIPEDIA_LOKSABHA_CONSTITUENCIES_LIST_URL = "https://en.wikipedia.org/wiki/List_of_constituencies_of_the_Lok_Sabha"
DATA_DIR = Path(PROJECT_ROOT).parents[0] / "data"
STATES = 29
UNION_TERRITORIES = 7
STATES_AND_UNION_TERRITORIES = STATES + UNION_TERRITORIES

filename = "loksabha_constituencies_list.{}"


def write_json(data):
    with open(DATA_DIR / filename.format("json"), "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)


def write_csv(data):
    header = ["State/Union Territory", "Constituency Name"]
    with open(DATA_DIR / filename.format("csv"), "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows([state_union, constituency] for state_union, constituencies in data.items()
                         for constituency in constituencies)


def write_yaml(data):
    with open(DATA_DIR / filename.format("yaml"), "w") as yamlfile:
        yaml.dump(data, yamlfile)


def write_output(data, output_format):
    if output_format == "json":
        write_json(data)
    elif output_format == "csv":
        write_csv(data)
    elif output_format == "yaml":
        write_yaml(data)
    else:
        print("Unsupported output format.")


class Command(BaseCommand):
    help = "Scrape constituencies list from wikipedia and write them to a file."

    def add_arguments(self, parser):
        parser.add_argument("output_format", type=str)

    def handle(self, *args, **kwargs):
        output_format = kwargs.get("output_format", None)
        data = urlopen(WIKIPEDIA_LOKSABHA_CONSTITUENCIES_LIST_URL).read()
        soup = BeautifulSoup(data, features='html.parser')

        table_rows = soup.find_all("tr")

        # Get all table rows from the page
        # the first table in the page contains list of states and their corresponding number of loksabha seats
        # the rest of the tables contain loksabha constituencies list of
        # first row of table (index 0) is header, skip that
        # total 29 states and 7 union territories so from second row (index 1),
        # iterate till 29 + 7 (add extra one to consider last one)
        states_and_union_territories = table_rows[1:STATES_AND_UNION_TERRITORIES+1]
        state_and_union_seat_count = dict()
        for s in states_and_union_territories:
            place, no_of_seats = s.text.strip().split("\n")
            state_and_union_seat_count[place] = int(no_of_seats)

        start = STATES_AND_UNION_TERRITORIES + 2  # skip first and second table header
        data = dict()

        for s, total_seats in state_and_union_seat_count.items():
            end = start + total_seats
            s_data = table_rows[start:end]
            data[s] = list()
            for d in s_data:
                constituency_name, is_reserved = d.text.strip().split("\n")[1:]
                data[s].append(constituency_name)
            assert len(data[s]) == total_seats
            start = end + 1

        if output_format:
            write_output(data, output_format)
