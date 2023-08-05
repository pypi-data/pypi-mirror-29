'''
    Based on input from various drive motors, these helper functions
    simulate moving the robot in various ways. Many thanks to
    `Ether <http://www.chiefdelphi.com/forums/member.php?u=34863>`_
    for assistance with the motion equations.
      
    When specifying the robot speed to the below functions, the following
    may help you determine the approximate speed of your robot:
    
    * Slow: 4ft/s
    * Typical: 5 to 7ft/s
    * Fast: 8 to 12ft/s
        
    Obviously, to get the best simulation results, you should try to
    estimate the speed of your robot accurately.
'''
import math

def linear_deadzone(deadzone):
    '''
        Real motors won't actually move unless you give them some minimum amount
        of input. This computes an output speed for a motor and causes it to
        'not move' if the input isn't high enough. Additionally, the output is
        adjusted linearly to compensate.
        
        Example: For a deadzone of 0.2:
        
        * Input of 0.0 will result in 0.0
        * Input of 0.2 will result in 0.0
        * Input of 0.3 will result in ~0.12
        * Input of 1.0 will result in 1.0
        
        This returns a function that computes the deadzone. You should pass the
        returned function to one of the drivetrain simulation functions as the
        ``deadzone`` parameter.
        
        Here's an example usage:
        
            from pyfrc.physics import drivetrains
        
            class PhysicsEngine:
                
                def __init__(self, physics_controller):
                    self.drivetrain_deadzone = drivetrains.linear_deadzone(0.2)
                    
                def update_sim(self, hal_data, now, tm_diff):
                    # TODO: get motor values from hal_data
                    speed_rotation = drivetrains.two_motor_drivetrain(l_motor, r_motor,
                                                                      deadzone=self.drivetrain_deadzone)
        
        :param motor_input: The motor input (between -1 and 1)
        :param deadzone: Minimum input required for the motor to move (between 0 and 1)
    '''
    assert 0.0 < deadzone < 1.0
    scale_param = 1.0 - deadzone
    def _linear_deadzone(motor_input):
        abs_motor_input = abs(motor_input)
        if abs_motor_input < deadzone:
            return 0.0
        else:
            return math.copysign((abs_motor_input - deadzone) / scale_param, motor_input)
    
    return _linear_deadzone
    
def two_motor_drivetrain(l_motor, r_motor, x_wheelbase=2, speed=5, deadzone=None):
    '''
        Two center-mounted motors with a simple drivetrain. The
        motion equations are as follows::
    
            FWD = (L+R)/2
            RCW = (L-R)/W
        
        * L is forward speed of the left wheel(s), all in sync
        * R is forward speed of the right wheel(s), all in sync
        * W is wheelbase in feet
        
        If you called "SetInvertedMotor" on any of your motors in RobotDrive,
        then you will need to multiply that motor's value by -1.
        
        .. note:: WPILib RobotDrive assumes that to make the robot go forward,
                  the left motor must be set to -1, and the right to +1
        
        :param l_motor:    Left motor value (-1 to 1); -1 is forward
        :param r_motor:    Right motor value (-1 to 1); 1 is forward
        :param x_wheelbase: The distance in feet between right and left wheels.
        :param speed:      Speed of robot in feet per second (see above)
        :param deadzone:   A function that adjusts the output of the motor (see :func:`linear_deadzone`)
        
        :returns: speed of robot (ft/s), clockwise rotation of robot (radians/s)
    '''
    
    if deadzone:
        l_motor = deadzone(l_motor)
        r_motor = deadzone(r_motor)
    
    l = -l_motor * speed
    r = r_motor * speed

    # Motion equations
    fwd = (l + r) * 0.5
    rcw = (l - r) / float(x_wheelbase)
        
    return fwd, rcw


def four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor, x_wheelbase=2, speed=5, deadzone=None):
    '''
        Four motors, each side chained together. The motion equations are
        as follows::
    
            FWD = (L+R)/2
            RCW = (L-R)/W
        
        * L is forward speed of the left wheel(s), all in sync
        * R is forward speed of the right wheel(s), all in sync
        * W is wheelbase in feet
        
        If you called "SetInvertedMotor" on any of your motors in RobotDrive,
        then you will need to multiply that motor's value by -1.
        
        .. note:: WPILib RobotDrive assumes that to make the robot go forward,
                  the left motors must be set to -1, and the right to +1
        
        :param lr_motor:   Left rear motor value (-1 to 1); -1 is forward
        :param rr_motor:   Right rear motor value (-1 to 1); 1 is forward
        :param lf_motor:   Left front motor value (-1 to 1); -1 is forward
        :param rf_motor:   Right front motor value (-1 to 1); 1 is forward
        :param x_wheelbase: The distance in feet between right and left wheels.
        :param speed:      Speed of robot in feet per second (see above)
        :param deadzone:   A function that adjusts the output of the motor (see :func:`linear_deadzone`)
        
        :returns: speed of robot (ft/s), clockwise rotation of robot (radians/s)
    '''
    
    if deadzone:
        lf_motor = deadzone(lf_motor)
        lr_motor = deadzone(lr_motor)
        rf_motor = deadzone(rf_motor)
        rr_motor = deadzone(rr_motor)
    
    l = -(lf_motor + lr_motor) * 0.5 * speed
    r = (rf_motor + rr_motor) * 0.5 * speed
    
    # Motion equations
    fwd = (l + r) * 0.5
    rcw = (l - r) / float(x_wheelbase)
        
    return fwd, rcw


def mecanum_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor, x_wheelbase=2, y_wheelbase=3, speed=5, deadzone=None):
    '''
        Four motors, each with a mechanum wheel attached to it.
        
        If you called "SetInvertedMotor" on any of your motors in RobotDrive,
        then you will need to multiply that motor's value by -1.
        
        .. note:: WPILib RobotDrive assumes that to make the robot go forward,
                  all motors are set to +1
        
        :param lr_motor:   Left rear motor value (-1 to 1); 1 is forward
        :param rr_motor:   Right rear motor value (-1 to 1); 1 is forward
        :param lf_motor:   Left front motor value (-1 to 1); 1 is forward
        :param rf_motor:   Right front motor value (-1 to 1); 1 is forward
        :param x_wheelbase: The distance in feet between right and left wheels.
        :param y_wheelbase: The distance in feet between forward and rear wheels.
        :param speed:      Speed of robot in feet per second (see above)
        :param deadzone:   A function that adjusts the output of the motor (see :func:`linear_deadzone`)
        
        :returns: Speed of robot in x (ft/s), Speed of robot in y (ft/s),
                  clockwise rotation of robot (radians/s)
    '''

    #
    # From http://www.chiefdelphi.com/media/papers/download/2722 pp7-9
    # [F] [omega](r) = [V]
    #
    # F is
    # .25  .25  .25 .25
    # -.25 .25 -.25 .25
    # -.25k -.25k .25k .25k
    #
    # omega is
    # [lf lr rr rf]
    
    if deadzone:
        lf_motor = deadzone(lf_motor)
        lr_motor = deadzone(lr_motor)
        rf_motor = deadzone(rf_motor)
        rr_motor = deadzone(rr_motor)

    # Calculate speed of each wheel
    lr = lr_motor * speed
    rr = rr_motor * speed
    lf = lf_motor * speed
    rf = rf_motor * speed

    # Calculate K
    k = abs(x_wheelbase/2) + abs(y_wheelbase/2)

    # Calculate resulting motion
    Vy = .25 * (lf + lr + rr + rf)
    Vx = .25 * (lf + -lr + rr + -rf)
    Vw = (.25/k) * (lf + lr + -rr + -rf)
    
    return Vx, Vy, Vw
    
def four_motor_swerve_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor, lr_angle, rr_angle, lf_angle, rf_angle, x_wheelbase=2, y_wheelbase=2, speed=5, deadzone=None):
    '''
        Four motors that can be rotated in any direction
        
        If any motors are inverted, then you will need to multiply that motor's
        value by -1.
        
        :param lr_motor:   Left rear motor value (-1 to 1); 1 is forward
        :param rr_motor:   Right rear motor value (-1 to 1); 1 is forward
        :param lf_motor:   Left front motor value (-1 to 1); 1 is forward
        :param rf_motor:   Right front motor value (-1 to 1); 1 is forward
        
        :param lr_angle:   Left rear motor angle in degrees (0 to 360 measured clockwise from forward position)
        :param rr_angle:   Right rear motor angle in degrees (0 to 360 measured clockwise from forward position)
        :param lf_angle:   Left front motor angle in degrees (0 to 360 measured clockwise from forward position)
        :param rf_angle:   Right front motor angle in degrees (0 to 360 measured clockwise from forward position)
        
        :param x_wheelbase: The distance in feet between right and left wheels.
        :param y_wheelbase: The distance in feet between forward and rear wheels.
        :param speed:      Speed of robot in feet per second (see above)
        :param deadzone:   A function that adjusts the output of the motor (see :func:`linear_deadzone`)
        
        :returns: Speed of robot in x (ft/s), Speed of robot in y (ft/s),
                  clockwise rotation of robot (radians/s)
    '''
    
    if deadzone:
        lf_motor = deadzone(lf_motor)
        lr_motor = deadzone(lr_motor)
        rf_motor = deadzone(rf_motor)
        rr_motor = deadzone(rr_motor)
    
    # Calculate speed of each wheel
    lr = lr_motor * speed
    rr = rr_motor * speed
    lf = lf_motor * speed
    rf = rf_motor * speed

    # Calculate angle in radians
    lr_rad = math.radians(lr_angle)
    rr_rad = math.radians(rr_angle)
    lf_rad = math.radians(lf_angle)
    rf_rad = math.radians(rf_angle)

    # Calculate wheelbase radius
    wheelbase_radius = math.hypot(x_wheelbase / 2, y_wheelbase / 2)

    # Calculates the Vx and Vy components
    # Sin an Cos inverted because forward is 0 on swerve wheels
    Vx = (math.sin(lr_rad) * lr) + (math.sin(rr_rad) * rr) + (math.sin(lf_rad) * lf) + (math.sin(rf_rad) * rf)
    Vy = (math.cos(lr_rad) * lr) + (math.cos(rr_rad) * rr) + (math.cos(lf_rad) * lf) + (math.cos(rf_rad) * rf)
    
    
    # Adjusts the angle corresponding to a diameter that is perpendicular to the radius (add or subtract 45deg)
    lr_rad = (lr_rad + (math.pi / 4)) % (2 * math.pi)
    rr_rad = (rr_rad - (math.pi / 4)) % (2 * math.pi)
    lf_rad = (lf_rad - (math.pi / 4)) % (2 * math.pi)
    rf_rad = (rf_rad + (math.pi / 4)) % (2 * math.pi)

    # Finds the rotational velocity by finding the torque and adding them up
    Vw = wheelbase_radius * ((math.cos(lr_rad) * lr) + (math.cos(rr_rad) * -rr) + (math.cos(lf_rad) * lf) + (math.cos(rf_rad) * -rf))
    
    Vx *= 0.25
    Vy *= 0.25
    Vw *= 0.25

    return Vx, Vy, Vw

# TODO: holonomic, etc
