from gpiozero import DistanceSensor, LED
from smbus2 import SMBus
from mlx90614 import MLX90614
from signal import pause
from time import sleep
from nio import AsyncClient
import asyncio

async def matrix_login(server, user, password, device_id=None):
    if device_id:
        client = AsyncClient(server, user, device_id)
    else:
        client = AsyncClient(server, user)
    await client.login(password)
    return client


async def matrix_get_room_id(client, room_name):
    response = await client.room_resolve_alias(room_name)
    room_id = response.room_id
    return room_id

async def send_message(client, room_id, message):
    await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content={
            "body": message,
            "msgtype": "m.text"
        }
    )
    


async def main():
    data = set()

    bus = SMBus(1)
    temp_sensor = MLX90614(bus, address=0x5A)

    dist_sensor = DistanceSensor(echo=27, trigger=22, threshold_distance=0.1)
    led = LED(23)
    
    good_temp_flag = True
    
    server = 'https://matrix-client.matrix.org'
    user = '@tavo9:matrix.org'
    password = 'O1KhpTBn7D47'
    room = '#temper:matrix.org'
    device_id = 'QXWVUANCNW'
    
    client = await matrix_login(server, user, password, device_id)
    room_id = await matrix_get_room_id(client, room)
    
    while True:
        # print(dist_sensor.distance)
        sleep(0.3)
        if dist_sensor.distance < dist_sensor.threshold_distance:
            if len(data) != 5:
                # print(dist_sensor.distance)
                led.on()
                data.add(temp_sensor.get_object_1())
                # sleep(0.5)
                print(f'Dato {len(data)}/5')
                good_temp_flag = False
            elif not good_temp_flag:
                avg_temp = round(sum(data)/len(data),2)
                good_temp_flag = True
                msg = f'La temperatura es: {avg_temp}, puede retirar la mano'
                print(msg)
                await send_message(client,room_id,str(avg_temp))
                led.off()
            continue
        elif not good_temp_flag:
            print('Superficie retirada, toma de temperatura detenida')
            good_temp_flag = True
            
        led.off()
        data.clear()
            

if __name__ == '__main__':
    asyncio.run(main())            

# dist_sensor.when_in_range = get_temp
# dist_sensor.when_out_of_range = no_temp

# pause()
