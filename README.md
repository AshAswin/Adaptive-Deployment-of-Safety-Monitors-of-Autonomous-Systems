# Adaptive-Deployment-of-Safety-Monitors-for-Autonomous-Systems

![alt text](https://www.materialhandling247.com/images/product/righthand-robotics-rightpick-robot-arm-3.jpg)

Adaptive deployment of safety monitors for autonomous systems solves the problem of deploying safety critical software for an autonomous system. The software can be re-deployed by the robots autonomously at runtime that accounts for changing requirements urged by their task, platform and environment [1]. The problem is formulated as a Constraint Satisfaction Problem (CSP). Constraint Satisfaction Problems are mathematical questions defined as a set of objects whose state must satisfy a number of constraints or limitations [2]. It is achieved using a library called **[MiniZinc](https://www.minizinc.org/)**.

Minizinc is a free and open source constraint modeling language. It can be used to model constraint satisfaction and optimization problems in a higher level. 

# Dependencies:
 - Python (>= 3.6)
 - Minizinc (2.4.3)
 - Pandas (1.0.7)

# Minizinc as an IDE:
Minizinc comes with a simple Integrated Development Environment (IDE), which makes it easier for developing and executing constraint models. It is user friendly.

Minizinc can be installed as bundled package that consists of Minizinc library, IDE, solvers and interfaces.

To install the bundled package, download it from [here](https://www.minizinc.org/software.html) 

OS specific downloads -
- Windows - [Click Here](https://github.com/MiniZinc/MiniZincIDE/releases/download/2.4.3/MiniZincIDE-2.4.3-bundled-setup-win64.exe)
- Linux - [Click Here](https://github.com/MiniZinc/MiniZincIDE/releases/download/2.4.3/MiniZincIDE-2.4.3-bundle-linux-x86_64.tgz)
- Mac OS - [Click Here](https://github.com/MiniZinc/MiniZincIDE/releases/download/2.4.3/MiniZincIDE-2.4.3-bundled.dmg)

For more information regarding installation, Visit [Minizinc Documentation.](https://www.minizinc.org/doc-2.4.3/en/installation.html)

# Minizinc Python:
It is a python package that allows accessing all of Minizinc's functionalities directly from Python. It provides an interface from Python to MiniZinc driver. It provides easy access to Minizinc using native Python structures.

# User Installation:
Use pip to install the Minizinc for Python -
```sh
pip install minizinc
```
For more information, Visit [PyPI.org](https://pypi.org/project/minizinc/)

The constraints are defined in the minizinc (.mzn) files. The .mzn files can be integrated with python using the python library for minizinc. The constraints can be solved using various solvers and it returns the best assignment or solution that satisfies the given constraints.

## How to use it:
**Files**
- The safety monitors, sensors and platforms are available as enumerations in **custom_dtypes.py**
- Constraints are defined in **platforms.mzn**. It consists of the CSP part and outputs the best suitable platform for deployment.
- The data for platforms.mzn to work is given in **platforms.dzn** which contains platform names and its properties.
- **input.csv** contains the list of robot’s context at every intervals along with memory available at each platform. 
    - **Example**: The current context is (True, True) => (gripper_status “False = Closed or True-Open”, robot_in_motion “True = Not stationary or False = stationary”)
- The actual implementation is provided in **adaptive_deployment.py**

**Usage** 
- Clone the repository to the local machine using ```git clone.```
- Install the requirements.
- Make sure Python 3 is installed followed by pandas and minizinc packages. (Note: It doesn’t work with Python 2)
- Make sure that files such as platforms.mzn, platforms.dzn, custom_dtypes.py, input.csv lies in the same directory.
- Execute adaptive_deployment.py file. Provide the name of the Minizn platform model as a command line argument.
```sh
python adaptive_deployment.py  --model platforms.mzn --input_data input.csv
```

# References:
[1]. Hochgeschwender, Nico. “Adaptive Deployment of Safety Monitors for Autonomous Systems.” International Conference on Computer Safety, Reliability, and Security, 2019, pp. 346–357. <br>
[2] https://en.wikipedia.org/wiki/Constraint_satisfaction_problem 
