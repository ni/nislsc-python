"""Demonstrate how to reset a SLSC module."""

import click

from nislsc import Session


@click.command()
@click.argument("device-names", type=str)
def main(device_names: str) -> None:
    """Reset the specified SLSC devices/chassis.

    Providing a chassis name will reset all the modules, but not reboot the chassis.

    DEVICE_NAMES is a comma-separated list of SLSC devices/chassis to reset.

    \b
    Examples:
        reset_device SLSC-12001-XXXXXXXX
        reset_device SLSC-12001-XXXXXXXX-Mod1
        reset_device SLSC-12001-XXXXXXXX-Mod1,SLSC-12001-XXXXXXXX-Mod2
    """  # noqa: D301
    try:
        with Session.initialize_session_with_devices(
            device_names=device_names,
        ) as session:
            session.reset_devices()
            print(f"Reset command sent to device(s) {device_names}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
