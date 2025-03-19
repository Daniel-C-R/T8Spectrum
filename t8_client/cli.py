import csv
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


def pmode_params(func):
    func = click.option("-M", "--machine", required=True, help="Machine tag")(func)
    func = click.option("-p", "--point", required=True, help="Point tag")(func)
    func = click.option("-m", "--pmode", required=True, help="Processing mode tag")(
        func
    )
    return func


@cli.command(
    name="list-waves",
    help="List all the waves for a given machine, point, and processing mode as a"
    + " list of dates.",
)
@pmode_params
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


@cli.command(
    name="list-spectra",
    help="List all the spectra for a given machine, point, and processing mode as a"
    + " list of dates.",
)
@pmode_params
@click.pass_context
def list_spectra(ctx, machine, point, pmode):
    for spectra in get_data.get_spectra(
        host=ctx.obj["HOST"],
        id=ctx.obj["ID"],
        machine=machine,
        point=point,
        pmode=pmode,
        t8_user=ctx.obj["T8_USER"],
        t8_password=ctx.obj["T8_PASSWORD"],
    ):
        print(spectra)


@cli.command(
    name="get-wave",
    help="Get the wave data for a given machine, point, processing mode, and time.",
)
@pmode_params
@click.option("-t", "--time", required=True, help="Time of the wave")
@click.pass_context
def get_wave(ctx, machine, point, pmode, time):
    waveform, _ = get_data.get_wave(
        host=ctx.obj["HOST"],
        id=ctx.obj["ID"],
        machine=machine,
        point=point,
        pmode=pmode,
        time=time,
        t8_user=ctx.obj["T8_USER"],
        t8_password=ctx.obj["T8_PASSWORD"],
    )

    # Print the waveform data
    for sample in waveform:
        print(sample)

    # Save the waveform data to a CSV file
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/wave_{machine}_{point}_{pmode}_{time}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Samples"])
        for sample in waveform:
            writer.writerow([sample])


if __name__ == "__main__":
    cli()
