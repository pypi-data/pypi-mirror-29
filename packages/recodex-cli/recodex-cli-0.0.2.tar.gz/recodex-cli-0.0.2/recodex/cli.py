import json
from pprint import pprint

import appdirs
import click
import pkg_resources
import sys
from pathlib import Path

from recodex.api import ApiClient
from recodex.config import UserContext
from recodex.decorators import pass_api_client, pass_data_dir, ReCodExContext


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    """
    ReCodEx CLI
    """

    config_dir = Path(appdirs.user_config_dir("recodex"))
    data_dir = Path(appdirs.user_data_dir("recodex"))

    context_path = data_dir / "context.yaml"
    user_context = UserContext.load(context_path) if context_path.exists() else UserContext()

    ctx.obj = ReCodExContext(
        ApiClient(user_context.api_url, user_context.api_token),
        config_dir,
        data_dir
    )


for entry_point in pkg_resources.iter_entry_points("recodex"):
    plugin = entry_point.load()
    plugin.name = entry_point.name
    cli.add_command(plugin)


@cli.command()
@click.argument("api_url")
@pass_data_dir
def init(data_dir: Path, api_url):
    """
    Set up the CLI with a token that you already own
    """

    api_token = click.prompt("API token")
    api = ApiClient(api_url, api_token)

    try:
        api.get_status()
    except:
        click.echo("API connection test failed", err=True)
        raise

    context = UserContext(api_url, api_token)

    data_dir.mkdir(parents=True, exist_ok=True)
    context.store(data_dir / "context.yaml")


@cli.command()
@click.argument("method")
@click.argument("path")
@pass_api_client
def call(api: ApiClient, method, path):
    """
    Perform an API call directly
    """

    method = method.lower()
    data = {}

    if method in ("post", "put"):
        data = json.loads(sys.stdin.read())

    pprint(api.extract_payload(api.call(method, path, data=data)))


if __name__ == "__main__":
    cli()
