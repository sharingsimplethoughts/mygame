#!/usr/bin/env python
import asyncio
import uvicorn
import socketio
import random

# import mysql.connector


sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
    '/': 'app.html',
})
background_task_started = False


# online_user_ids={
#     'wsade34sdff_sid':'1_uid',
#     'rtsade34sdef_sid':'2_uid',
# }
# joined_room_player_ids=['1','2','3']
# room_detail={
#     '94_room_id':{
#         'game_id':'1',
#         'players':['3','4','5'],
#         'is_busy':True,
#     }
#     '105_room_id':{
#         'game_id':'2',
#         'players':['6','8','10'],
#         'is_busy':False
#     }
#     '135_room_id':{
#         'game_id':'1',
#         'players':['31','14','51'],
#         'is_busy':True
#     }
# }


game_types={
    '1':{
        'max_player':'3',
    },
    '3':{
        'max_player':'8',
    },
}
online_user_ids={}
joined_room_player_ids=[]
room_detail={}

def generate_room_id():
    existing_room_ids = room_detail.keys()
    generated_room_id = ''
    while True:
        generated_room_id = random.randint(0, 1000000)
        if generated_room_id not in existing_room_ids:
            break
    return generated_room_id
def join_room(game_id,room_id,sid):    
    if room_id in room_detail and sid in room_detail[room_id]['players']:
        print('1')
        pass
    elif room_id in room_detail and sid not in room_detail[room_id]['players']:
        print('2')
        room_detail[room_id]['players'].append(sid)
    else:
        print('3')
        room_detail[room_id]={
            'game_id':game_id,
            'players':[sid],
            'is_busy':False,
        }
def get_room_members(room_id):
    members = []
    member_uids = []
    if room_id in room_detail.keys():
        members=room_detail[room_id]['players']
    if members:
        for m in members:
            member_uids.append(get_uid(m))
    return member_uids
def get_uid(sid):
    return online_user_ids[sid] if sid in online_user_ids.keys() else ''


async def background_task():    
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        active_user_list=list(online_user_ids.values())
        print(active_user_list)
        # await sio.emit('my_response', {'data': 'Server generated event'})
        await sio.emit('my_response', {'data': active_user_list})


@sio.on('my_event')
async def test_message(sid, message):
    print('********************')
    print(message)
    online_user_ids[str(sid)]=str(message['uid'])
    print(online_user_ids)
    active_user_list=list(online_user_ids.values())
    await sio.emit('my_response', {'data': active_user_list}, room=sid)

@sio.on('my_event_2')
async def test_message_2(sid, message):
    await sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.on('my_broadcast_event')
async def test_broadcast_message(sid, message):
    await sio.emit('my_response', {'data': message['data']})


@sio.on('join')
async def join(sid, message):
    game_id = message['gid']
    room_id = ''
    max_player = int(game_types[game_id]['max_player'])
    entered_room_id=''
    for i in room_detail.keys():
        if room_detail[i]['game_id'] == game_id:
            if not room_detail[i]['is_busy']:
                if max_player > len(room_detail[i]['players']):
                    room_id = i
                    sio.enter_room(sid, room_id)
                    joined_room_player_ids.append(online_user_ids[str(sid)])
                    join_room(None,room_id,sid)
                    entered_room_id = sio.rooms(sid,None)
    
    if entered_room_id=='':
        generated_room_id = generate_room_id()
        room_id = str(generated_room_id)
        sio.enter_room(sid, room_id)
        joined_room_player_ids.append(online_user_ids[str(sid)])
        join_room(game_id,room_id,sid)
    room_players = get_room_members(room_id)

    data = {'data': room_id, 'players': room_players}
    print(room_id)
    await sio.emit('my_response', {'data': room_players}, room=room_id)

@sio.on('update_room')
async def update_room(sid,message):
    room_detail[message['room']]['is_busy']=True
    await sio.emit('my_response', {'data': 'Room is busy now'}, room=message['room'])

@sio.on('leave')
async def leave(sid, message):
    sio.leave_room(sid, message['room'])
    temp_uid = get_uid(sid)
    joined_room_player_ids.remove(get_uid(sid))
    room_detail[message['room']]['players'].remove(sid)
    await sio.emit('my_response', {'data': temp_uid+ ' Left room'}, room=message['room'])
    await sio.emit('my_response', {'data': 'You Left room: '+message['room']}, room=sid)


@sio.on('close room')
async def close(sid, message):
    await sio.emit('my_response',
                   {'data': 'Room ' + message['room'] + ' is closing.'},
                   room=message['room'])
    await sio.close_room(message['room'])
    room_players = get_room_members(message['room'])    
    for p in room_players:
        if p in joined_room_player_ids:
            joined_room_player_ids.remove(p)
    del room_detail[message['room']]


@sio.on('my_room_event')
async def send_room_message(sid, message):
    await sio.emit('my_response', {'data': message['data']},
                   room=message['room'])


@sio.on('disconnect request')
async def disconnect_request(sid):
    if str(sid) in online_user_ids:
        del online_user_ids[str(sid)]
        joined_room_player_ids.remove(get_uid(sid))
        for r in room_detail:
            if sid in r['players']:
                r['players'].remove(sid)
    # joined_room_ids=[]
    await sio.disconnect(sid)


@sio.on('connect')
async def test_connect(sid, environ):  
    print('------------------')  
    print(sid)
    print(environ)
    global background_task_started
    if not background_task_started:
        print('1')
        sio.start_background_task(background_task)
        print('2')
        background_task_started = True
    # await sio.emit('my_response', {'data': str(posts), 'count': 0}, room=sid)
    print('3')
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.on('disconnect')
def test_disconnect(sid):
    del online_user_ids[str(sid)]
    joined_room_player_ids.remove(get_uid(sid))
    for r in room_detail:
            if sid in r['players']:
                r['players'].remove(sid)
    # joined_room_ids=[]
    print('Client disconnected')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
