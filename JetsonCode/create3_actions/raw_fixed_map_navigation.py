
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Create3
from irobot_edu_sdk.music import Note
import queue


room_map = [['E','E','B','B'],['B','E','E','B'],['E','E','E','B'],['B','E','E','E']]

class Robot:
    def __init__(self): 
        # global variables
        self.robot = Create3(Bluetooth())
        self.DIR = [0,1,0,-1,0]
        self.UNIT_LENGTH = 20

    # Sound mapping
    async def play_sound(self, action):
        if action == 'start_move':
            await self.robot.play_note(Note.A4, 0.5)
        elif action == 'stop_move':
            await self.robot.play_note(Note.A4_SHARP, 0.5)
        elif action == 'dock':
            await self.robot.play_note(Note.C4, 0.5)
        elif action == 'undock':
            await self.robot.play_note(Note.C4_SHARP, 0.5)


    def get_path(self, room_map, start, target):
        path = []
        cur_pos = target
        path.append(cur_pos)
        while (cur_pos != start):
            for i in range (0, 4):
                prev_pos = (cur_pos[0]-self.DIR[i], cur_pos[1]-self.DIR[i+1])
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
                return self.get_path(room_map, start, target)
            
            # update map to find path
            for i in range(0,4):
                next_pos = (cur_pos[0]+self.DIR[i], cur_pos[1]+self.DIR[i+1])
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

    async def helper_fixed_map_navigate_to(self, room_map, target):
        await self.play_sound('start_move')
        cur_pos = await self.robot.get_position()
        start = (cur_pos.x, cur_pos.y)
        path = self.BFS(room_map, start, target)
        print ("Path: ", path)
        for i in range (0,len(path)):
            x = path[i][0]
            y = path[i][1]
            await self.robot.navigate_to(x*UNIT_LENGTH, y*UNIT_LENGTH, heading = None)
        await self.play_sound('stop_move')

    def fixed_map_navigate_to(self, room_map, target):
        async def navigate(self):
            await self.helper_fixed_map_navigate_to(room_map, target)
        self.robot.when_play(navigate)
        self.robot.play()  # Start the robot's event loop


robot = Robot()
robot.fixed_map_navigate_to(room_map, (3,3))
