#--------------------------------------------  Import libraries  --------------------------------------------#
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Create3
from irobot_edu_sdk.music import Note
from irobot_edu_sdk.utils import stop_program
import queue

#--------------------------------------------  Robot class implementation  --------------------------------------------#
class Robot:
    #==================== global variables ====================#
    def __init__(self): 
        self.robot_bluetooth_address = "00:16:A4:64:E7:E7"
        self.robot_name = 'iRobot-690A4C7F9021447A92FBC7'
        self.robot = Create3(Bluetooth(name=self.robot_name))
        self.DIR = [0,1,0,-1,0]
        self.UNIT_LENGTH = 20


    #==================== sound action mapping ====================#
    ### explanation: Define different sounds for different actions of the robot.

    async def play_sound(self, action):
        if action == 'start_move':
            await self.robot.play_note(Note.A4, 0.5)
        elif action == 'stop_move':
            await self.robot.play_note(Note.A4_SHARP, 0.5)
        elif action == 'dock':
            await self.robot.play_note(Note.C4, 0.5)
        elif action == 'undock':
            await self.robot.play_note(Note.C4_SHARP, 0.5)
            
    #==================== return a list of path that the robot will follow ====================#
    ### explaination: room_map now has "B" in places that are blocked and integers in places can be arrived showing the steps from the point to the origin. 
    ###               The target position will have the largest integer on the map.
    ###               get_path function back trace the numbers in descending order until find a 0, ie, start point. 
    ###               path list reverse itself after the back trace to get correct sequence of paths that robot will want to follow.
    
    def get_path(self, room_map, start, target):
        # Define an empty path and append the target position
        path = []
        cur_pos = target
        path.append(cur_pos)

        # Search for numbers in descending order on map until find start position
        while (cur_pos != start):
            for i in range (0, 4):
                prev_pos = (cur_pos[0]-self.DIR[i], cur_pos[1]-self.DIR[i+1])
                if prev_pos[0]<0 or prev_pos[0]>=len(room_map) or prev_pos[1]<0 or prev_pos[1]>=len(room_map[0]):
                    continue
                if room_map[prev_pos[0]][prev_pos[1]] == room_map[cur_pos[0]][cur_pos[1]]-1:
                    # add position that matches standard to the list
                    path.append(prev_pos)
                    break
            cur_pos = prev_pos
        
        # Delete start point from the list
        path.pop()

        # Reverse the list to get correct-ordered path
        path.reverse()
        return path


    #==================== BFS ====================#
    ### explanation: Find and return the shortest path the robot can follow from one point to another
    ###              exit(1) if robot cannot get to the target place

    def BFS(self, room_map, start, target):
        # If start and target are the same place, no need to move
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
            
            # Update map to find path
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
        
        # Not find valid path and exit with error
        print("Cannot find a path to the target point")
        exit(1)

    
    #==================== main body of robot navigation action ====================#
    ### explanation: robot mainly follow the actions in this function when fixed_map_navigate_to function is called
    # action 1: Play sound to show the robot starts moving
    # action 2: Call BFS to find the optimal path
    # action 3: Follow the optimal path by using robot.navigate_to function (length between two points is defined by UNIT_LENGTH)
    # action 4: Play sound to show the robot finishes moving
    # action 5: Print "Navigation completed!"

    async def helper_fixed_map_navigate_to(self, room_map, target):
        # action 1
        await self.play_sound('start_move')

        # action 2
        cur_pos = await self.robot.get_position()
        start = (cur_pos.x, cur_pos.y)
        path = self.BFS(room_map, start, target)
        print ("Path: ", path)

        # action 3
        for i in range (0,len(path)):
            x = path[i][0]
            y = path[i][1]
            await self.robot.navigate_to(x*self.UNIT_LENGTH, y*self.UNIT_LENGTH, heading = None)

        # action 4
        await self.play_sound('stop_move')

        # action 5
        print("Navigation completed!")

    #==================== add navigation helper function to the play loop ====================#
    ### explanation: Robot will only start move when robot.play() function is captured by event robot.when_play (reference: irobot_edu_sdk/robot.py).
    ###              Define navigate function to wrap navigation helper function.
    ###              Pass the navigate function to when_play event and call the robot.play().

    def fixed_map_navigate_to(self, room_map, target):
        async def navigate(robot):
            await self.helper_fixed_map_navigate_to(room_map, target)
            # TODO: experiment on jetson to see if need to stop_program (possibly not)
            stop_program()
        self.robot.when_play(navigate)
        self.robot.play()  # Start the robot's event loop


#-------------------------------------------------- test case --------------------------------------------------#
if __name__ == '__main__':
    room_map = [['E','E','B','B'],['B','E','E','B'],['E','E','E','B'],['B','E','E','E']]
    robot = Robot()
    robot.fixed_map_navigate_to(room_map, (3, 3))
    robot.stop()
