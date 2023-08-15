#!/bin/bash
argument=$1
if [ "$argument" = "dock" ]; then
    ros2 action send_goal /dock irobot_create_msgs/action/DockServo "{}"
elif [ "$argument" = "undock" ]; then
    ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"
elif [ "$argument" = "drive_arc" ]; then
    EXPECTED_ARGS=5
    if [ $# -ne $EXPECTED_ARGS ]; then
        echo "Error: wrong number of arguments"
        exit 1
    else
        ros2 action send_goal /drive_arc irobot_create_msgs/action/DriveArc "{angle: $2,radius: $3,translate_direction: $4,max_translation_speed: $5}"
    fi
elif [ "$argument" = "drive_distance" ]; then
    EXPECTED_ARGS=3
    if [ $# -ne $EXPECTED_ARGS ]; then
        echo "Error: wrong number of arguments"
        exit 1
    else
        ros2 action send_goal /drive_distance irobot_create_msgs/action/DriveDistance "{distance: $2,max_translation_speed: $3}"
    fi
elif [ "$argument" = "navigate_to_position" ]; then
    EXPECTED_ARGS=9
    if [ $# -ne $EXPECTED_ARGS ]; then
        echo "Error: wrong number of arguments"
        exit 1
    else
        ros2 action send_goal /navigate_to_position irobot_create_msgs/action/NavigateToPosition "{achieve_goal_heading: $2,goal_pose:{pose:{position:{x: $3,y: $4,z: $5}, orientation:{x: $6,y: $7, z: $8, w: $9}}}}"
    fi
elif [ "$argument" = "rotate_angle" ]; then
    EXPECTED_ARGS=3
    if [ $# -ne $EXPECTED_ARGS ]; then
        echo "Error: wrong number of arguments"
        exit 1
    else
        ros2 action send_goal /rotate_angle irobot_create_msgs/action/RotateAngle "{angle: $2,max_rotation_speed: $3}"
    fi
elif [ "$argument" = "wall_follow" ]; then
    EXPECTED_ARGS=4
    if [ $# -ne $EXPECTED_ARGS ]; then
        echo "Error: wrong number of arguments"
        exit 1
    else
        ros2 action send_goal /wall_follow irobot_create_msgs/action/WallFollow "{follow_side: $2, max_runtime: {sec: $3, nanosec: $4}}"
    fi
fi
    



