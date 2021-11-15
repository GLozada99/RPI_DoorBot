import subprocess

import asyncio
from decouple import config

import matrix_functions as mx
import functions as func


async def main():
    server = config('MATRIX_SERVER')
    user = config('MATRIX_USER')
    password = config('MATRIX_PASSWORD')
    device_id = config('MATRIX_DEVICE_ID')
    room = config('MATRIX_ROOM_NAME_SPEAKER')
    
    client_task = asyncio.create_task(
        mx.matrix_login(server, user, password, device_id))
    client = await client_task

    room_id_task1 = asyncio.create_task(
        mx.matrix_get_room_id(client, room))
    room_id = await room_id_task1

    proc = subprocess.Popen(['true'])
    last_msg_ids = set()
    messages = []
    while True:
        msg = ''
        room_msg_task = asyncio.create_task(
            mx.matrix_get_messages(client, room_id, limit=2))
        room_msgs = await room_msg_task
        if room_msgs:
            for room_msg in room_msgs:
                msg, timestamp, msg_id = room_msg
                if not (msg_id in last_msg_ids or func.has_time_passed(timestamp, 20)):
                    last_msg_ids.add(msg_id)
                    messages.extend(msg.split('\n'))

        for name in messages:
            try:
                proc = subprocess.Popen(
                    f'aplay ./Audio/{name}.wav'.split())
                proc.wait()
            except Exception as e:
                print(e)

        messages.clear()

        # for _, event_id in room_msgs:
        #     last_room_msg_event_ids.insert(0, event_id)

        # last_room_msg_event_ids = last_room_msg_event_ids[:10]

if __name__ == '__main__':
    asyncio.run(main())
