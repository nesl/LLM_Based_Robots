class RobotFunctions:
    
    script_file = '/home/nesl/RobotROS2.sh'

    def __init__(self):
        import subprocess
        import numpy as np
        self.subprocess = subprocess
        self.np = np

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

    def drive_distance(self, distance:"np.float32", max_translation_speed: "np.float32"):
        command='drive_distance'
        output=self.subprocess.run([self.script_file, command, str(distance), str(max_translation_speed)], capture_output=True, text=True)
        if output.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with return code:", output.returncode)
            print("Error output:", output.stderr)

    def rotate_angle(self, angle: "np.float32", max_rotation_speed: "np.float32"):
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
'''
while True:
    input_string=input("Next instruction: ")
    print("command copied")
    try:
        # Extract the function name
        function_name = input_string[:input_string.index('(')]

    	# Extract the arguments
        if input_string.index('(')+1 != input_string.index(')'):
            arguments = input_string[input_string.index('(')+1:input_string.index(')')].split(',')
        else:
            arguments = ''
        
        # Strip whitespace from arguments
        arguments = [arg.strip() for arg in arguments]
        # Call the function dynamically
        functions = RobotFunctions()
        function = getattr(functions, function_name)
        function(*arguments)
	
    except Exception as e:
    	# Handle the exception
    	print("An error occurred: ", e)
'''
