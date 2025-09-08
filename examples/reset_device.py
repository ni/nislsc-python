"""Demonstrate how to reset a SLSC module."""

import click

from nislsc import Session
from nislsc.constants import ReservationAccess


@click.command()
@click.argument("device-names", type=str)
def main(device_names: str) -> None:
    """Reset the specified SLSC devices/chassis.

    Providing a chassis name will reset all the modules, but not reboot the chassis.

    DEVICE_NAMES is a comma-separated list of SLSC devices/chassis to reset.

    \b
    Examples:
        "reset_device SLSC-12001-XXXXXXXX"
        "reset_device SLSC-12001-XXXXXXXX-Mod1"
        "reset_device SLSC-12001-XXXXXXXX-Mod1,SLSC-12001-XXXXXXXX-Mod2"
    """  # NOQA: D301
    try:
        connection_timeout = 10.0
        reservation_access = ReservationAccess.READ_ONLY
        reservation_group = "admin"
        reservation_timeout = 10.0

        with Session.initialize_session_with_devices(
            None,
            device_names=device_names,
            connection_timeout=connection_timeout,
            reservation_access=reservation_access,
            reservation_group=reservation_group,
            reservation_timeout=reservation_timeout,
        ) as session:
            session.reset_devices(device_names)
            print(f"Reset command sent to device(s) {device_names}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
