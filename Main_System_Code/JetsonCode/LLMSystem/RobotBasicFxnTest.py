from robotclass import Create3Robot 
import pandas as pd
import time

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
robot = Create3Robot()

# Create an empty DataFrame
df = pd.DataFrame(columns=['start_time', 'end_time', 'time_cost'])
# 1. turn
turn_row = []
start_time = time.time()
turn_row.append(start_time)
robot.turn_left(90)
end_time = time.time()
turn_row.append(end_time)
time_cost = end_time - start_time
turn_row.append(time_cost)
print("turn left 90:", turn_row)
df.loc['turn left 90'] = turn_row

turn_row = []
start_time = time.time()
turn_row.append(start_time)
robot.turn_left(180)
end_time = time.time()
turn_row.append(end_time)
time_cost = end_time - start_time
turn_row.append(time_cost)
print("turn left 180:", turn_row)
df.loc['turn left 180'] = turn_row

turn_row = []
start_time = time.time()
turn_row.append(start_time)
robot.turn_left(270)
end_time = time.time()
turn_row.append(end_time)
time_cost = end_time - start_time
turn_row.append(time_cost)
print("turn left 270:", turn_row)
df.loc['turn left 270'] = turn_row

turn_row = []
start_time = time.time()
turn_row.append(start_time)
robot.turn_left(360)
end_time = time.time()
turn_row.append(end_time)
time_cost = end_time - start_time
turn_row.append(time_cost)
print("turn left 360:", turn_row)
df.loc['turn left 360'] = turn_row

turn_row = []
start_time = time.time()
turn_row.append(start_time)
robot.turn_right(90)
end_time = time.time()
turn_row.append(end_time)
time_cost = end_time - start_time
turn_row.append(time_cost)
print("turn right 90:", turn_row)
df.loc['turn right 90'] = turn_row

turn_row = []
start_time = time.time()
turn_row.append(start_time)
robot.turn_right(180)
end_time = time.time()
turn_row.append(end_time)
time_cost = end_time - start_time
turn_row.append(time_cost)
print("turn right 180:", turn_row)
df.loc['turn right 180'] = turn_row

turn_row = []
start_time = time.time()
turn_row.append(start_time)
robot.turn_right(270)
end_time = time.time()
turn_row.append(end_time)
time_cost = end_time - start_time
turn_row.append(time_cost)
print("turn right 270:", turn_row)
df.loc['turn right 270'] = turn_row

turn_row = []
start_time = time.time()
turn_row.append(start_time)
robot.turn_right(270)
end_time = time.time()
turn_row.append(end_time)
time_cost = end_time - start_time
turn_row.append(time_cost)
print("turn right 360:", turn_row)
df.loc['turn right 360'] = turn_row

robot.turn_left(90)

# navigate
for distance in range (5, 25, 5):
    move_row = []
    start_time = time.time()
    move_row.append(start_time)
    robot.navigate([0,0], [0,distance], 0)
    end_time = time.time()
    move_row.append(end_time)
    time_cost = end_time - start_time
    move_row.append(time_cost)
    print("navigate straight{distance}:", move_row)
    df.loc['navigate straight {distance}'] = move_row

    # navigate one turn
for pos in range (1,6):
    move_row = []
    start_time = time.time()
    move_row.append(start_time)
    robot.navigate([0,0], [pos,0], 0)
    end_time = time.time()
    move_row.append(end_time)
    time_cost = end_time - start_time
    move_row.append(time_cost)
    print("navigate turn once {distance}:", move_row)
    df.loc['navigate turn once {distance}'] = move_row

    # navigate twice turn
for pos in range (1,6):
    move_row = []
    start_time = time.time()
    move_row.append(start_time)
    robot.navigate([0,0], [pos,pos], 0)
    end_time = time.time()
    move_row.append(end_time)
    time_cost = end_time - start_time
    move_row.append(time_cost)
    print("navigate turn twice {distance}:", move_row)
    df.loc['navigate turn twice {distance}'] = move_row

# BFS
BFS_row = []
start_time = time.time()
BFS_row.append(start_time)
robot.navigate_to(ROOM_MAP, [6,2])
end_time = time.time()
BFS_row.append(end_time)
time_cost = end_time - start_time
BFS_row.append(time_cost)
print("BFS time cost to pos[6,2]")
df.loc["BFS time cost to pos[6,2]"] = BFS_row

df.to_csv('RobotBasicFxnTestOutput.csv')






