import os

import click

from t8_client import get_data
from t8_client.util.csv import save_array_to_csv


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
    filename = f"wave_{machine}_{point}_{pmode}_{time}.csv"
    file_path = os.path.join("output", filename)
    save_array_to_csv(file_path, waveform, "Samples")


@cli.command(
    name="get-spectrum",
    help="Get the spectrum data for a given machine, point, processing mode, and time.",
)
@pmode_params
@click.option("-t", "--time", required=True, help="Time of the spectrum")
@click.pass_context
def get_spectrum(ctx, machine, point, pmode, time):
    spectrum = get_data.get_spectrum(
        host=ctx.obj["HOST"],
        id=ctx.obj["ID"],
        machine=machine,
        point=point,
        pmode=pmode,
        time=time,
        t8_user=ctx.obj["T8_USER"],
        t8_password=ctx.obj["T8_PASSWORD"],
    )[0]

    # Print the spectrum data
    for sample in spectrum:
        print(sample)

    # Save the spectrum data to a CSV file
    filename = f"spectrum_{machine}_{point}_{pmode}_{time}.csv"
    file_path = os.path.join("output", filename)
    save_array_to_csv(file_path, spectrum, "Samples")


if __name__ == "__main__":
    cli()
