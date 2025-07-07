"""Demonstrates how to query and display the command and property tree.

It connects to the specified SLSC device, retrieves its available
commands, properties, and physical channels, and organizes this
information into a structured JSON format. The module supports querying
both device-level and physical channel-level commands and properties.
"""

import json
import sys

from nislsc._nislsc import NISLSC
from nislsc.constants import (
    DataType,
    PropertyAccess,
    ReservationAccess,
)


def show_command_and_property_tree(device_names: str) -> dict:
    """Show the command and property tree of the NISLSC library."""
    with NISLSC() as nislsc:
        with nislsc.initialize_library() as lib:

            connection_timeout = 10.0
            reservation_access = 1
            reservation_group = "admin"
            reservation_timeout = 10.0

            data = {
                "name": device_names,
                "Commands": [],
                "Properties": [],
            }

            with lib.initialize_session_with_devices(
                device_names,
                connection_timeout,
                reservation_access,
                reservation_group,
                reservation_timeout,
            ) as session:

                device_commands = session.get_device_property_string_array(
                    device_names, "Dev.Commands"
                )

                device_properties = session.get_device_property_string_array(
                    device_names, "Dev.Properties"
                )

                device_physical_channels = session.get_device_property_string_array(
                    device_names, "Dev.PhysChans"
                )

                for physical_channel in device_physical_channels:
                    data[f"{physical_channel}"] = {"Commands": [], "Properties": []}

                for device_command in device_commands:
                    with session.open_device_command(device_names, device_command) as command:
                        name = device_command
                        description = command.get_command_property_string("Cmd.Descr")
                        access = ReservationAccess(command.get_command_property_int32("Cmd.Access"))
                        data["Commands"].append(
                            {"name": name, "description": description, "access": access.name}
                        )

                        print(data)

                for device_property in device_properties:
                    with session.open_device_property(device_names, device_property) as property:
                        name = device_property
                        datatype = DataType(property.get_property_property_int32("Prop.DataType"))

                        current_value = get_property(
                            session, device_names, device_property, datatype
                        )

                        access = PropertyAccess(property.get_property_property_int32("Prop.Access"))
                        description = property.get_property_property_string("Prop.Descr")

                        min_value = property.get_property_property_string("Prop.MinValue")
                        max_value = property.get_property_property_string("Prop.MaxValue")

                        range_value = (
                            f"[{min_value}, {max_value}]"
                            if min_value is not None and max_value is not None
                            else ""
                        )
                        data["Properties"].append(
                            {
                                "name": name,
                                "current_value": current_value,
                                "datatype": datatype.name,
                                "range": range_value,
                                "access": access.name,
                                "description": description,
                            }
                        )

                for physical_channel in device_physical_channels:

                    physical_channel_commands = session.get_physical_channel_property_string_array(
                        physical_channel, "PhysChan.Commands"
                    )
                    physical_channel_properties = (
                        session.get_physical_channel_property_string_array(
                            physical_channel, "PhysChan.Properties"
                        )
                    )

                    for physical_channel_command in physical_channel_commands:
                        with session.open_physical_channel_command(
                            physical_channel, physical_channel_command
                        ) as command:
                            name = physical_channel_command
                            description = command.get_command_property_string("Cmd.Descr")
                            access = ReservationAccess(
                                command.get_command_property_int32("Cmd.Access")
                            )
                            data[physical_channel]["Commands"].append(
                                {"name": name, "description": description, "access": access.name}
                            )

                    for physical_channel_property in physical_channel_properties:
                        with session.open_physical_channel_property(
                            physical_channel, physical_channel_property
                        ) as property:
                            name = physical_channel_property
                            datatype = DataType(
                                property.get_property_property_int32("Prop.DataType")
                            )

                            current_value = get_property(
                                session, physical_channel, physical_channel_property, datatype
                            )

                            access = PropertyAccess(
                                property.get_property_property_int32("Prop.Access")
                            )
                            description = property.get_property_property_string("Prop.Descr")

                            min_value = property.get_property_property_string("Prop.MinValue")
                            max_value = property.get_property_property_string("Prop.MaxValue")

                            range_value = (
                                f"[{min_value}, {max_value}]" if min_value and max_value else ""
                            )
                            data[physical_channel]["Properties"].append(
                                {
                                    "name": name,
                                    "current_value": current_value,
                                    "datatype": datatype.name,
                                    "range": range_value,
                                    "access": access.name,
                                    "description": description,
                                }
                            )

                complete_data = json.dumps(data, indent=4)
                print(complete_data)


def get_property(session, resource, property, datatype):
    """Retrieve the current value of a property based on its data type."""
    if datatype.value == DataType.BOOL:
        current_value = session.get_generic_property_bool(resource, property)
    elif datatype.value == DataType.DOUBLE:
        current_value = session.get_generic_property_double(resource, property)
    elif datatype.value == DataType.INT32:
        current_value = session.get_generic_property_int32(resource, property)
    elif datatype.value == DataType.INT64:
        current_value = session.get_generic_property_int64(resource, property)
    elif datatype.value == DataType.STRING:
        current_value = session.get_generic_property_string(resource, property)
    elif datatype.value == DataType.UINT32:
        current_value = session.get_generic_property_uint32(resource, property)
    elif datatype.value == DataType.UINT64:
        current_value = session.get_generic_property_uint64(resource, property)
    elif datatype.value == DataType.BOOL_ARRAY:
        current_value = session.get_generic_property_bool_array(resource, property)
    elif datatype.value == DataType.DOUBLE_ARRAY:
        current_value = session.get_generic_property_double_array(resource, property)
    elif datatype.value == DataType.INT32_ARRAY:
        current_value = session.get_generic_property_int32_array(resource, property)
    elif datatype.value == DataType.INT64_ARRAY:
        current_value = session.get_generic_property_int64_array(resource, property)
    elif datatype.value == DataType.STRING_ARRAY:
        current_value = session.get_generic_property_string_array(resource, property)
    elif datatype.value == DataType.UINT32_ARRAY:
        current_value = session.get_generic_property_uint32_array(resource, property)
    elif datatype.value == DataType.UINT64_ARRAY:
        current_value = session.get_generic_property_uint64_array(resource, property)
    else:
        current_value = "Unsupported DataType"

    return current_value


def main():
    """Main function to execute the command."""
    if len(sys.argv) > 1:
        device_names = sys.argv[1]
    else:
        print("Please provide device names.")

    show_command_and_property_tree(device_names)


main()
