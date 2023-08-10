#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

import math
from typing import Union
from struct import pack, unpack
from .backend.backend import Backend
from .completer import Completer
from .packet import Packet
from .utils import bound, stop_program
from .getter_types import IPv4Addresses, IrProximity, Pose
from irobot_edu_sdk.robot import Robot
import queue
from irobot_edu_sdk.music import Note


class Create3(Robot):
    """Create 3 robot object."""

    DOCK_STATUS_SUCCEEDED = 0
    DOCK_STATUS_ABORTED   = 1
    DOCK_STATUS_CANCELED  = 2
    DOCK_RESULT_UNDOCKED = 0
    DOCK_RESULT_DOCKED   = 1
    
    DIR = [0,1,0,-1,0]
    UNIT_LENGTH = 20

    def __init__(self, backend: Backend):
        super().__init__(backend=backend)

        # Getters.
        self.ipv4_address = IPv4Addresses()
        self.position = [0,0]
        #self.heading = 0

        #update position and heading -- read from a text file containing three numbers -- first two for position and third for heading
        output = readData('odometryData.txt') #may need to update file name later
        self.position[0] = int(output[0])
        self.position[1] = int(output[1])
        self.heading = int(output[2])
    

    #file manipulation functions
    def clearData(file_path):   #makes text file empty -- necessary for overriding contents
        with open(file_path, 'w') as file:
            file.write('')

    def writeData(file_path, data):  #adds contents to text file via appending
        with open(file_path, 'a') as file:
            file.write(data)

    def readData(file_path):  #stores every line in the text file as an element in a list
        with open(file_path, 'r') as file:
            data = file.readlines()
            return data
            
    def updateOdometry():
        clearData('odometryData.txt')
        data = [self.position[0], self.position[1], self.heading]
        for i in data:
            writeData('odometryData.txt', str(i) + '\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    async def get_ipv4_address(self) -> IPv4Addresses:
        """Get the robot's ipv4 address as a IPv4Addresses, which contains wlan0, wlan1 and usb0. Returns None if anything went wrong."""
        dev, cmd, inc = 100, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            self.ipv4_address.wlan0 = [packet.payload[0], packet.payload[1], packet.payload[2], packet.payload[3]]
            self.ipv4_address.wlan1 = [packet.payload[4], packet.payload[5], packet.payload[6], packet.payload[7]]
            self.ipv4_address.usb0 = [packet.payload[8], packet.payload[9], packet.payload[10], packet.payload[11]]
            return self.ipv4_address
        return None

    async def get_ir_proximity(self):
        dev, cmd, inc = 11, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            unpacked = unpack('>IHHHHHH', packet.payload)
            ir_proximity = IrProximity()
            ir_proximity.sensors = list(unpacked[1:])
            return ir_proximity
        return None

    async def get_packed_ir_proximity(self):
        """Get Packed IR Proximity Values and States"""
        dev, cmd, inc = 11, 2, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            payload = packet.payload
            timestamp = unpack('>I', payload[0:4])[0]
            ir_proximity = IrProximity()
            #ir_proximity.state = payload[4]
            ir_proximity.sensors = [
                (payload[ 5] << 4) + (payload[12] >> 4),
                (payload[ 6] << 4) + (payload[12] & 0xF),
                (payload[ 7] << 4) + (payload[13] >> 4),
                (payload[ 8] << 4) + (payload[13] & 0xF),
                (payload[ 9] << 4) + (payload[14] >> 4),
                (payload[10] << 4) + (payload[14] & 0xF),
                (payload[11] << 4) + (payload[15] >> 4),
            ]
            return ir_proximity
        return None

    async def get_position(self):
        dev, cmd, inc = 1, 16, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            payload = packet.payload
            timestamp = unpack('>I', payload[0:4])[0]
            x = unpack('>i', payload[4:8])[0]
            y = unpack('>i', payload[8:12])[0]
            heading = unpack('>h', payload[12:14])[0] / 10
            return Pose(x, y, heading)
        return None

    async def reset_navigation(self):
        await self._backend.write_packet(Packet(1, 15, self.inc))

    async def navigate_to(self, x: Union[int, float], y: Union[int, float], heading: Union[int, float] = None):
        """ If heading is None, then it will be ignored, and the robot will arrive to its destination
        pointing towards the direction of the line between the destination and the origin points.
        Units:
            x, y: cm
            heading: deg
        """
        if self._disable_motors:
            return
        dev, cmd, inc = 1, 17, self.inc
        _heading = -1
        if heading is not None:
            _heading = int(heading * 10)
            _heading = bound(_heading, 0, 3599)
        payload = pack('>iih', int(x * 10), int(y * 10), _heading)
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc, payload))
        timeout = self.DEFAULT_TIMEOUT + int(math.sqrt(x * x + y * y) / 10) + 4  # 4 is the timeout for a potential rotation.
        await completer.wait(timeout)
        
    #==================== sound action mapping ====================#
    ### explanation: Define different sounds for different actions of the robot.
    async def play_sound(self, action):
        try:
            if action == 'start_move':
                await super().play_note(Note.A4, 0.5)
            elif action == 'stop_move':
                await super().play_note(Note.A4_SHARP, 0.5)
            elif action == 'dock':
                await super().play_note(Note.C4, 0.5)
            elif action == 'undock':
                await super().play_note(Note.C4_SHARP, 0.5)
        except Exception as e:
            print("Error when playing sound:", e)
        
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
    def face_coordinate(self, float32 xp, float32 yp):
        # map possible directions
        relative_x = xp - self.position[0]
        relative_y = yp - self.position[1]
        
        if relative_x == 0 && relative_y == 0: return
        
        angle_to_rotate = 0
        if relative_x == 0:
            if relative_y < 0:
                angle_to_rotate = 180
        else:
            angle_to_rotate = math.atan(relative_y / relative_x)
            
            if relative_x < 0:
                angle_to_rotate += 180
            elif relative_y < 0 && relative_x > 0:
                angle_to_rotate += 360
            
            angle_to_rotate -= 90
                        
            if angle_to_rotate < 0:
                angle_to_rotate += 360
            
            angle_to_rotate = 360 - angle_to_rotate
        
        # calculate angles to rotate
        angle_to_rotate = self.heading - angle_to_rotate
        self.rotate_angle(angle_to_rotate)

        # update self.heading
        self.heading += angle_to_rotate
        self.heading %= 360
        if self.heading < 0:
            self.heading += 360
    
    ############# main body of robot navigation action #############
    ### explanation: robot mainly follow the actions in this function when fixed_map_navigate_to function is called
    # action 1: Call BFS to find the optimal path
    # action 2: Play sound to show the robot starts moving
    # action 3: Follow the optimal path by using robot.navigate_to function (length between two points is defined by unit_length)
    # action 4: Play sound to show the robot finishes moving
    # action 5: Print "Navigation completed!"

    async def fixed_map_navigate_to(self, room_map, target):
        try:
            # action 1
            cur_pos = await self.get_position()
            start = [cur_pos.x, cur_pos.y]
            path = self.BFS(room_map, start, target)
            print ("Path: ", path)

            # action 2
            await self.play_sound('start_move')

            # action 3
            for i in range (0,len(path)):
                x = path[i][0]
                y = path[i][1]
                await self.navigate_to(x*self.UNIT_LENGTH, y*self.UNIT_LENGTH, heading = None)
                updatePositionalStatus(self.position, path[i])
                

            # action 4
            await self.play_sound('stop_move')

            # action 5
            print("Navigation completed!")
        except Exception as e:
            print("Error when navigating:", e)


    #==================== drive_distance function ====================#
    async def drive_distance(self, meters: Union[float, int] , speed:[float, int]):
        self.position[0] += meters * math.cos(heading)
        self.position[1] += meters * math.sin(heading)
        self.position[0] /= UNIT_LENGTH
        self.position[1] /= UNIT_LENGTH
        centimeters = meters*100
        motor_speed = speed*5
        await super().set_wheel_speeds(motor_speed, motor_speed)
        await super().move(centimeters)

    #==================== rotate_angle function ====================#
    async def rotate_angle(self, degrees: Union[float, int], rotation_speed: Union[float, int]):
        self.heading += degrees
        self.heading %= 360
        if self.heading < 0:
            self.heading += 360
        motor_speed = rotation_speed*5
        if (degrees >= 0):
            await super().set_left_speed(motor_speed)
        else:
            await super().set_right_speed(motor_speed)
        await super().turn_right(degrees)

    async def dock(self):
        """Request a docking action."""
        dev, cmd, inc = 1, 19, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(60)
        if packet:
            unpacked = unpack('>IBBHHHHH', packet.payload)
            return {'timestamp': unpacked[0], 'status': unpacked[1], 'result': unpacked[2]}
        return None

    async def undock(self):
        """Request an undocking action."""
        dev, cmd, inc = 1, 20, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(30)
        if packet:
            unpacked = unpack('>IBBHHHHH', packet.payload)
            return {'timestamp': unpacked[0], 'status': unpacked[1], 'result': unpacked[2]}
        return None

    async def get_docking_values(self):
        """Get docking values."""
        dev, cmd, inc = 19, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            unpacked = unpack('>IBBBBHHHH', packet.payload)
            return {'timestamp': unpacked[0], 'contacts': unpacked[1], 'IR sensor 0': unpacked[2],
                    'IR sensor 1': unpacked[3], 'IR sensor 2': unpacked[4]}
        return None

    async def get_version_string(self) -> str:
        """Get version as a human-readable string."""
        ver = await self.get_versions(0xA5)
        try:
            major = ver[1]
            minor = ver[2]
            patch = ver[9]
            if major < 32 or major > 126:
                major = str(major)
            else:
                major = chr(major)

            return '.'.join([major, str(ver[2]), str(ver[9])])
        except IndexError:
            return None;

