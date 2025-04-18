import os

import click
import numpy as np

from t8_client import get_data
from t8_client.util.csv import save_array_to_csv
from t8_client.util.plots import plot_spectrum, plot_waveform


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj["HOST"] = os.getenv("HOST")
    ctx.obj["ID"] = os.getenv("ID")
    ctx.obj["T8_USER"] = os.getenv("T8_USER")
    ctx.obj["T8_PASSWORD"] = os.getenv("T8_PASSWORD")


def pmode_params(func):
    func = click.option("-M", "--machine", help="Machine tag")(func)
    func = click.option(
        "-p", "--point", help="Point tag or combined tag in the format M1:P1:PM1"
    )(func)
    func = click.option("-m", "--pmode", help="Processing mode tag")(func)
    return func


def parse_combined_tag(ctx, param, value):
    if value and ":" in value:
        machine, point, pmode = value.split(":")
        ctx.params["machine"] = machine
        ctx.params["point"] = point
        ctx.params["pmode"] = pmode
    return value


@cli.command(
    name="list-waves",
    help="List all the waves for a given machine, point, and processing mode as a"
    + " list of dates.",
)
@pmode_params
@click.pass_context
def list_waves(ctx, machine, point, pmode):
    if point and ":" in point:
        parse_combined_tag(ctx, None, point)
    for wave in get_data.get_wave_list(
        host=ctx.obj["HOST"],
        id=ctx.obj["ID"],
        machine=ctx.params["machine"],
        point=ctx.params["point"],
        pmode=ctx.params["pmode"],
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
    if point and ":" in point:
        parse_combined_tag(ctx, None, point)
    for spectra in get_data.get_spectra(
        host=ctx.obj["HOST"],
        id=ctx.obj["ID"],
        machine=ctx.params["machine"],
        point=ctx.params["point"],
        pmode=ctx.params["pmode"],
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
    if point and ":" in point:
        parse_combined_tag(ctx, None, point)
    waveform, _ = get_data.get_wave(
        host=ctx.obj["HOST"],
        id=ctx.obj["ID"],
        machine=ctx.params["machine"],
        point=ctx.params["point"],
        pmode=ctx.params["pmode"],
        time=time,
        t8_user=ctx.obj["T8_USER"],
        t8_password=ctx.obj["T8_PASSWORD"],
    )

    # Print the waveform data
    for sample in waveform:
        print(sample)

    # Save the waveform data to a CSV file
    filename = (
        f"wave_{ctx.params['machine']}_{ctx.params['point']}_"
        + f"{ctx.params['pmode']}_{time}.csv"
    )
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
    if point and ":" in point:
        parse_combined_tag(ctx, None, point)
    spectrum = get_data.get_spectrum(
        host=ctx.obj["HOST"],
        id=ctx.obj["ID"],
        machine=ctx.params["machine"],
        point=ctx.params["point"],
        pmode=ctx.params["pmode"],
        time=time,
        t8_user=ctx.obj["T8_USER"],
        t8_password=ctx.obj["T8_PASSWORD"],
    )[0]

    # Print the spectrum data
    for sample in spectrum:
        print(sample)

    # Save the spectrum data to a CSV file
    filename = (
        f"spectrum_{ctx.params['machine']}_{ctx.params['point']}_"
        + f"{ctx.params['pmode']}_{time}.csv"
    )
    file_path = os.path.join("output", filename)
    save_array_to_csv(file_path, spectrum, "Samples")


@cli.command(
    name="plot-wave",
    help="Plot the wave data for a given machine, point, processing mode, and time.",
)
@click.option("-t", "--time", required=True, help="Time of the wave")
@pmode_params
@click.pass_context
def plot_wave(ctx, machine, point, pmode, time):
    if point and ":" in point:
        parse_combined_tag(ctx, None, point)
    waveform, sample_rate = get_data.get_wave(
        host=ctx.obj["HOST"],
        id=ctx.obj["ID"],
        machine=ctx.params["machine"],
        point=ctx.params["point"],
        pmode=ctx.params["pmode"],
        time=time,
        t8_user=ctx.obj["T8_USER"],
        t8_password=ctx.obj["T8_PASSWORD"],
    )

    plot_waveform(waveform, sample_rate)


@cli.command(
    name="plot-spectrum",
    help="Plot the spectrum data for a given machine, point, processing mode, and"
    + " time.",
)
@click.option("-t", "--time", required=True, help="Time of the spectrum")
@pmode_params
@click.pass_context
def plot_spectrum_cmd(ctx, machine, point, pmode, time):
    if point and ":" in point:
        parse_combined_tag(ctx, None, point)
    spectrum, fmin, fmax = get_data.get_spectrum(
        host=ctx.obj["HOST"],
        id=ctx.obj["ID"],
        machine=ctx.params["machine"],
        point=ctx.params["point"],
        pmode=ctx.params["pmode"],
        time=time,
        t8_user=ctx.obj["T8_USER"],
        t8_password=ctx.obj["T8_PASSWORD"],
    )

    freqs = np.linspace(fmin, fmax, len(spectrum))

    plot_spectrum(spectrum, freqs, 0, 500)


if __name__ == "__main__":
    cli()
