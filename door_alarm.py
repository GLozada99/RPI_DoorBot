from gpiozero import Button, LED
from decouple import config
import matrix_functions as mx
import functions as func
import asyncio
import time

#Parar el programa hasta que el pin se ponga high, si pasa un tiempo depsues del high se tiene que correr el audio

async def main():
    server = config('MATRIX_SERVER')
    user = config('MATRIX_USER')
    password = config('MATRIX_PASSWORD')
    device_id = config('MATRIX_DEVICE_ID')
    room = config('MATRIX_ROOM_NAME_ALARM')
    el_pin = Button(17, pull_up=False)

    alarm_task = asyncio.create_task(
        mx.matrix_login(server, user, password, device_id))
    alarm = await alarm_task

    room_id_task = asyncio.create_task(mx.matrix_get_room_id(alarm,room))
    room_id = await room_id_task

    time_flag = True
    other_flag = True

    ALARM_TIME = 30

    while True:
        time.sleep(1)
        if not el_pin.is_active:
            if time_flag:
                time_msg = time.time()
                time_flag = False
                other_flag = True
            if func.has_time_passed(time_msg, ALARM_TIME) and other_flag:
                other_flag = False
                await mx.matrix_send_message(alarm, room_id, 'ALARM')
                print('alarm')
        elif not time_flag and not other_flag:
            await mx.matrix_send_message(alarm, room_id, 'STOP')
            time_flag = True
            print('stop')
        else:
            time_msg = time.time()
        
if __name__ == '__main__':
    asyncio.run(main())


