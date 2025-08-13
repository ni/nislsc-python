"""Demonstrate how to reset a SLSC module.

Selecting a chassis will reset all the modules, not reboot the chassis.
"""

import click

from nislsc import Session
from nislsc.constants import ReservationAccess


@click.command()
@click.argument("device_names", type=str)
def main(device_names: str) -> None:
    """Reset the specified SLSC devices/chassis.

    device_names: Comma-separated list of SLSC devices/chassis to reset.

    Examples:
        "SLSC-12001-03146D67"
        "SLSC-12001-03146D67-Mod1"
        "SLSC-12001-03146D67-Mod1,SLSC-12001-03146D67-Mod2"
    """
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
        click.echo(f"Input Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
