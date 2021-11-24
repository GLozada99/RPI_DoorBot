import subprocess

import asyncio
import time
from decouple import config

import matrix_functions as mx
import functions as func


async def main():
    server = config('MATRIX_SERVER')
    user = config('MATRIX_USER')
    password = config('MATRIX_PASSWORD')
    device_id = config('MATRIX_DEVICE_ID')
    room = config('MATRIX_ROOM_NAME_SPEAKER')
    lang_room = config('MATRIX_ROOM_NAME_LANGUAGE')
    
    client_task = asyncio.create_task(
        mx.matrix_login(server, user, password, device_id))
    client = await client_task

    room_id_task1 = asyncio.create_task(
        mx.matrix_get_room_id(client, room))
    room_id = await room_id_task1

    lang_id_task = asyncio.create_task(mx.matrix_get_room_id(client, lang_room))
    lang_id = await lang_id_task

    proc = subprocess.Popen(['true'])
    last_msg_ids = set()
    messages = []
    langu = ""
    last_time_lang = 0
    while True:
        msg = ''
        room_msg_task = asyncio.create_task(
            mx.matrix_get_messages(client, room_id, limit=2))
        room_msgs = await room_msg_task

        lang_room_task = asyncio.create_task(
            mx.matrix_get_messages(client, lang_id))

        if (func.has_time_passed(last_time_lang, 10)):
            langu = await lang_room_task
            last_time_lang = time.time()

        if room_msgs:
            for room_msg in room_msgs:
                msg, timestamp, msg_id = room_msg
                if not (msg_id in last_msg_ids or func.has_time_passed(timestamp, 20)):
                    last_msg_ids.add(msg_id)
                    messages.extend(msg.split('\n'))
                    messages = messages[0].split()
        for name in messages:
            command = f'aplay ./Audio/{langu}/{name}.wav' 
            try:
                proc = subprocess.Popen(command.split())
                proc.wait()
            except Exception as e:
                print(e)

        messages.clear()

        # for _, event_id in room_msgs:
        #     last_room_msg_event_ids.insert(0, event_id)

        # last_room_msg_event_ids = last_room_msg_event_ids[:10]

if __name__ == '__main__':
    asyncio.run(main())
