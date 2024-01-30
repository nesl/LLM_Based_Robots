# #
# # Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2022 iRobot Corporation. All rights reserved.
# #

# from irobot_edu_sdk.backend.bluetooth import Bluetooth
# from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
# from irobot_edu_sdk.music import Note


# robot = Create3(Bluetooth("iRobotCreate3", "47682A24-F400-A918-B4A0-08822B3A25F4"))

# POLL_SENSOR = True # Try changing this to compare the speed of events vs polling

# @event(robot.when_play)
# async def play(robot):
#     # print('Dock')
#     # print(await robot.dock())
#     # print('get_docking_values:', await robot.get_docking_values())

#     distance = 20
#     await robot.move(-20)

#     # while True:
#     #     if POLL_SENSOR:
#     #         sensor = (await robot.get_docking_values())['IR sensor 0']
#     #     else:
#     #         sensor = robot.docking_sensor.sensors[0]
#     #         if sensor == None: # no event yet received
#     #             sensor = 0
#     #     r = 255 * ((sensor & 8)/8)
#     #     g = 255 * ((sensor & 4)/4)
#     #     b = 255 * (sensor & 1)
#     #     await robot.set_lights_on_rgb(r, g, b)

# # @event(robot.when_play)
# # async def play(robot):
# #     # Trigger an undock and then dock. Try putting this in an infinite loop!
# #     print('Undock')
# #     print(await robot.undock())
# #     print('get_docking_values:', await robot.get_docking_values())
# #     # print('Dock')
# #     # print(await robot.dock())
# #     # print('get_docking_values:', await robot.get_docking_values())


# robot.play()

# # step 1: try parallel when_play, ie first undock and then dock
# # step 2: if working, modify robot class 
# # step 3: if not working, modify logic of play


from robotclass import Robot

room_map = [['E','B','B','B'],['E','E','E','B'],['B','B','E','B'],['B','E','E','E']]
robot = Robot()
# robot.robot_undock()
# robot.robot_dock()
robot.fixed_map_navigate_to(room_map, [2, 2])
# robot.navigate([0,0],[0,1])
# robot.fixed_map_navigate_to(room_map, [0, 0])
# robot.robot_finish_moving()
robot.start_action()

