
import inspect
from os.path import abspath, dirname

import hal_impl.functions

from ..test_support import pyfrc_fake_hooks

import logging
logger = logging.getLogger('pyfrc.sim')


class PyFrcSim:
    """
        Executes the robot code using the low fidelity simulator and shows
        a tk-based GUI to control the simulation
    """

    def __init__(self, parser):
        pass

    def run(self, options, robot_class, **static_options):
        
        from .. import config
        from ..configloader import _load_config
        
        config.mode = 'sim'
        
        # Load these late so tk isn't loaded each time we run a test
        from ..physics.core import PhysicsInitException
        from .. import sim
        
        # load the config json file
        robot_file = abspath(inspect.getfile(robot_class))
        robot_path = dirname(robot_file)
        
        _load_config(robot_path)
        config_obj = config.config_obj
        
        fake_time = sim.FakeRealTime()
        hal_impl.functions.hooks = pyfrc_fake_hooks.PyFrcFakeHooks(fake_time)
        hal_impl.functions.reset_hal()
    
        sim_manager = sim.SimManager()
        
        try:
            controller = sim.RobotController(robot_class, robot_path, fake_time, config_obj)
        except PhysicsInitException:
            return False
            
        robot_element = None
        if controller.has_physics():
            robot_element = sim.RobotElement(controller, config_obj)
        
        sim_manager.add_robot(controller)
        
        controller.run()
        controller.wait_for_robotinit()
        if not controller.is_alive():
            return 1
        
        ui = sim.SimUI(sim_manager, fake_time, config_obj)
        
        if robot_element is not None:
            ui.field.add_moving_element(robot_element)
        
        ui.run()
    
        # once it has finished, try to shut the robot down
        # -> if it can't, then the user messed up
        if not controller.stop():
            print('Error: could not stop the robot code! Check your code')
    
        return 0
