"""Demonstrate how to verify the battery health of the SLSC system.

It connects to the specified SLSC chassis, retrieves its battery status,
and displays the health information.
"""

from typing import Any

import click
from nislsc import Session
from nislsc.constants import ReservationAccess


def get_battery_status(device_name: str) -> dict[str, Any]:
    """Retrieve the battery status of the specified SLSC chassis."""
    physical_channel_names = f"{device_name}/BatteryVoltageSensor"
    connection_timeout = 10.0
    reservation_access = ReservationAccess.READ_ONLY
    reservation_group = "admin"
    reservation_timeout = 10.0

    with Session.initialize_session_with_physical_channels(
        None,
        physical_channel_names=physical_channel_names,
        connection_timeout=connection_timeout,
        reservation_access=reservation_access,
        reservation_group=reservation_group,
        reservation_timeout=reservation_timeout,
    ) as session:
        sensor_lower_critical = session.get_physical_channel_property_double(
            physical_channel_names=physical_channel_names,
            property_name="SensorLowerCritical",
        )
        sensor_reading = session.get_physical_channel_property_double(
            physical_channel_names=physical_channel_names,
            property_name="SensorReading",
        )
        health_state = session.get_physical_channel_property_string(
            physical_channel_names=physical_channel_names,
            property_name="HealthState",
        )
    return {
        "SensorLowerCritical": sensor_lower_critical,
        "SensorReading": sensor_reading,
        "HealthState": health_state,
    }


@click.command()
@click.argument("chassis_name", type=str)
def main(chassis_name: str) -> None:
    """Check chassis battery.

    chassis_name: Name of the SLSC chassis to query.

    Examples:
        "SLSC-12001-03146D67"
    """
    try:
        battery_status = get_battery_status(chassis_name)
        needs_replacement = (
            battery_status["SensorReading"] < battery_status["SensorLowerCritical"]
        )

        print(f"Battery Health State: {battery_status['HealthState']}")
        print(f"Sensor Reading: {battery_status['SensorReading']}")
        print(f"Battery needs replacement?: {needs_replacement}")
    except Exception as e:
        click.echo(f"Input Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
