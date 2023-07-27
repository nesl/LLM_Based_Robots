
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Create3
from irobot_edu_sdk.music import Note
import queue

robot = Create3(Bluetooth())
print("Successfully connect to create3 robot")

# Sound mapping
async def play_sound(robot, action):
    if action == 'start_move':
        await robot.play_note(Note.A4, 0.5)
    elif action == 'stop_move':
        await robot.play_note(Note.A4_SHARP, 0.5)
    elif action == 'dock':
        await robot.play_note(Note.C4, 0.5)
    elif action == 'undock':
        await robot.play_note(Note.C4_SHARP, 0.5)

# global variables
DIR = [0,1,0,-1,0]
UNIT_LENGTH = 20
room_map = [['E','E','B','B'],['B','E','E','B'],['E','E','E','B'],['B','E','E','E']]


def get_path(room_map, start, target):
    path = []
    cur_pos = target
    path.append(cur_pos)
    while (cur_pos != start):
        for i in range (0, 4):
            prev_pos = (cur_pos[0]-DIR[i], cur_pos[1]-DIR[i+1])
            if prev_pos[0]<0 or prev_pos[0]>=len(room_map) or prev_pos[1]<0 or prev_pos[1]>=len(room_map[0]):
                continue
            if room_map[prev_pos[0]][prev_pos[1]] == room_map[cur_pos[0]][cur_pos[1]]-1:
                path.append(prev_pos)
                break
        cur_pos = prev_pos
    path.pop()
    path.reverse()
    return path

def BFS(room_map, start, target):
    if (start == target):
        return []

     # BFS 
    my_queue = queue.Queue()
    my_queue.put(start)   
    room_map[start[0]][start[1]] = 0

    # Process elements in the queue until it becomes empty
    while not my_queue.empty():
        # Get the current position from the front of the queue
        cur_pos = my_queue.get()
        # record and return the valid path
        if (cur_pos == target):
            return get_path(room_map, start, target)
        
        # update map to find path
        for i in range(0,4):
            next_pos = (cur_pos[0]+DIR[i], cur_pos[1]+DIR[i+1])
            if next_pos[0]<0 or next_pos[0]>=len(room_map) or next_pos[1]<0 or next_pos[1]>=len(room_map[0]):
                continue
            if room_map[next_pos[0]][next_pos[1]] == 'B':
                continue
            if str(room_map[next_pos[0]][next_pos[1]]).isdigit():
                room_map[next_pos[0]][next_pos[1]] = min(room_map[next_pos[0]][next_pos[1]], room_map[cur_pos[0]][cur_pos[1]]+1)
                continue
            room_map[next_pos[0]][next_pos[1]] = room_map[cur_pos[0]][cur_pos[1]]+1
            my_queue.put(next_pos)
    print("Cannot find a path to the target point")
    exit(1)

async def fixed_map_navigate_to(robot, room_map, target):
    await play_sound(robot, 'start_move')
    cur_pos = await robot.get_position()
    start = (cur_pos.x, cur_pos.y)
    path = BFS(room_map, start, target)
    print ("Path: ", path)
    for i in range (0,len(path)):
        # TODO: change unit_length
        x = path[i][0]
        y = path[i][1]
        await robot.navigate_to(x*UNIT_LENGTH, y*UNIT_LENGTH, heading = None)
    await play_sound(robot, 'stop_move')

@event(robot.when_play)
async def play(robot):
    await fixed_map_navigate_to(robot, room_map, (3,3))

robot.play()
