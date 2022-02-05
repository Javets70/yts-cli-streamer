import typer
from scraper import ytscraper

app = typer.Typer()


@app.command()
def search(name: str = typer.Argument(..., metavar="💫NAME OF THE MOVIE💫"),
           action: str = typer.Option(
               "s", help="The actions can be s(stream) or d(download) or u(get link)"),
           player: str = typer.Option("mpv", help="Enter any player supported by webtorrent-cli")):
    start = ytscraper(name)
    start.get_movies()
    start.player_is(player)
    start.action_is(action)
    start.select_quality()


if __name__ == '__main__':
    app()
