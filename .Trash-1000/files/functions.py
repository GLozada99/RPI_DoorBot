from nio import AsyncClient, RoomMessageText


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


async def matrix_get_messages(client, room_id):
    messages = []
    sync_response = await client.sync(timeout=10000)

    if len(sync_response.rooms.join) > 0:
        events = sync_response.rooms.join[room_id].timeline.events
        message_events = filter(
            lambda x: isinstance(x, RoomMessageText), events)

        for eve in message_events:
            msg = eve.body
            timestamp_miliseconds = int(eve.server_timestamp)
            timestamp_seconds = float(timestamp_miliseconds / 1000)
            messages.append((msg, timestamp_seconds))

    return messages
