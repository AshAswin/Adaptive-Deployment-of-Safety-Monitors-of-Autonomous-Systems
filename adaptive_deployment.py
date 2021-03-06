# General Skeleton for Adaptive Deployment of Safety Monitors

from abc import ABC, abstractmethod
from custom_dtypes import *
from minizinc import Instance, Model, Solver
import argparse
import pandas
import time
from tabulate import tabulate

class Context_Monitor:
    """
    Provide the contextual information needed for selection and deployment.
    """

    def __init__(self, repo_image):
        self.__gripper_status = False
        self.__robot_in_motion = False
        self.__time_stamp = 0.0
        self.__repo_image = repo_image

    def get_robot_status(self):
        """
        This method is used to read the current status of the gripper and robot motion.
        Parameters
        ----------
        **params : 
            None
        Returns
        -------
            None
        """

        self.__gripper_status = True
        self.__robot_in_motion = True

    def set_robot_status(self, current_context=(False, False)):
        """
        Set the parameters of this variables.
        This method is used to set the status of the gripper and robot motion.
        Parameters
        ----------
            current_context: (bool, bool)
        Returns
        -------
            None
        """

        self.__gripper_status = current_context[0]
        self.__robot_in_motion = current_context[1]

    def update_info_to_repo(self):
        """
        This method is used update the state of the robot in the repository method.
        Method takes the updated gripper and robot motion and updates. 
        Parameters
        ----------
        **params : 
            None
        Returns
        -------
            None
        """
        self.__repo_image.update_context(self.__gripper_status, self.__robot_in_motion)


class Repository():
    """
    Repository contains information for deployment. It is the central component in the architecture. Every components updates the information to the repository.
    """

    def __init__(self, active_safety_monitor=SafetyMonitor.NO_SELECTION, active_sensor=Sensors.NO_SELECTION,
                 current_context=[False, False], fixed_deployment=True,
                 safety_monitor_platform=Platforms.NO_SELECTION):
        self.__active_safety_monitor = active_safety_monitor
        self.__active_sensor = active_sensor
        self.__safety_monitor_platform = safety_monitor_platform
        self.__current_context = current_context
        self.__fixed_deployment = fixed_deployment
        #This attribute is added only to show that memory availability of every platform changes over time
        self.platforms_memory_availability = []
        self.force_sensor_presence = True
        self.min_tactile_sensor_count = 100
        self.min_memory_fused = 400
        self.fused_platform_min_latency = 5
        self.fused_platform_max_latency = 200
        self.force_sensor_type = 3
        self.n_platforms = 5
        self.platforms = set([1, 2, 3, 4, 5])

    def update_context(self, gripper_status, robot_motion):
        """
        Setter methods for updating current context, safety monitor and platform information 
        for deployment from other componenents. 
        Parameters
        ----------
        gripper_status: bool
            The gripper has status either true or false that means gripper is open or closed condition.
        robot_motion:
            The robot motion has status either true or false that means robot is moving or stopped.
        Returns
        -------
            None
        """
        self.__current_context = gripper_status, robot_motion
        print("Current_Context")
        print(tabulate([self.__current_context], headers=["GripperStatus","RobotMotion"],tablefmt="fancy_grid"))
        time.sleep(2)

    def update_current_safety_monitor(self, current_safety_monitor):
        """
        Setter methods for updating current active safety monitor and prints the selected safety monitor. 
        Parameters
        ----------
        current_safety_monitor: int
            The current_safety_monitor is the safety monitor that is currently active. 
            Each integer value represent unique safety monitor.
        Returns
        -------
            None
        """
        self.__active_safety_monitor = current_safety_monitor
        print("Selected_Safety_Monitor : {}".format(self.__active_safety_monitor))
        time.sleep(2)
    def update_platform_status(self, safety_monitor_platform):
        """
        Setter methods for updating current platform status and prints the selected safety monitor to deploy. 
        Parameters
        ----------
        safety_monitor_platform: int
            The safety_monitor_platform is the platform that needs to be deployed. 
            Each integer value represent unique platform.
        Returns
        -------
            None
        """
        self.__safety_monitor_platform = safety_monitor_platform

    def get_active_safety_monitor(self):
        """
        Getter methods for obtaining active safety monitor . 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            current active safety monitor
        """
        return self.__active_safety_monitor

    def get_current_context(self):
        """
        Getter methods for obtaining current context. 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            current context
        """
        return self.__current_context

    def __notify_changes(self):
        """
        This method is responsible for broadcasting changes in values to all modules in a system. This is not
        implemented as of now
        """
        pass

    def update_platform_memory_availability(self,current_memory_availability):
        """
        The update_platform_memory_availability method updates the memory availability of every platform

        Parameters
        ----------
        current_memory_availability: list of int
           current_memory_availability is a list containing memory availability value of every platform

        Returns
        -------
            None
        """
        self.platforms_memory_availability = current_memory_availability

class Selector(ABC):
    @abstractmethod
    def query_repository(self):
        """
        Query repository interface. 
        Interface for querying repository and acts as a communicator between repository and other components of the system.
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        pass

    @abstractmethod
    def update_repository(self):
        """
        Query repository interface. 
        Interface for updating repository and acts as a communicator between repository and other components of the system.
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        pass


class Safety_Monitor_Selector(Selector):
    """
    Contains definition for selecting the safety monitor based on the current context. The selected safety monitor information is updated in the repository.
    """

    def __init__(self, repo_image):
        """ 
        Initially the attributes are set to null and no safety monitor is selected by default.
        Current context contains gripper_status,robot_motion
        """
        self.__current_context = (False, False)
        self.__selected_safety_monitor = SafetyMonitor.NO_SELECTION
        self.__repo_image = repo_image

    def query_repository(self):
        """
        The query repository method update the current context by getting the current context from repository object. 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        self.__current_context = self.__repo_image.get_current_context()

    def select_safety_monitor(self):
        """
        The select safety monitor method checks the status of the current context of gripper and robot motion.
        Once the status has recieved appropriate safety monitor is passed onto the selected safety monitor variable. 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        if (self.__current_context == (True, True)):
            self.__selected_safety_monitor = SafetyMonitor.FORCE_SLIP

        elif (self.__current_context == (True, False)):
            self.__selected_safety_monitor = SafetyMonitor.TACTILE_SLIP

        else:
            self.__selected_safety_monitor = SafetyMonitor.FUSED_SLIP

    def update_repository(self):
        """
        The update_repository method updates the current safety monitor by extracting the selected safety monitor. 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        self.__repo_image.update_current_safety_monitor(self.__selected_safety_monitor)


class Platform_Selector(Selector):
    """
    Contains definition for selecting the platform based on the selected safety monitor.
    The selected platform information is updated in the repository.
    Checks and returns the platforms that satisfy the given requirements.
    It is achieved by solving Constraint Satisfaction Problem (CSP). CSP is implemented using MiniZinc(mzn) library.
    The requirements are formulated into suitable constraints and platforms that satisfy the given constraints will be selected.
    
    """

    def __init__(self, repo_image, minizinc_model):
        """
        Initially the attributes are set to null and no safety monitor and platform is selected by default.
        
        """
        self.__current_safety_monitor = SafetyMonitor.NO_SELECTION
        self.__repo_image = repo_image
        self.__platform = Platforms.NO_SELECTION
        self.__minizinc_model = minizinc_model
        self.__selected_platforms = None

    def query_repository(self):
        """
        The query_repository method get the active safety monitor and updates the current safety monitor. 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        self.__current_safety_monitor = self.__repo_image.get_active_safety_monitor()

    def select_deployment_platform(self):
        """
        The select deployment platform method get the selected paltform by calling platform selected method. 
        Once the paltform selected is obtained is compared with the current safety monitor and appropriate safety monitor
        is updated to the platform.
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        self.__selected_platforms = self.__platform_selected()
        if len(self.__selected_platforms) == 0:
            print("The available set of platforms do not satisfy requirements!")
            self.__platform = Platforms.NO_SELECTION
        else:
            print('"Constraints satisfied"')
            time.sleep(2)
            if self.__current_safety_monitor == SafetyMonitor.FORCE_SLIP:
                self.__platform = Platforms(self.__selected_platforms[0][0])
                selected_platform_details = self.__selected_platforms[0]
            elif self.__current_safety_monitor == SafetyMonitor.TACTILE_SLIP:
                self.__platform = Platforms(self.__selected_platforms[1][0])
                selected_platform_details = self.__selected_platforms[1]
            else:
                self.__platform = Platforms(self.__selected_platforms[2][0])
                selected_platform_details = self.__selected_platforms[2]

            print("Selected Platform = {}\nProperties:".format(Platforms(selected_platform_details[0])))
            print(tabulate([selected_platform_details], headers=["Platform ID","ForceSensorPresence","TactileSensorCount","MemoryAvailability",
                                                        "ForceSensorType","Latency"],tablefmt="fancy_grid"))

    def update_repository(self):
        """
        The update repository method update the platform status by passing the paltform variable values. 

        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        self.__repo_image.update_platform_status(self.__platform)

    def __platform_selected(self):
        """
        The paltform selected method intialises the solver, create a instance and pass appropriate varibles values.
        Insatnce is solved and results are appended to appropriate variable.
        Returns the selected platform from minizinc that solves CSP. 

        Parameters
        ----------
        **params: 
            None

        Returns
        -------
        platform_solutions: list
            Contains all the solution obtained from the CSP solver.
        """
        # Load platfroms model from file
        minizinc_file = "./" + str(self.__minizinc_model)
        platforms = Model(minizinc_file)
        # Find the MiniZinc solver configuration for Gecode
        gecode = Solver.lookup("gecode")
        # Create an Instance of the platforms model for Gecode
        instance = Instance(gecode, platforms)
        instance["force_sensor_presence"] = self.__repo_image.force_sensor_presence
        instance["min_tactile_sensor_count"] = self.__repo_image.min_tactile_sensor_count
        instance["min_memory_fused"] = self.__repo_image.min_memory_fused
        instance["n_platforms"] = self.__repo_image.n_platforms
        instance["platforms"] = self.__repo_image.platforms
        instance["min_latency"] = self.__repo_image.fused_platform_min_latency
        instance["max_latency"] = self.__repo_image.fused_platform_max_latency
        instance["req_force_plfm_type"] = self.__repo_image.force_sensor_type
        instance["curr_memory_availability"]=  [int(x) for x in self.__repo_image.platforms_memory_availability]

        result = instance.solve(intermediate_solutions=True)
        platform_solutions = []
        if len(result) != 0:
            for i in result:
                platform_solutions.append(i.force_platform)
                platform_solutions.append(i.tactile_platform)
                platform_solutions.append(i.fused_platform)

        return platform_solutions


if __name__ == '__main__':
    """
    minizinc model is loaded from the terminal 
    """
    args = argparse.ArgumentParser("Description: Please include the constraint satisfaction minizn solver file ")
    args.add_argument("--model", required=True, help="Provide the path of the Minizn platform model")
    args.add_argument("--input_data", required=True, help="Provide the csv file containing input data ")

    input_args = vars(args.parse_args())
    data_frame = pandas.read_csv(input_args["input_data"])

    repo_obj = Repository()
    """
    The instance of repository id is passed to context monitor, so that the information from context monitor 
    can be updated to the repository
    """
    context_monitor_obj = Context_Monitor(repo_obj)
    """
    The safety monitor selector receives current context info from repository and selects safety monitor and
     updates them in the repository.
    """
    safety_monitor_obj = Safety_Monitor_Selector(repo_obj)
    """
    The platform selector receives selected safety monitor info from repository and selects safety suitable platform
     using minizinc and updates them in the repository.
    """
    platform_selector_obj = Platform_Selector(repo_obj, input_args["model"])

    time_step = 0

    for data in data_frame.index:
        current_context = (data_frame['gripper_status'][data], data_frame['robot_in_motion'][data])
        platforms_memory_availability = [data_frame['pf1'][data],data_frame['pf2'][data],data_frame['pf3'][data],
                                         data_frame['pf4'][data],data_frame['pf5'][data]]

        print("Time_Step: T{}\n".format(time_step))
        time.sleep(2)
        print("Current memory availability in platforms")
        print(tabulate([platforms_memory_availability], headers=["Platform 1","Platform 2","Platform 3","Platform 4",
                                                                 "Platform 5"],tablefmt="fancy_grid"))
        time.sleep(2)
        repo_obj.update_platform_memory_availability(platforms_memory_availability)
        context_monitor_obj.set_robot_status(current_context)
        context_monitor_obj.update_info_to_repo()

        safety_monitor_obj.query_repository()
        safety_monitor_obj.select_safety_monitor()
        safety_monitor_obj.update_repository()

        platform_selector_obj.query_repository()
        platform_selector_obj.select_deployment_platform()
        platform_selector_obj.update_repository()
        time_step+=1

        print("\nWaiting for the next input...\n\n")
        time.sleep(5)
