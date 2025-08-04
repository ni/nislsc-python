"""Demonstrate how to query and display the command and property tree.

It connects to the specified SLSC device, retrieves its available
commands, properties, and physical channels, and organizes this
information into a structured JSON format. The module supports querying
both device-level and physical channel-level commands and properties.
"""

import json

import click

from example_helper import _get_session_generic_property
from nislsc import Command, Property, Session
from nislsc.constants import (
    DataType,
    PropertyAccess,
    ReservationAccess,
)


def show_command_and_property_tree(device_names: str) -> str:
    """Show the command and property tree of the NISLSC library."""
    connection_timeout = 10.0
    reservation_access = 1
    reservation_group = "admin"
    reservation_timeout = 10.0

    with Session.initialize_session_with_devices(
        None,
        device_names,
        connection_timeout,
        reservation_access,
        reservation_group,
        reservation_timeout,
    ) as session:

        data = {
            "Name": device_names,
            "Commands": [],
            "Properties": [],
        }

        device_commands = session.get_device_property_string_array(device_names, "Dev.Commands")

        device_properties = session.get_device_property_string_array(device_names, "Dev.Properties")

        device_physical_channels = session.get_device_property_string_array(
            device_names, "Dev.PhysChans"
        )

        for physical_channel in device_physical_channels:
            data[physical_channel] = {"Commands": [], "Properties": []}

        for device_command in device_commands:
            with Command.open_device_command(session, device_names, device_command) as command:
                name = device_command
                description = command.get_command_property_string("Cmd.Descr")
                access = ReservationAccess(command.get_command_property_int32("Cmd.Access"))
                data["Commands"].append(
                    {"name": name, "description": description, "access": access.name}
                )

        for device_property in device_properties:
            with Property.open_device_property(session, device_names, device_property) as property:
                name = device_property

                datatype = DataType(property.get_property_property_int32("Prop.DataType"))

                current_value = _get_session_generic_property(
                    session, device_names, device_property, datatype
                )

                access = PropertyAccess(property.get_property_property_int32("Prop.Access"))

                description = property.get_property_property_string("Prop.Descr")

                documentation = property.get_property_property_string("Prop.Doc")

                min_value = property.get_property_property_string("Prop.MinValue")
                max_value = property.get_property_property_string("Prop.MaxValue")

                if len(min_value) == 0 and len(max_value) == 0:
                    range_value = ""
                else:
                    range_value = f"[{min_value}, {max_value}]"

                data["Properties"].append(
                    {
                        "name": name,
                        "current_value": current_value,
                        "datatype": datatype.name,
                        "range": range_value,
                        "access": access.name,
                        "description": description,
                        "documentation": documentation,
                    }
                )

        for physical_channel in device_physical_channels:

            physical_channel_commands = session.get_physical_channel_property_string_array(
                physical_channel, "PhysChan.Commands"
            )
            physical_channel_properties = session.get_physical_channel_property_string_array(
                physical_channel, "PhysChan.Properties"
            )

            for physical_channel_command in physical_channel_commands:
                with Command.open_physical_channel_command(
                    session, physical_channel, physical_channel_command
                ) as command:
                    name = physical_channel_command
                    description = command.get_command_property_string("Cmd.Descr")
                    access = ReservationAccess(command.get_command_property_int32("Cmd.Access"))
                    data[physical_channel]["Commands"].append(
                        {"name": name, "description": description, "access": access.name}
                    )

            for physical_channel_property in physical_channel_properties:
                with Property.open_physical_channel_property(
                    session, physical_channel, physical_channel_property
                ) as property:
                    name = physical_channel_property
                    datatype = DataType(property.get_property_property_int32("Prop.DataType"))

                    current_value = _get_session_generic_property(
                        session, physical_channel, physical_channel_property, datatype
                    )

                    access = PropertyAccess(property.get_property_property_int32("Prop.Access"))

                    description = property.get_property_property_string("Prop.Descr")

                    documentation = property.get_property_property_string("Prop.Doc")

                    min_value = property.get_property_property_string("Prop.MinValue")
                    max_value = property.get_property_property_string("Prop.MaxValue")

                    if len(min_value) == 0 and len(max_value) == 0:
                        range_value = ""
                    else:
                        range_value = f"[{min_value}, {max_value}]"

                    data[physical_channel]["Properties"].append(
                        {
                            "name": name,
                            "current_value": current_value,
                            "datatype": datatype.name,
                            "range": range_value,
                            "access": access.name,
                            "description": description,
                            "documentation": documentation,
                        }
                    )

        complete_data = json.dumps(data, indent=4)
        return complete_data


@click.command()
@click.argument("device_names", type=str)
def main(device_names: str) -> None:
    r"""Create a command and property tree.

    DEVICE_NAMES: Name of the SLSC device to query.

    \b
    Examples:
        "SLSC-12001-03146D67"
        "SLSC-12001-03146D67-Mod1"
        "SLSC-12001-03146D67-Mod2"
    """
    try:
        data = show_command_and_property_tree(device_names)
        print(data)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
