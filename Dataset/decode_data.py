import pandas as pd
import struct

data = pd.read_csv('./raw_sleep_data.csv', dtype=str)

def decode_radar_packet(hex_string):
    if pd.isna(hex_string) or not isinstance(hex_string, str):
        return "Invalid Data", None, "Invalid Data"

    try:
        bytes_list = [int(x, 16) for x in hex_string.split()]
    except ValueError:
        return "Invalid Data", None, "Invalid Data"

    if len(bytes_list) < 10 or bytes_list[0] != 0x55:
        return "Invalid Packet", None, "Invalid Packet"

    packet_type = bytes_list[5]

    try:
        raw_float_bytes = bytes(bytes_list[6:10])
        movement_value = struct.unpack('<f', raw_float_bytes)[0]
    except struct.error:
        return "Error Extracting Data", None, "Error Extracting Data"

    status = "Deep Sleep"
    posture = "supine"

    if packet_type == 0x06:
        if movement_value < 0.5:
            status = "Sleeping"
            posture = "Supine"
        elif 0.5 <= movement_value < 5:
            status = "Sleeping"
            posture = "Prone"
        elif 5 <= movement_value < 15:
            status = "Sleeping"
            posture = "Side Sleeping"
        elif 15 <= movement_value < 25:
            status = "Posture Change"
            posture = "Supine to Side"
        elif 25 <= movement_value < 35:
            status = "Posture Change"
            posture = "Supine to Prone"
        elif 35 <= movement_value < 45:
            status = "Posture Change"
            posture = "Side to Supine"
        elif 45 <= movement_value < 55:
            status = "Posture Change"
            posture = "Side to Prone"
        elif movement_value >= 55:
            status = "Major Movement"
            posture = "Rolling Over"
    elif packet_type == 0x07:
        if bytes_list[8] == 0x01:
            status = "No Move"
        elif bytes_list[8] == 0x02:
            status = "Deep Breathing"
        elif bytes_list[8] == 0x03:
            status = "Low Breathing"
        else:
            status = f"Unknown Presence Type {bytes_list[8]}"

    return status, movement_value, posture

data[['Status', 'Movement_Value', 'Posture']] = data['raw_data_hex'].apply(
    lambda x: pd.Series(decode_radar_packet(x))
)

data.drop(columns=['raw_data_hex'], inplace=True)

data[['millis', 'Status', 'Movement_Value', 'Posture', 'Name']].to_csv(
    './decoded_sleep_data.csv', index=False
)
print(data.head(20))
