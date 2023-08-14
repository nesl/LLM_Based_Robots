class CreateRobot:
    
    script_file = '/home/nesl/RobotROS2.sh'

    def __init__(self):
        import math
        import subprocess
        import numpy as np
        import queue
        self.math = math
        self.subprocess = subprocess
        self.np = np
        self.queue = queue
        
        self.position = [0,0]
        self.heading = 0
        
        DIR = [0,1,0,-1,0]
        UNIT_LENGTH = 12
        ROOM_MAP = [['E','E','E','E','E','E','E','E'],
                ['E','E','E','E','E','E','E','E'],
                ['E','E','E','E','E','B','E','E'],
                ['E','E','E','E','E','B','E','E'],
                ['B','B','E','E','E','E','E','E'],
                ['E','E','E','B','B','E','E','E'],
                ['E','E','E','B','B','E','B','E'],
                ['E','E','E','E','E','E','B','E'],
                ['E','E','E','E','E','E','B','E'],
                ['E','E','E','E','E','E','E','E']
                ]
                
    def stop(self):
        continue
    
    def dock(self):
        command='dock'
        output=self.subprocess.run([self.script_file, command], capture_output=True, text=True)
        if output.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with return code:", output.returncode)
            print("Error output:", output.stderr)

    def undock(self):
        command='undock'
        output=self.subprocess.run([self.script_file, command], capture_output=True, text=True)
        if output.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with return code:", output.returncode)
            print("Error output:", output.stderr)

    def drive_distance_helper(self, distance:"np.float32", max_translation_speed: "np.float32"):
        command='drive_distance'
        output=self.subprocess.run([self.script_file, command, str(distance), str(max_translation_speed)], capture_output=True, text=True)
        if output.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with return code:", output.returncode)
            print("Error output:", output.stderr)

    def rotate_angle_helper(self, angle: "np.float32", max_rotation_speed: "np.float32"):
        command = 'rotate_angle'
        output = subprocess.run([self.script_file, command, str(angle), str(max_rotation_speed)], capture_output=True, text=True)
        if output.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with return code:", output.returncode)
            print("Error output:", output.stderr)

    def wall_follow(self, follow_side: "np.int8", max_runtime_sec: int, max_runtime_nanosec: int):
        command = 'wall_follow'
        output = subprocess.run([self.script_file, command, str(follow_side), str(max_runtime_sec), str(max_runtime_nanosec)], capture_output=True, text=True)
        if output.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with return code:", output.returncode)
            print("Error output:", output.stderr)

    def drive_arc(self, angle: "np.float32", radius: "np.float32", translate_direction: "np.int8", max_translation_speed: "np.float32"):
        command = 'drive_arc'
        output = subprocess.run([self.script_file, command, str(angle), str(radius), str(translate_direction), str(max_translation_speed)], capture_output=True, text=True)
        if output.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with return code:", output.returncode)
            print("Error output:", output.stderr)
    
    def navigate_to_position(self, achieve_goal_heading: bool, xp: "np.float32", yp: "np.float32", zp: "np.float32", xo: "np.float32", yo: "np.float32", zo: "np.float32", wo: "np.float32"):
        command = 'navigate_to_position'
        output = subprocess.run([self.script_file, command, str(achieve_goal_heading), str(xp), str(yp), str(zp), str(xo), str(yo), str(zo), str(wo)], capture_output=True, text=True)
        if output.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with return code:", output.returncode)
            print("Error output:", output.stderr)





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

    
    #==================== update_positional_status function ====================#
    def update_positional_status(self, current, target):
        #update heading
        if target[1] - current[1] > 0: #moved north
            return
        elif target[1] - current[1] < 0: #moved south
            self.heading += 180
        elif target[0] - current[0] > 0: #moved east
            self.heading += 90
        elif target[0] - current[0] < 0: #moved west
            self.heading -= 90
        
        self.heading %= 360
        if self.heading < 0:
            self.heading += 360
        
        self.position = target
        #update position
    
    #==================== face_to function ====================#
    def face_coordinate(self, xp: float, yp: float):
        # map possible directions
        relative_x = xp - self.position[0]
        relative_y = yp - self.position[1]
        
        if relative_x == 0 and relative_y == 0:
            return
        
        angle_to_rotate = 0
        if relative_x == 0:
            if relative_y < 0:
                angle_to_rotate = 180
        else:
            angle_to_rotate = math.atan(relative_y / relative_x)
            
            if relative_x < 0:
                angle_to_rotate += 180
            elif relative_y < 0 and relative_x > 0:
                angle_to_rotate += 360
            
            angle_to_rotate -= 90
                        
            if angle_to_rotate < 0:
                angle_to_rotate += 360
            
            angle_to_rotate = 360 - angle_to_rotate
        
        # calculate angles to rotate
        angle_to_rotate = self.heading - angle_to_rotate
        self.rotate_angle(angle_to_rotate, 5)
    
    ############# main body of robot navigation action #############
    ### explanation: robot mainly follow the actions in this function when fixed_map_navigate_to function is called
    # action 1: Call BFS to find the optimal path
    # action 2: Play sound to show the robot starts moving
    # action 3: Follow the optimal path by using robot.navigate_to function (length between two points is defined by unit_length)
    # action 4: Play sound to show the robot finishes moving
    # action 5: Print "Navigation completed!"

    # async def fixed_map_navigate_to(self, room_map, target):
    def fixed_map_navigate_to(self, target):
        try:
            # action 1
            cur_pos = [self.position[0], self.position[1]]
            start = [cur_pos.x, cur_pos.y]
            path = self.BFS(self.ROOM_MAP, start, target)
            print ("Path: ", path)

            # action 2
            #await self.play_sound('start_move')

            # action 3
            for i in range (0,len(path)):
                x = path[i][0]
                y = path[i][1]
                self.navigate_to(false, x*self.UNIT_LENGTH, y*self.UNIT_LENGTH, 0, 0, 0, 0)
                self.update_positional_status(self.position, path[i])
                

            # action 4
            #await self.play_sound('stop_move')

            # action 5
            print("Navigation completed!")
        except Exception as e:
            print("Error when navigating:", e)


    #==================== drive_distance function ====================#
    def drive_distance(self, meters: Union[float, int] , speed:[float, int]):
        self.position[0] += meters * math.cos(self.heading)
        self.position[1] += meters * math.sin(self.heading)
        self.position[0] /= self.UNIT_LENGTH
        self.position[1] /= self.UNIT_LENGTH
        self.drive_distance_helper(meters, speed)

    #==================== rotate_angle function ====================#
    def rotate_angle(self, degrees: Union[float, int], rotation_speed: Union[float, int]):
        self.heading += degrees
        self.heading %= 360
        if self.heading < 0:
            self.heading += 360
        radians = (degrees * math.pi) / 180
        self.rotate_angle_helper(radians, rotation_speed)
