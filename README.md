# <a name="_dp1pvo7e969g"></a>Overall Project Goals and Description:
### <a name="_wsd4gpfpx9lo"></a>Research Question / Purpose
How viable is the method of using LLMs to control robots?

Research Question/Goal: Integrate 2 LLMs to create a robotic system that receives human speech prompts and aids in performing daily life tasks. Test the capabilities, advantages, and limitations of such a system. 

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


# <a name="_rq48s2ghwvnh"></a>Overall Flowchart of Robot Interface / Execution
Nodes:

- Create-3
- NVIDIA Jetson AGX
- LIDAR Camera
- Microphone Array
- Desktop Machine

Overall Process:

- Input: Microphone → Desktop → Command String (text file, etc.)
- Processing: Desktop + Command String → Create Prompt → LLM → Generate Output Code
- Execution: Output Code → Grabbed by Jetson → Executed (on Create 3, LiDar, etc.)
  - If error, retry code generation

Prompt Engineering:

- Microphone Input (What did the User Say?)
- Add set list of functions/APIs

3 (+1) Computers

- Desktop
  - Main LLM
  - Receives prompt and function descriptions (in English)
- Jetson
  - Lidar – OpenCV + YOLO Object Recognition
  - Microphone – Whisper AI
  - USB Speaker – Some text to speech LLM
  - Communicating with Desktop
  - Houses APIs (in code form)
- Robot
  - Communicates with Desktop
- Raspberry Pi (Optional)


# <a name="_u5tjiebpdhq1"></a>Steps To Work on Project
1. Connect Create 3 Robot to Wifi using [these steps](https://edu.irobot.com/create3-setup)
1. Go to Terminal
   1. Type “source /opt/ros/galactic/setup.bash”
   1. Type “export ROS\_DOMAIN\_ID=<your\_domain\_id>” (in our case, 0)
1. To open

# <a name="_szlqy2n8cbw"></a>General Links:
### <a name="_58wk7hfvy6ky"></a>Nvidia Jetson:
- [AGX Developer Manual](https://developer.download.nvidia.com/embedded/L4T/r32-3-1_Release_v1.0/jetson_agx_xavier_developer_kit_user_guide.pdf?t=eyJscyI6InJlZiIsImxzZCI6IlJFRi1pcm9ib3RlZHVjYXRpb24uZ2l0aHViLmlvLyJ9)
- [Nvidia Jetson Linux](https://developer.nvidia.com/embedded/jetson-linux)
- [Nvidia Jetpack Information](https://developer.nvidia.com/embedded/jetpack)
- [Specs](https://elinux.org/Jetson_AGX_Xavier)
### <a name="_43vo509xsoz9"></a>Create 3 Robot:
- [Create 3 Robot Setup](https://edu.irobot.com/create3-setup)
- [Create3 galactic environment setup](https://iroboteducation.github.io/create3_docs/setup/ubuntu2004/)
- [Create 3 Learning Library](https://edu.irobot.com/learning-library?robotValue=Advanced%20Create%203%20Robot&toggle=lessons)
- [Create 3 Docs](https://iroboteducation.github.io/create3_docs/)
- [Create 3 Setup Video](https://www.youtube.com/watch?v=UeLHrAvZ_h0)
### <a name="_coij5y6249ow"></a>Other Sensors / Electronics:
- [LiDar camera (Intel Realsense L515)](https://www.intelrealsense.com/lidar-camera-l515/)
- [Intel Realsense with ROS](https://dev.intelrealsense.com/docs/ros-wrapper?_ga=2.42215591.38238678.1687886906-1916588351.1687886906)
- [Intel Realsense Overall (Intel website)](https://www.intelrealsense.com/sdk-2/)
- [Intel realsense connect to jetson](https://dev.intelrealsense.com/docs/nvidia-jetson-tx2-installation)
- https://intelrealsense.github.io/librealsense/python\_docs/\_generated/pyrealsense2.html
### <a name="_7xsf9smccxwv"></a>LLMs:
- [AI (/LLM) Leaderboard](https://huggingface.co/spaces/mike-ravkine/can-ai-code-results)
- [StarChat Playground](https://huggingface.co/spaces/HuggingFaceH4/starchat-playground)
- [Connect Raspberry Pi to Create 3](https://jimbobbennett.dev/blogs/irobot-create3-connect-a-pi/)
- [Whisper AI](https://platform.openai.com/docs/models/whisper)
- [Whisper Paper](https://arxiv.org/abs/2306.08568)
- [Wizard LM](https://github.com/nlpxucan/WizardLM/tree/main/WizardCoder)
### <a name="_91gnzzlbwlfo"></a>ROS 2
- [ROS 2 Distributions](https://docs.ros.org/en/rolling/Releases.html)
- [Intro to ROS](https://www.toptal.com/robotics/introduction-to-robot-operating-system)
- <https://github.com/IntelRealSense/realsense-ros#installation-instructions>
### <a name="_1rge0cxylwci"></a>Tutorials
- [ROS Tutorials](http://wiki.ros.org/ROS/Tutorials)
- [tf2 Tutorials](http://wiki.ros.org/tf2/Tutorials)
- [Understanding ROS](https://docs.ros.org/en/rolling/Tutorials.html)
- [Install ROS to AGX](https://www.youtube.com/watch?v=HjFs00rrJfY)
- [Getting Started with the Create 3® Educational Robot](https://www.youtube.com/watch?v=UeLHrAvZ_h0)

### <a name="_35ws8hg0fki8"></a>Audio/Raspberry PI:
- [GitHub - openai/whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://github.com/openai/whisper) 
- [How do I run Whisper on a Raspberry Pi 4B? · openai whisper · Discussion #1304 · GitHub](https://github.com/openai/whisper/discussions/1304) 
- [ReSpeaker Mic Array v2.0 | Seeed Studio Wiki](https://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/#extract-voice) 
### <a name="_mnmb6lxjpm0i"></a>Other Resources:
- Ubuntu 22.04 OS Installation: <https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview> 
### <a name="_xwz4675yuvvg"></a>Lab Related:
- [Key Form](https://www.ee.ucla.edu/wp-content/uploads/ee/HSSEAS-Key-Request-Form-2012.pdf)
