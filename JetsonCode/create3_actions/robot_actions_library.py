#--------------------------------------------  Import libraries  --------------------------------------------#
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Create3
from irobot_edu_sdk.music import Note
from irobot_edu_sdk.utils import stop_program
import queue
import numpy as np

#--------------------------------------------  Robot class implementation  --------------------------------------------#
class Robot:
    #==================== global variables ====================#
    DIR = [0,1,0,-1,0]
    UNIT_LENGTH = 20

    def __init__(self): 
        try:
        # Connecting to iRobotCreate3 (47682A24-F400-A918-B4A0-08822B3A25F4)
            self._robot_name = 'iRobotCreate3'
            self._robot_bluetooth_address = "47682A24-F400-A918-B4A0-08822B3A25F4"
            self._robot = Create3(Bluetooth(self._robot_name, self._robot_bluetooth_address))
        except Exception as e:
            print("Error when connecting to robot create3:", e)


    #==================== sound action mapping ====================#
    ### explanation: Define different sounds for different actions of the robot.

    async def play_sound(self, action):
        try:
            if action == 'start_move':
                await self._robot.play_note(Note.A4, 0.5)
            elif action == 'stop_move':
                await self._robot.play_note(Note.A4_SHARP, 0.5)
            elif action == 'dock':
                await self._robot.play_note(Note.C4, 0.5)
            elif action == 'undock':
                await self._robot.play_note(Note.C4_SHARP, 0.5)
        except Exception as e:
            print("Error when playing sound:", e)
    
    #==================== dock function ====================#
    def dock(self):
        try: 
            async def helper_dock(robot):
                await self._robot.dock()
                #await self.play_sound('dock')
                print("Finish docking")
                # TODO: experiment on jetson to see if need to stop_program (possibly not)
            self._robot.when_play(helper_dock)
            self._robot.play()  # Start the robot's event loop
        except Exception as e:
            print("Error happened when dock:", e)
    
    #==================== undock function ====================#
    def undock(self):
        try:
            async def helper_undock(robot):
                await self._robot.undock()
                #await self.play_sound('undock')
                print("Finish undocking")
                # TODO: experiment on jetson to see if need to stop_program (possibly not)
            self._robot.when_play(helper_undock)
            self._robot.play()
        except Exception as e:
            print("Error happened when undock:", e)
            
    #==================== fixed_map_navigate_to function ====================#
    #***************** helper functions *****************#

    ############# get path #############
    ### explaination: room_map now has "B" in places that are blocked and integers in places can be arrived showing the steps from the point to the origin. 
    ###               The target position will have the largest integer on the map.
    ###               get_path function back trace the numbers in descending order until find a 0, ie, start point. 
    ###               path list reverse itself after the back trace to get correct sequence of paths that robot will want to follow.

    def get_path(self, room_map, start, target):

        # helper function to optimize path
        ### explanation: merge two coordinates if they are in the same line
        def merge_path(path):
            try:
                merged_path = []
                i = 0
                same_x = True
                same_y = True
                while i < len(path):
                    cur_coordinate = path[i]
                    next_coordinate = path[i+1] if i+1 < len(path) else None

                    # if in the same line consistently, check next element
                    if same_x and next_coordinate and cur_coordinate[0] == next_coordinate[0]:
                        coordinate_to_add = next_coordinate
                        same_y = False
                    elif same_y and next_coordinate and cur_coordinate[1] == next_coordinate[1]:
                        coordinate_to_add = next_coordinate
                        same_x = False
                    else:
                        # add the last element on the line to merged list
                        merged_path.append(cur_coordinate)
                        same_x = True
                        same_y = True
                    i += 1

                return merged_path
            except Exception as e:
                print("Error when merging path:", e)

        try:
            # Define an empty path and append the target position
            path = []
            cur_pos = start
            path.append(cur_pos)

            # Search for numbers in descending order on map until find start position
            while (cur_pos != target):
                for i in range (0, 4):
                    prev_pos = [cur_pos[0]-self.DIR[i], cur_pos[1]-self.DIR[i+1]]
                    # print(room_map[prev_pos[0]][prev_pos[1]], room_map[cur_pos[0]][cur_pos[1]]) # For debug purpose
                    if prev_pos[0]<0 or prev_pos[0]>=len(room_map) or prev_pos[1]<0 or prev_pos[1]>=len(room_map[0]):
                        continue
                    if str(room_map[prev_pos[0]][prev_pos[1]]).isdigit() and room_map[prev_pos[0]][prev_pos[1]] == room_map[cur_pos[0]][cur_pos[1]]-1:
                        # add position that matches standard to the list
                        path.append(prev_pos)
                        break
                cur_pos = prev_pos

            # Reverse the list to get correct-ordered path
            print("Complete path: ", path)
            return merge_path(path)
        
        except Exception as e:
            print("Error when get path:", e)


    ############# BFS #############
    ### explanation: Find and return the shortest path the robot can follow from one point to another
    ###              exit(1) if robot cannot get to the target place

    def BFS(self, room_map, start, target):
        try:
            # If start and target are the same place, no need to move
            if (start == target):
                return

            # BFS 
            my_queue = queue.Queue()
            my_queue.put(target)   
            room_map[target[0]][target[1]] = 0

            # Process elements in the queue until it becomes empty
            while not my_queue.empty():
                # Get the current position from the front of the queue
                cur_pos = my_queue.get()
                # record and return the valid path
                if (cur_pos == start):
                    return self.get_path(room_map, start, target)
                
                # Update map to find path
                for i in range(0,4):
                    next_pos = [cur_pos[0]+self.DIR[i], cur_pos[1]+self.DIR[i+1]]
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
        except Exception as e:
            print("Error when BFS:", e)

    
    ############# main body of robot navigation action #############
    ### explanation: robot mainly follow the actions in this function when fixed_map_navigate_to function is called
    # action 1: Call BFS to find the optimal path
    # action 2: Play sound to show the robot starts moving
    # action 3: Follow the optimal path by using robot.navigate_to function (length between two points is defined by unit_length)
    # action 4: Play sound to show the robot finishes moving
    # action 5: Print "Navigation completed!"

    async def helper_fixed_map_navigate_to(self, room_map, target):
        try: 
            # action 1
            cur_pos = await self._robot.get_position()
            start = [cur_pos.x, cur_pos.y]
            path = self.BFS(room_map, start, target)
            print ("Path: ", path)

            # action 2
            await self.play_sound('start_move')

            # action 3
            for i in range (0,len(path)):
                x = path[i][0]
                y = path[i][1]
                await self._robot.navigate_to(x*self.UNIT_LENGTH, y*self.UNIT_LENGTH, heading = None)

            # action 4
            await self.play_sound('stop_move')

            # action 5
            print("Navigation completed!")
        except Exception as e:
            print("Error when navigating:", e)

   #***************** main navigation function *****************#
    ### explanation: Robot will only start move when robot.play() function is captured by event robot.when_play (reference: irobot_edu_sdk/robot.py).
    ###              Define navigate function to wrap navigation helper function.
    ###              Pass the navigate function to when_play event and call the robot.play().

    def fixed_map_navigate_to(self, room_map, target):
        try:
            async def navigate(robot):
                await self.helper_fixed_map_navigate_to(room_map, target)
                # TODO: experiment on jetson to see if need to stop_program (possibly not)
                stop_program()
            self._robot.when_play(navigate)
            self._robot.play()  # Start the robot's event loop
        except Exception as e:
            print("Error when start nagivation in play loop")


#-------------------------------------------------- test case --------------------------------------------------#
if __name__ == '__main__':
    robot = Robot()

    #*********** navigate_to ***********#
    # room_map = [['E','B','B','B'],['E','E','E','B'],['B','B','E','B'],['B','E','E','E']]
    # robot.fixed_map_navigate_to(room_map, [2, 2])
    # robot.stop()

    #*********** dock and undock ***********#
    await robot.dock()
    await robot.undock()
