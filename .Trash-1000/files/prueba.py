# from gpiozero import LED
# from dae import Daemon

import time
import argparse
import functions as func
import asyncio


async def run():
    server = 'https://matrix-client.matrix.org'
    user = '@tavo9:matrix.org'
    password = 'O1KhpTBn7D47'
    room = '#temper:matrix.org'
    device_id = 'QXWVUANCNW'
    client_task = asyncio.create_task(
        func.matrix_login(server, user, password, device_id))
    client = await client_task

    room_id_task = asyncio.create_task(
        func.matrix_get_room_id(client, room))
    room_id = await room_id_task
    # led = LED(23)
    while True:
        # print('Hola')
        # led.on()
        time.sleep(1)
        await func.send_message(client, room_id, 'HOLAAAAAAAAAA')
        # print('Adios')
        # led.off()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--start', action='store_true')
    ap.add_argument('-e', '--stop', action='store_true')
    ap.add_argument('-r', '--restart', action='store_true')
    ap.add_argument('-d', '--debug', action='store_true')
    ap.add_argument('-i', '--status', action='store_true')

    # sensor = Sensor('/tmp/sensor.pid', '/tmp/sensor.date',
    #                 stdout='/tmp/sensor.log')

    args = vars(ap.parse_args())

    if args['start']:
        asyncio.run(run())

        # elif args['stop']:
        #     sensor.stop()
        # elif args['restart']:
        #     asyncio.run(sensor.restart())
        # elif args['debug']:
        #     asyncio.run(sensor.run())
        # elif args['status']:
        #     sensor.is_running()
