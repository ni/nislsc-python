"""Demonstrate how to verify the battery health of the SLSC system."""

import click

from nislsc import Session
from nislsc.constants import ReservationAccess


@click.command()
@click.argument("chassis-name", type=str)
def main(chassis_name: str) -> None:
    """Check chassis battery.

    Connects to the specified SLSC chassis, retrieves its battery status,
    and displays the health information.

    CHASSIS_NAME is the name of the SLSC chassis to query.

    \b
    Examples:
        "check_chassis_battery SLSC-12001-XXXXXXXX"
    """  # NOQA: D301
    try:
        physical_channel_names = f"{chassis_name}/BatteryVoltageSensor"
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
            needs_replacement = sensor_reading < sensor_lower_critical

            print(f"Battery health state: {health_state}")
            print(f"Sensor reading: {sensor_reading} V")
            print(f"Battery needs replacement?: {needs_replacement}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
