"""Demonstrate how to query and display the command and property tree."""

import json
from typing import Any

import click

from nislsc import Command, Property, Session
from nislsc.constants import (
    CommandProperty,
    DataType,
    DeviceProperty,
    PhysicalChannelProperty,
    PropertyAccess,
    PropertyProperty,
    ReservationAccess,
)


def _get_session_generic_property(
    session: Session, resource: str, property: str, datatype: DataType
) -> Any:
    """Retrieve the current value of a property based on its data type.

    Args:
        session: SLSC session instance.
        resource: Device or physical channel name.
        property: Property name to retrieve.
        datatype: DataType enum indicating the property's data type.

    Returns:
        Property value in its native type, or "Unsupported DataType" if
            invalid.
    """
    if datatype == DataType.NONE:
        raise ValueError(f"Invalid data type: {datatype}")
    else:
        method_name = f"get_generic_property_{datatype.name.lower()}"
        method = getattr(session, method_name)
        return method(resource, property)


def get_command_and_property_tree(device_name: str) -> dict:
    """Show the command and property tree of the NISLSC library.

    Args:
        device_name: Name of the SLSC device to query.

    Returns:
        Dictionary containing the command and property tree of the device.
    """
    connection_timeout = 10.0
    reservation_access = ReservationAccess.READ_ONLY
    reservation_group = "admin"
    reservation_timeout = 10.0

    with Session.initialize_session_with_devices(
        None,
        device_name,
        connection_timeout,
        reservation_access,
        reservation_group,
        reservation_timeout,
    ) as session:

        data = {
            "Name": device_name,
            "Commands": [],
            "Properties": [],
        }

        device_commands = session.get_device_property_string_array(
            device_name,
            DeviceProperty.COMMANDS,
        )

        device_properties = session.get_device_property_string_array(
            device_name,
            DeviceProperty.PROPERTIES,
        )

        device_physical_channels = session.get_device_property_string_array(
            device_name,
            DeviceProperty.PHYSICAL_CHANNELS,
        )

        for physical_channel in device_physical_channels:
            data[physical_channel] = {"Commands": [], "Properties": []}

        for device_command in device_commands:
            with Command.open_device_command(session, device_name, device_command) as command:
                name = device_command
                description = command.get_command_property_string(CommandProperty.DESCRIPTION)
                data["Commands"].append({"name": name, "description": description})

        for device_property in device_properties:
            with Property.open_device_property(session, device_name, device_property) as property:
                name = device_property

                datatype = DataType(
                    property.get_property_property_int32(PropertyProperty.DATA_TYPE)
                )

                current_value = _get_session_generic_property(
                    session, device_name, device_property, datatype
                )

                access = PropertyAccess(
                    property.get_property_property_int32(PropertyProperty.ACCESS)
                )

                description = property.get_property_property_string(PropertyProperty.DESCRIPTION)

                documentation = property.get_property_property_string(
                    PropertyProperty.DOCUMENTATION
                )

                min_value = property.get_property_property_string(PropertyProperty.MINIMUM_VALUE)
                max_value = property.get_property_property_string(PropertyProperty.MAXIMUM_VALUE)

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
                physical_channel, PhysicalChannelProperty.COMMANDS
            )
            physical_channel_properties = session.get_physical_channel_property_string_array(
                physical_channel, PhysicalChannelProperty.PROPERTIES
            )

            for physical_channel_command in physical_channel_commands:
                with Command.open_physical_channel_command(
                    session, physical_channel, physical_channel_command
                ) as command:
                    name = physical_channel_command
                    description = command.get_command_property_string(CommandProperty.DESCRIPTION)
                    data[physical_channel]["Commands"].append(
                        {"name": name, "description": description}
                    )

            for physical_channel_property in physical_channel_properties:
                with Property.open_physical_channel_property(
                    session, physical_channel, physical_channel_property
                ) as property:
                    name = physical_channel_property
                    datatype = DataType(
                        property.get_property_property_int32(PropertyProperty.DATA_TYPE)
                    )

                    current_value = _get_session_generic_property(
                        session, physical_channel, physical_channel_property, datatype
                    )

                    access = PropertyAccess(
                        property.get_property_property_int32(PropertyProperty.ACCESS)
                    )

                    description = property.get_property_property_string(
                        PropertyProperty.DESCRIPTION
                    )

                    documentation = property.get_property_property_string(
                        PropertyProperty.DOCUMENTATION
                    )

                    min_value = property.get_property_property_string(
                        PropertyProperty.MINIMUM_VALUE
                    )
                    max_value = property.get_property_property_string(
                        PropertyProperty.MAXIMUM_VALUE
                    )

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

        return data


@click.command()
@click.argument("device-name", type=str)
def main(device_name: str) -> None:
    """Create a command and property tree.

    Connects to the specified SLSC device, retrieves its available
    commands, properties, and physical channels, and organizes this
    information into a structured JSON format.

    The module supports querying both device-level and physical
    channel-level commands and properties.

    DEVICE_NAME is the name of the SLSC device to query.

    \b
    Examples:
        show_command_and_property_tree SLSC-12001-XXXXXXXX
        show_command_and_property_tree SLSC-12001-XXXXXXXX-Mod1
        show_command_and_property_tree SLSC-12001-XXXXXXXX-Mod2
    """  # noqa: D301
    try:
        data = get_command_and_property_tree(device_name)
        print(json.dumps(data, indent=4))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
