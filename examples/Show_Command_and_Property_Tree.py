import json
import sys
from nislsc._nislsc import NISLSC
from nislsc.constants import ReservationAccess, PropertyAccess, DataType, TableScaleCoercion

def show_command_and_property_tree():
    """
    Show the command and property tree of the NISLSC library.
    """

    with NISLSC() as nislsc:
        with nislsc.initialize_library() as lib:
            
            # Initialize session
            if len(sys.argv) > 1:
                device_names = sys.argv[1]
            else:
                print("Please provide device names.")

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
                device_names, connection_timeout, reservation_access, reservation_group, reservation_timeout
            ) as session:

                device_commands = session.get_device_property_string_array(device_names, "Dev.Commands")

                device_properties = session.get_device_property_string_array(device_names, "Dev.Properties")

                device_physical_channels = session.get_device_property_string_array(device_names, "Dev.PhysChans")

                for physical_channel in device_physical_channels:
                    data[f"{physical_channel}"] = {
                        "Commands": [],
                        "Properties": []
                    }
                
                for device_command in device_commands:
                    with session.open_device_command(device_names, device_command) as command:
                        name = device_command
                        description = command.get_command_property_string("Cmd.Descr")
                        access = ReservationAccess(command.get_command_property_int32("Cmd.Access"))
                        data['Commands'].append({
                            "name": name,
                            "description": description,
                            "access": access.name
                        })
                        
                        print(data)

                for device_property in device_properties:
                    with session.open_device_property(device_names, device_property) as property:
                        name = device_property
                        datatype = DataType(property.get_property_property_int32("Prop.DataType"))
                        
                        if datatype.value == 1:
                            current_value = session.get_generic_property_bool(device_names, device_property)
                        elif datatype.value == 2:
                            current_value = session.get_generic_property_double(device_names, device_property)
                        elif datatype.value == 3:
                            current_value = session.get_generic_property_int32(device_names, device_property)
                        elif datatype.value == 4:
                            current_value = session.get_generic_property_int64(device_names, device_property)
                        elif datatype.value == 5:
                            current_value = session.get_generic_property_string(device_names, device_property)
                        elif datatype.value == 6:
                            current_value = session.get_generic_property_uint32(device_names, device_property)
                        elif datatype.value == 7:
                            current_value = session.get_generic_property_uint64(device_names, device_property)
                        elif datatype.value == 8:
                            current_value = session.get_generic_property_bool_array(device_names, device_property)
                        elif datatype.value == 9:
                            current_value = session.get_generic_property_double_array(device_names, device_property)
                        elif datatype.value == 10:
                            current_value = session.get_generic_property_int32_array(device_names, device_property)
                        elif datatype.value == 11:
                            current_value = session.get_generic_property_int64_array(device_names, device_property)
                        elif datatype.value == 12:
                            current_value = session.get_generic_property_string_array(device_names, device_property)
                        elif datatype.value == 13:
                            current_value = session.get_generic_property_uint32_array(device_names, device_property)
                        elif datatype.value == 14:
                            current_value = session.get_generic_property_uint64_array(device_names, device_property)
                        else:
                            current_value = "Unsupported DataType"

                        access = PropertyAccess(property.get_property_property_int32("Prop.Access"))
                        description = property.get_property_property_string("Prop.Descr")

                        min_value = property.get_property_property_string("Prop.MinValue")
                        max_value = property.get_property_property_string("Prop.MaxValue")
                        
                        range_value = f"[{min_value}, {max_value}]" if min_value is not None and max_value is not None else ""
                        data['Properties'].append({
                            "name": name,
                            "current_value": current_value,
                            "datatype": datatype.name,
                            "range": range_value,
                            "access": access.name,
                            "description": description
                        })
                        
                for physical_channel in device_physical_channels:

                    physical_channel_commands = session.get_physical_channel_property_string_array(physical_channel, "PhysChan.Commands")
                    physical_channel_properties = session.get_physical_channel_property_string_array(physical_channel, "PhysChan.Properties")

                    for physical_channel_command in physical_channel_commands:
                        with session.open_physical_channel_command(physical_channel, physical_channel_command) as command:
                            name = physical_channel_command
                            description = command.get_command_property_string("Cmd.Descr")
                            access = ReservationAccess(command.get_command_property_int32("Cmd.Access"))
                            data[physical_channel]["Commands"].append({
                                "name": name,
                                "description": description,
                                "access": access.name
                            })

                    for physical_channel_property in physical_channel_properties:
                        with session.open_physical_channel_property(physical_channel, physical_channel_property) as property:
                            name = physical_channel_property
                            datatype = DataType(property.get_property_property_int32("Prop.DataType"))
                            
                            if datatype.value == 1:
                                current_value = session.get_generic_property_bool(physical_channel, physical_channel_property)
                            elif datatype.value == 2:
                                current_value = session.get_generic_property_double(physical_channel, physical_channel_property)
                            elif datatype.value == 3:
                                current_value = session.get_generic_property_int32(physical_channel, physical_channel_property)
                            elif datatype.value == 4:
                                current_value = session.get_generic_property_int64(physical_channel, physical_channel_property)
                            elif datatype.value == 5:
                                current_value = session.get_generic_property_string(physical_channel, physical_channel_property)
                            elif datatype.value == 6:
                                current_value = session.get_generic_property_uint32(physical_channel, physical_channel_property)
                            elif datatype.value == 7:
                                current_value = session.get_generic_property_uint64(physical_channel, physical_channel_property)
                            elif datatype.value == 8:
                                current_value = session.get_generic_property_bool_array(physical_channel, physical_channel_property)
                            elif datatype.value == 9:
                                current_value = session.get_generic_property_double_array(physical_channel, physical_channel_property)
                            elif datatype.value == 10:
                                current_value = session.get_generic_property_int32_array(physical_channel, physical_channel_property)
                            elif datatype.value == 11:
                                current_value = session.get_generic_property_int64_array(physical_channel, physical_channel_property)
                            elif datatype.value == 12:
                                current_value = session.get_generic_property_string_array(physical_channel, physical_channel_property)
                            elif datatype.value == 13:
                                current_value = session.get_generic_property_uint32_array(physical_channel, physical_channel_property)
                            elif datatype.value == 14:
                                current_value = session.get_generic_property_uint64_array(physical_channel, physical_channel_property)
                            else:
                                current_value = "Unsupported DataType"

                            access = PropertyAccess(property.get_property_property_int32("Prop.Access"))
                            description = property.get_property_property_string("Prop.Descr")

                            min_value = property.get_property_property_string("Prop.MinValue")
                            max_value = property.get_property_property_string("Prop.MaxValue")

                            range_value = f"[{min_value}, {max_value}]" if min_value and max_value else ""
                            data[physical_channel]["Properties"].append({
                                "name": name,
                                "current_value": current_value,
                                "datatype": datatype.name,
                                "range": range_value,
                                "access": access.name,
                                "description": description
                            })

                complete_data = json.dumps(data, indent=4)
                print(complete_data)


show_command_and_property_tree()
