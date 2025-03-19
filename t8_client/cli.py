import os

import click

from t8_client import get_data


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj["HOST"] = os.getenv("HOST")
    ctx.obj["ID"] = os.getenv("ID")
    ctx.obj["T8_USER"] = os.getenv("T8_USER")
    ctx.obj["T8_PASSWORD"] = os.getenv("T8_PASSWORD")


@cli.command(
    name="list-waves",
    help="List all the waves for a given machine, point, and processing mode as a"
    + " list of dates.",
)
@click.option("-M", "--machine", required=True, help="Machine tag")
@click.option("-p", "--point", required=True, help="Point tag")
@click.option("-m", "--pmode", required=True, help="Processing mode tag")
@click.pass_context
def list_waves(ctx, machine, point, pmode):
    for wave in get_data.get_wave_list(
        host=ctx.obj["HOST"],
        id=ctx.obj["ID"],
        machine=machine,
        point=point,
        pmode=pmode,
        t8_user=ctx.obj["T8_USER"],
        t8_password=ctx.obj["T8_PASSWORD"],
    ):
        print(wave)


if __name__ == "__main__":
    cli()
