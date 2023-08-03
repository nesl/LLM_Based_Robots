#--------------------------------------------  Import libraries  --------------------------------------------#
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3
from irobot_edu_sdk.utils import stop_program

robot = Create3(Bluetooth())

@event(robot.when_play)
async def play(robot):
    await robot.rotate_angle(-180, 10)
    await robot.rotate_angle(-180, 1)
    # await robot.drive_distance(0.2, 0.001)
    # await robot.drive_distance(0.2, 10)
    # await robot.drive_distance(0.2, 10)
    stop_program()
robot.play()