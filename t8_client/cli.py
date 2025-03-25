"""Command line interface for the T8 client."""

# ruff: noqa: ANN001
# ruff: noqa: ANN201
# ruff: noqa: ARG001
# ruff: noqa: D103

import os

import click
import numpy as np

from t8_client import get_data, url_params
from t8_client.util.csv import save_array_to_csv
from t8_client.util.plots import plot_spectrum, plot_waveform


@click.group(context_settings={"auto_envvar_prefix": "T8_CLIENT"})
@click.option("-H", "--host", required=True, help="Host URL")
@click.option("-i", "--id", required=True, help="ID for the endpoint")
@click.option("-u", "--user", required=True, help="Username for authentication")
@click.option("-P", "--password", required=True, help="Password for authentication")
@click.pass_context
def cli(ctx, host, id, user, password):
    ctx.ensure_object(dict)
    ctx.obj["host"] = host
    ctx.obj["id"] = id
    ctx.obj["user"] = user
    ctx.obj["password"] = password


def pmode_params(func):
    func = click.option("-M", "--machine", help="Machine tag")(func)
    func = click.option(
        "-p", "--point", help="Point tag or combined tag in the format M1:P1:PM1"
    )(func)
    return click.option("-m", "--pmode", help="Processing mode tag")(func)


def parse_combined_tag(point: str) -> tuple[str, str, str]:
    """Parses a combined tag string into its components: machine, point, and pmode.

    The input string must be in the format 'M1:P1:PM1', where:
    - 'M1' represents the machine identifier.
    - 'P1' represents the point identifier.
    - 'PM1' represents the mode identifier.

    Args:
        point (str): The combined tag string to parse. It must contain exactly two
            colons (':').

    Returns:
        tuple[str, str, str]: A tuple containing the machine, point, and pmode
            components.

    Raises:
        ValueError: If the input string does not contain exactly two colons or is not in
            the correct format.

    """
    if point and ":" in point:
        parts = point.split(":")
        if len(parts) == 3:  # noqa: PLR2004
            machine, point, pmode = parts
            return machine, point, pmode
        error_message = "Point must be in the format 'M1:P1:PM1'"
        raise ValueError(error_message)
    error_message = "Point must contain ':' and be in the format 'M1:P1:PM1'"
    raise ValueError(error_message)


@cli.command(
    name="list-waves",
    help="List all the waves for a given machine, point, and processing mode as a"
    + " list of dates.",
)
@pmode_params
@click.pass_context
def list_waves(ctx, machine, point, pmode):
    if point and ":" in point:
        machine, point, pmode = parse_combined_tag(point)

    params = url_params.PmodeParams(
        host=ctx.obj["host"],
        id_=ctx.obj["id"],
        user=ctx.obj["user"],
        password=ctx.obj["password"],
        machine=machine,
        point=point,
        pmode=pmode,
    )

    for wave in get_data.get_wave_list(
        params=params,
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
        machine, point, pmode = parse_combined_tag(point)

    params = url_params.PmodeParams(
        host=ctx.obj["host"],
        id_=ctx.obj["id"],
        user=ctx.obj["user"],
        password=ctx.obj["password"],
        machine=machine,
        point=point,
        pmode=pmode,
    )

    for spectra in get_data.get_spectra(params):
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
        machine, point, pmode = parse_combined_tag(point)

    params = url_params.PmodeTimeParams(
        host=ctx.obj["host"],
        id_=ctx.obj["id"],
        user=ctx.obj["user"],
        password=ctx.obj["password"],
        machine=machine,
        point=point,
        pmode=pmode,
        time=time,
    )

    waveform, _ = get_data.get_wave(params)

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
        machine, point, pmode = parse_combined_tag(point)

    params = url_params.PmodeTimeParams(
        host=ctx.obj["host"],
        id_=ctx.obj["id"],
        user=ctx.obj["user"],
        password=ctx.obj["password"],
        machine=machine,
        point=point,
        pmode=pmode,
        time=time,
    )

    spectrum = get_data.get_spectrum(params)[0]

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
        machine, point, pmode = parse_combined_tag(point)

    params = url_params.PmodeTimeParams(
        host=ctx.obj["host"],
        id_=ctx.obj["id"],
        user=ctx.obj["user"],
        password=ctx.obj["password"],
        machine=machine,
        point=point,
        pmode=pmode,
        time=time,
    )

    waveform, sample_rate = get_data.get_wave(params)

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
        machine, point, pmode = parse_combined_tag(point)

    params = url_params.PmodeTimeParams(
        host=ctx.obj["host"],
        id_=ctx.obj["id"],
        user=ctx.obj["user"],
        password=ctx.obj["password"],
        machine=machine,
        point=point,
        pmode=pmode,
        time=time,
    )

    spectrum, fmin, fmax = get_data.get_spectrum(params)

    freqs = np.linspace(fmin, fmax, len(spectrum))

    plot_spectrum(spectrum, freqs, 0, 500)
