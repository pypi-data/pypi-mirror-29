import click
from pathlib import Path

from recodex.api import ApiClient
from recodex.config import UserContext
from recodex.decorators import pass_data_dir


@click.command()
@click.argument("api_url")
@pass_data_dir
def login(data_dir: Path, api_url):
    """
    Log in using a ReCodEx account
    """

    username = click.prompt("User name")
    password = click.prompt("Password", hide_input=True)

    api = ApiClient(api_url)
    api_login_response = api.login(username, password)

    api_token = api_login_response["accessToken"]
    UserContext(api_url, api_token).store(data_dir / "context.yaml")
