# <a name="_dp1pvo7e969g"></a>Overall Project Goals and Description:
### <a name="_wsd4gpfpx9lo"></a>Research Question / Purpose
How viable is the method of using LLMs to control robots?

Research Question/Goal: Create a framework that incorporates an LLM into a robotic system to serve as the central reasoning node.
Then evaluate how LLMs work in real-time, resource-constrained environments that are often characteristic of home automation and personalized robotics.
—----------------------------------------------------------------------------------------------------------------------------

Three main phases in the Project:

- Action (Get Robot to work)
- Sensing (Integrate Sensors)
- Intelligence (LLM)

# <a name="_j2xgk1o4oxgt"></a>Flow Chart


# <a name="_2mm3fcg06im1"></a>Hardware
- Create 3 Robot
  - [7 IR Obstacle Sensors](https://iroboteducation.github.io/create3_docs/hw/data/ir_sensors_drawing.svg) in the front
    - Can be used to detect obstacles
  - Three Buttons on top
    - Can be overloaded using ROS 2 application
    - Power Button features ring of 6 RGB LEDs for indication
  - Multi-Zone Bumper
  - Docking Sensor
  - [Adapter Board](https://iroboteducation.github.io/create3_docs/hw/adapter/) below Faceplate
    - Main Purpose: Used to interface to external computers either through Bluetooth or via USB-C
    - Unregulated Battery Port (~14 V at 2 A max)
    - USB-C Connector: USB 2.0 Host connection into robot with 5.13 V at 3.0 A provided to power downstream connections. Power is disabled on this port unless a proper USB-C device is connected.
    - USB/BLE Toggle routes the robot's single USB Host connection to either the USB-C port or to the on-board Bluetooth Low Energy module.
  - Faceplate + Cargo Bay
    - Regular hole pattern for attaching payloads
  - 4 Cliff sensors
    - Keeps robot on ground
  - Optical Odometry Sensor 
  - IMU
- Nvidia Jetson AGX Xavier Development Kit
  - CPU structure:
  - GPU structure:
- Desktop Machine
  - CPU structure:
  - GPU structure:
- Raspberry Pi (Optional)

- Intel Realsense LiDar Camera L515
  - Depth camera
  - RGB camera

check rest of the list
  - Gyroscope?


# <a name="_lurn8zysr1yz"></a>
# <a name="_7m57xmegjlky"></a>Software Setup Steps
This section describes all the required setup steps for the devices and also installing the necessary programs such as the LLMs.
### <a name="_w6bxqfk0gqed"></a>**Nvidia Jetson AGX Xavier Developer Kit:**
1. Install Jetpack 5.1.1 using SDK Manager (make sure installation occurring on 18.04 device)
   1. Install to NVMe to utilize SSD as main path
   1. Once installation done, make sure that Ubuntu version on Jetson is 20.04
   1. [AGX Developer Manual](https://developer.download.nvidia.com/embedded/L4T/r32-3-1_Release_v1.0/jetson_agx_xavier_developer_kit_user_guide.pdf?t=eyJscyI6InJlZiIsImxzZCI6IlJFRi1pcm9ib3RlZHVjYXRpb24uZ2l0aHViLmlvLyJ9)
1. Setup to install everything (and all packages) on the SSD.

Ethan finish
1. Install Whisper
### <a name="_wz48jhjac9c"></a>**ROS 2 Galactic:** 
1. [ROS 2 Installation (using Binary Packages)](https://docs.ros.org/en/galactic/Installation/Ubuntu-Install-Debians.html)
1. [Configure ROS 2 Environment](https://docs.ros.org/en/galactic/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)
1. [Create 3 ROS 2 Setup](https://iroboteducation.github.io/create3_docs/setup/ubuntu2004/)
1. [Nvidia Jetson Setup with Create 3](https://iroboteducation.github.io/create3_docs/setup/jetson/)
1. Test Run
   1. Make sure to run “source /opt/ros/galactic/setup.bash” and “export ROS\_DOMAIN\_ID=0”
   1. [Run Docking and Undocking Commands](https://iroboteducation.github.io/create3_docs/api/docking/)
### <a name="_ipoi7k53nfal"></a>**Create 3 Robot**
1. [Create 3 Initial Software Update](https://edu.irobot.com/create3-setup)
1. [Create 3 ROS 2 Setup](https://iroboteducation.github.io/create3_docs/setup/ubuntu2004/)
### <a name="_kixv8wiff98"></a>**LiDar L515**
1. [Intel Realsense connect to jetson](https://dev.intelrealsense.com/docs/nvidia-jetson-tx2-installation)
1. [Intel Realsense Python Wrapper installation](https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python)
   1. [Python Package Installation (pyrealsense2)](https://pypi.org/project/pyrealsense2/)
### <a name="_vfo2xrqkgcq8"></a>**Desktop Machine**
1. [Install Pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line)
1. [Install Cuda](https://developer.nvidia.com/cuda-downloads)
1. [Install Pytorch](https://pytorch.org/get-started/locally/)
1. [Install Numpy](https://numpy.org/install/)
   1. pip install numpy
1. [Install transformers](https://pypi.org/project/transformers/)
   1. pip install transformers
1. Install LLM
   1. python3
   1. Type in commands under “Load Model Directly” in [here](https://huggingface.co/WizardLM/WizardCoder-15B-V1.0)
### <a name="_mdzbkvsxfwrk"></a>**Raspberry Pi (Optional):**
1. Setup the Raspberry Pi
   1. Install 64-bit Raspbian OS
1. Download WhisperAI files from Github Repository: [GitHub - openai/whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://github.com/openai/whisper) 
1. Test Python Example Code on ThonnyIDE


# <a name="_u5tjiebpdhq1"></a>Steps To Work on Project
1. Connect Create 3 Robot to Wifi using [these steps](https://edu.irobot.com/create3-setup)
1. Go to Terminal
   1. Type “source /opt/ros/galactic/setup.bash”
   1. Type “export ROS\_DOMAIN\_ID=<your\_domain\_id>” (in our case, 0)
1. To open
