from rich.console import Console
from rich.table import Table
import requests
import json
import sys
import subprocess as sp

console = Console()


class ytscraper:
    def __init__(self, query):
        self.query = query
        self.movies = {}

### --- Initializing the console and the table --- ###

        self.console = Console()
        self.movie_table = Table(title="LIST OF MOVIES", style="bold")
        self.movie_table.add_column("[green]ID", style="cyan")
        self.movie_table.add_column("[cyan]TITLE", style="green")

    def get_movies(self):  # Gets max 50 movies related to the query term
        self.payload = {"limit": 50, "query_term": self.query}
        self.r = requests.get(
            "https://yts.mx/api/v2/list_movies.json", params=self.payload)
        try:
            self.content = json.loads(self.r.content)["data"]["movies"]
        except KeyError:
            self.console.print("NO RESULTS FOUND", style="bold red")
            sys.exit()

### --- Prints the Table --- ###

        for i in range(len(self.content)):
            self.movies[i] = [self.content[i]
                              ["title_english"], self.content[i]["torrents"]]
            self.movie_table.add_row(str(i), str(
                self.content[i]["title_english"]))
        self.console.print(self.movie_table)

### --- Select the Movie ---###
        self.id = int(console.input("[bold]ENTER ID : "))
        if self.id not in self.movies:
            self.console.print("INVALID ID", style="bold red")
            sys.exit()

    def action_is(self, action):
        self.action = action

    def player_is(self, player):
        self.player = player

    def select_quality(self):
        self.quality_data = {}

### --- prints the quality table ---###

        self.quality_table = Table()
        self.quality_table.add_column("INDEX", style="white")
        self.quality_table.add_column("QUALITY", style="cyan")
        self.quality_table.add_column("TYPE", style="magenta")
        self.quality_table.add_column("SEEDS", style="green")
        self.quality_table.add_column("PEERS", style="yellow")
        self.quality_table.add_column("SIZE", style="purple")

        for i in range(len(self.movies[self.id][1])):
            self.url_dict = self.movies[self.id][1][i]
            self.quality_table.add_row(str(i),
                                       str(self.url_dict["quality"]),
                                       str(self.url_dict["type"]),
                                       str(self.url_dict["seeds"]),
                                       str(self.url_dict["peers"]),
                                       str(self.url_dict["size"]))

            self.quality_data[i] = self.url_dict["hash"]
        self.console.print(self.quality_table)

###--- Gets the index of the quality ---###
        try:
            self.index = int(self.console.input("[bold]ENTER INDEX: "))
        except ValueError:
            self.console.print("INVALID INPUT", style="bold red")
            sys.exit()
        if self.index not in self.quality_data:
            self.console.print("INVALID INDEX", style="bold red")
            sys.exit()
        else:
            if self.action == "d":
                sp.run(
                    f"webtorrent download https://yts.mx/torrent/download/{self.quality_data[self.index]}".split(), text=True)
            elif self.action == "s":
                sp.run(
                    f"webtorrent download https://yts.mx/torrent/download/{self.quality_data[self.index]} --{self.player}".split(), text=True)
            elif self.action == "u":
                self.console.print(
                    f"https://yts.mx/torrent/download/{self.quality_data[self.index]}", style="bold")
            else:
                self.console.print("INVALID ACTION", style="bold red")
                sys.exit()
