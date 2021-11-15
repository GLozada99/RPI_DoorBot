from gpiozero import LED
from decouple import config
from time import sleep, time
import asyncio
import matrix_functions as mx
import functions as fc
from sys import exit


async def main():
    door_unlock = LED(26, initial_value=False)
    
    time_out = 10
    time_unlock = 0
    
    VALID_REQUEST_INTERVAL = 3
    OPEN_DOOR_INTERVAL = 7
    
    server = config('MATRIX_SERVER')
    user = config('MATRIX_USER')
    password = config('MATRIX_PASSWORD')
    device_id = config('MATRIX_DEVICE_ID')
    door_room_name = config('MATRIX_ROOM_NAME_DOOR')
        
    try:
        client = await asyncio.wait_for(mx.matrix_login(
            server, user, password, device_id), time_out)
        door_room_id = await asyncio.wait_for(mx.matrix_get_room_id(
            client, door_room_name), time_out)
    except asyncio.TimeoutError:
        exit(1)
        
    while True:        
        if fc.has_time_passed(time_unlock, OPEN_DOOR_INTERVAL):
            door_unlock.off()

        room_msg_task = asyncio.create_task(
            mx.matrix_get_messages(client, door_room_id))
        room_msgs = await room_msg_task
        if room_msgs:
            msg, timestamp, _ = room_msgs[0]
            try:
                msg = int(msg)
            except ValueError:
                continue
            if not fc.has_time_passed(timestamp, VALID_REQUEST_INTERVAL) and msg == 1 and not door_unlock.is_active:
                door_unlock.on()
                time_unlock = time()
        sleep(0.2)
        


if __name__ == '__main__':
    asyncio.run(main())