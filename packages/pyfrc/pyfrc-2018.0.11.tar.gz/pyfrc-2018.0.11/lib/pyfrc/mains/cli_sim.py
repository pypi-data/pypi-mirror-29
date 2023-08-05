
import inspect
import json
import logging
from os.path import abspath, dirname, exists, join, isabs

import hal_impl.functions

from ..test_support import pyfrc_fake_hooks


logger = logging.getLogger('pyfrc.sim')

_field_root = abspath(join(dirname(__file__), '..', 'sim', 'field'))

_field_defaults = {
    '2017': {
        'h': 31,
        'w': 29,
        'px_per_ft': 17,
        'image': join(_field_root, '2017-field.gif')
    },
    '2018': {
        'h': 27,
        'w': 27,
        'px_per_ft': 15,
        'image': join(_field_root, '2018-field.gif')
    },
    'default': {
        'h': 1,
        'w': 1,
        'px_per_ft': 10,
        'image': None
    }
}


class PyFrcSim:
    """
        Executes the robot code using the low fidelity simulator and shows
        a tk-based GUI to control the simulation
    """

    def __init__(self, parser):
        pass
    
    def _load_config(self, config_file, sim_path):
        
        if exists(config_file):
            with open(config_file, 'r') as fp:
                config_obj = json.load(fp)
        else:
            logger.warn("sim/config.json not found, using default simulation parameters")
            config_obj = {}
        
        config_obj['simpath'] = sim_path
        
        # setup defaults
        config_obj.setdefault('pyfrc', {})
        
        config_obj['pyfrc'].setdefault('robot', {})
        config_obj['pyfrc']['robot'].setdefault('w', 2)
        config_obj['pyfrc']['robot'].setdefault('h', 3)
        config_obj['pyfrc']['robot'].setdefault('starting_x', 0)
        config_obj['pyfrc']['robot'].setdefault('starting_y', 0)
        config_obj['pyfrc']['robot'].setdefault('starting_angle', 0)
        
        config_obj['pyfrc'].setdefault('field', {})
        
        # backwards compat
        if 'season' in config_obj['pyfrc']['field']:
            season = config_obj['pyfrc']['field']['season']
            defaults = _field_defaults.get(str(season), _field_defaults['default'])
        elif 'objects' in config_obj['pyfrc']['field']:
            defaults = _field_defaults['default']
        else:
            defaults = _field_defaults['2018']
        
        config_obj['pyfrc']['field'].setdefault('objects', [])
        config_obj['pyfrc']['field'].setdefault('w', defaults['w'])
        config_obj['pyfrc']['field'].setdefault('h', defaults['h'])
        config_obj['pyfrc']['field'].setdefault('px_per_ft', defaults['px_per_ft'])
        img = config_obj['pyfrc']['field'].setdefault('image', defaults['image'])
        
        if img and not isabs(config_obj['pyfrc']['field']['image']):
            config_obj['pyfrc']['field']['image'] = abspath(join(sim_path, img))
        
        config_obj['pyfrc'].setdefault('analog', {})
        config_obj['pyfrc'].setdefault('CAN', {})
        config_obj['pyfrc'].setdefault('dio', {})
        config_obj['pyfrc'].setdefault('pwm', {})
        config_obj['pyfrc'].setdefault('relay', {})
        config_obj['pyfrc'].setdefault('solenoid', {})
        
        config_obj['pyfrc'].setdefault('joysticks', {})
        for i in range(6):
            config_obj['pyfrc']['joysticks'].setdefault(str(i), {})
            config_obj['pyfrc']['joysticks'][str(i)].setdefault('axes', {})
            config_obj['pyfrc']['joysticks'][str(i)].setdefault('buttons', {})
            
            config_obj['pyfrc']['joysticks'][str(i)]['buttons'].setdefault("1", "Trigger")
            config_obj['pyfrc']['joysticks'][str(i)]['buttons'].setdefault("2", "Top")
            
        return config_obj
        

    def run(self, options, robot_class, **static_options):
        
        from .. import config
        config.mode = 'sim'
        
        # Load these late so tk isn't loaded each time we run a test
        from ..physics.core import PhysicsInitException
        from .. import sim
        
        # load the config json file
        robot_file = abspath(inspect.getfile(robot_class))
        robot_path = dirname(robot_file)
        sim_path = join(robot_path, 'sim')
        config_file = join(sim_path, 'config.json')
        
        config_obj = self._load_config(config_file, sim_path)
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
