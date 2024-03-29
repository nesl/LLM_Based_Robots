#--------------------------------------------  Import libraries  --------------------------------------------#
import sys
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Create3, Robot
from irobot_edu_sdk.music import Note
from irobot_edu_sdk.utils import stop_program
import queue
import copy


#--------------------------------------------  Robot class implementation  --------------------------------------------#
class Create3Robot:
    #==================== global variables ====================#
    DIR = [0,1,0,-1,0]
    UNIT_LENGTH = 4
    ROBOT_POS = [0,0]
    ROBOT_HEADING = 0

    def __init__(self): 
        # Connecting to iRobotCreate3 (47682A24-F400-A918-B4A0-08822B3A25F4)
        self._robot_name = 'iRobotCreate3'
        self._robot_bluetooth_address = "47682A24-F400-A918-B4A0-08822B3A25F4"
        self._robot = Robot(Bluetooth(self._robot_name, self._robot_bluetooth_address))
        

    #==================== update position class method ====================#
    @classmethod
    def update_robot_position(cls, new_position):
        cls.ROBOT_POS = new_position

    @classmethod
    def update_robot_orientation(cls, new_heading):
        cls.ROBOT_HEADING = new_heading


    #==================== sound action mapping ====================#
    ### explanation: Define different sounds for different actions of the robot.

    async def play_sound(self, action):
        if action == 'start_move':
            await self._robot.play_note(Note.A4, 0.5)
        elif action == 'stop_move':
            await self._robot.play_note(Note.A4_SHARP, 0.5)
        elif action == 'dock':
            await self._robot.play_note(Note.C4, 0.5)
        elif action == 'undock':
            await self._robot.play_note(Note.C4_SHARP, 0.5)
            
    #==================== return a list of path that the robot will follow ====================#
    ### explaination: room_map now has "B" in places that are blocked and integers in places can be arrived showing the steps from the point to the origin. 
    ###               The target position will have the largest integer on the map.
    ###               get_path function back trace the numbers in descending order until find a 0, ie, start point. 
    ###               path list reverse itself after the back trace to get correct sequence of paths that robot will want to follow.

    def get_path(self, room_map, start, target):
        # helper function to optimize path
        ### explanation: merge two coordinates if they are in the same line
        def merge_path(path):
            merged_path = []
            i = 0
            same_x = True
            same_y = True
            while i < len(path):
                cur_coordinate = path[i]
                next_coordinate = path[i+1] if i+1 < len(path) else None

                # if in the same line consistently, check next element
                if same_x and next_coordinate and cur_coordinate[0] == next_coordinate[0]:
                    same_y = False
                    i += 1
                elif same_y and next_coordinate and cur_coordinate[1] == next_coordinate[1]:
                    same_x = False
                    i += 1
                else:
                    # add the last element on the line to merged list
                    merged_path.append(cur_coordinate)
                    same_x = True
                    same_y = True
                    i += 1
            
            # print("merged path:", merged_path) #for debugging
            return merged_path

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
        # path.reverse()
        # print("Complete path: ", path)

        return merge_path(path)


    #==================== BFS ====================#
    ### explanation: Find and return the shortest path the robot can follow from one point to another
    ###              exit(1) if robot cannot get to the target place

    def BFS(self, my_room_map, start, target):
        room_map = copy.deepcopy(my_room_map)
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
    
    #==================== navigate function ====================#
    def navigate(self, pos, exp_pos, heading=ROBOT_HEADING):
        if pos[0] == exp_pos[0] and pos[1] != exp_pos[1]:
            y = exp_pos[1]-pos[1]
            new_heading = heading
            if y < 0:
                turn_angle = (360+180-heading)%360
            elif y > 0:
                turn_angle = 360-heading
            else:
                turn_angle = 0
            distance = y*self.UNIT_LENGTH
            
        elif pos[0] != exp_pos[0] and pos[1] == exp_pos[1]:
            x = exp_pos[0]-pos[0]
            if x < 0:
                turn_angle=(360+270-heading)%360
            elif x > 0:
                turn_angle=(360+90-heading)%360
            else:
                turn_angle = 0
            distance = x*self.UNIT_LENGTH
        new_heading = (heading + turn_angle) % 360

        # print("turn angle:", turn_angle)
        # print("new heading:", new_heading)
        turn_left = False
        if (turn_angle > 180):
            turn_angle -= 180
            turn_left = True
        if turn_left:
            self.turn_left(turn_angle)
        else:
            self.turn_right(turn_angle)
        self.update_robot_orientation(new_heading)
        print("robot heading:", self.ROBOT_HEADING)
        self._robot.move(distance)
        self.update_robot_position(exp_pos)
        print("robot position:", self.ROBOT_POS)
    
    #==================== main body of robot navigation saction ====================#
    ### explanation: robot mainly follow the actions in this function when fixed_map_navigate_to function is called
    # action 1: Call BFS to find the optimal path
    # action 2: Play sound to show the robot starts moving
    # action 3: Follow the optimal path by using robot.navigate_to function (length between two points is defined by unit_length)
    # action 4: Play sound to show the robot finishes moving
    # action 5: Print "Navigation completed!"

    def navigate_to(self, room_map, target):

        # action 1
        start = self.ROBOT_POS
        print("start position:", start)
        print("target:", target)
        path = self.BFS(room_map, start, target)
        print ("Path: ", path)
        print("Start Navigation")

        # action 2
        # await self.play_sound('start_move')


        # action 3
        print("self.ROBOT_POS before:", self.ROBOT_POS)
        prev_pos = self.ROBOT_POS
        if path is not None:
            for i in range (0,len(path)):
                exp_pos = path[i]
                self.navigate(prev_pos,exp_pos,self.ROBOT_HEADING)
                print("now the robot is at:", exp_pos)
                prev_pos = [path[i][0], path[i][1]]
            # self.update_robot_position(path[i])
            print("self.ROBOT_POS after:", self.ROBOT_POS)

        # action 4
        # await self.play_sound('stop_move')

        # action 5
        print("Navigation completed!")


    def undock(self):
        self._robot.undock()

    def dock(self):
        self._robot.dock()

    def turn_right(self, angle):
        self._robot.turn_right(angle)
        self.update_robot_orientation((self.ROBOT_HEADING + angle)%360)
        

    def turn_left(self, angle):
        self._robot.turn_left(angle)
        self.update_robot_orientation((self.ROBOT_HEADING + (360-angle))%360)
        


#-------------------------------------------------- test case --------------------------------------------------#
if __name__ == '__main__':
    room_map = [['E','B','B','B'],['E','E','E','B'],['B','B','E','B'],['B','E','E','E']]
    robot = Create3Robot()
    # test 1: navigate to, turn
    # robot.navigate_to(room_map, [1, 0])
    # robot.navigate_to(room_map, [2, 2])

    # test 2: dock and undock
    # robot.undock()
    # robot.dock()

    # test 3: speed
    # robot.navigate_to(room_map, [1, 0])
    # print("good")
    # time.sleep(5)
    # robot.navigate_to(room_map, [2, 2])
    # robot._robot.set_wheel_speeds(100,100)
    # start_time = time.time()
    # robot._robot.move(distance = 20)
    # end_time = time.time()
    # print("speed 10: ", end_time - start_time)

    # start_time = time.time()
    # robot._robot.move(distance = 20)
    # end_time = time.time()
    # print("speed 50: ", end_time - start_time)

    
