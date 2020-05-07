import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Angle, Pose
import time


def robot_mod(robot: cozmo.robot.Robot):
    # reset Cozmo
    robot.move_lift(-3)
    robot.set_head_angle(degrees(0)).wait_for_completed()

    # bring lift upwards for the tape 
    robot.move_lift(.30)
    time.sleep(1)
    robot.move_lift(0)

    # drive forward
    robot.drive_straight(distance_mm(100), speed_mmps(100)).wait_for_completed()

    # pick up tape
    robot.move_lift(3)
    time.sleep(1)

    # drive forward
    robot.drive_straight(distance_mm(100), speed_mmps(100)).wait_for_completed()

    # place down tape
    robot.move_lift(-.50)
    time.sleep(1)
    robot.move_lift(0)

    # drive backwards
    robot.drive_straight(distance_mm(-100), speed_mmps(100)).wait_for_completed()

    # reset Cozmo
    robot.move_lift(-3)
    robot.set_head_angle(degrees(0)).wait_for_completed()

def enviro_mod(robot: cozmo.robot.Robot):
    # reset Cozmo
    robot.move_lift(-3)
    robot.set_head_angle(degrees(0)).wait_for_completed()

    # drive forward
    robot.drive_straight(distance_mm(100), speed_mmps(100)).wait_for_completed()

    # pick up tape
    robot.move_lift(1)
    time.sleep(1)

    # drive forward
    robot.drive_straight(distance_mm(100), speed_mmps(100)).wait_for_completed()

    # place down tape
    robot.move_lift(-3)
    time.sleep(1)
    robot.move_lift(0)

    # drive backwards
    robot.drive_straight(distance_mm(-100), speed_mmps(100)).wait_for_completed()

def cozmo_go_to_pose(robot, x, y, angle_z):
	"""Moves the robot to a pose relative to its current pose.
		Arguments:
		robot -- the Cozmo robot instance passed to the function
		x,y -- Desired position of the robot in millimeters
		angle_z -- Desired rotation of the robot around the vertical axis in degrees
	"""
	robot.go_to_pose(Pose(x, y, 0, angle_z=degrees(angle_z)), relative_to_robot=True).wait_for_completed()

def move_object_to_pose(robot, x, y):
    """Moves an object 5cm in front of Cozmo to the given pose
		Arguments:
		robot -- the Cozmo robot instance passed to the function
		x,y -- Desired position of the object in millimeters
	"""
    robot.drive_straight(distance_mm(50), speed_mmps(100)).wait_for_completed()
    cozmo_go_to_pose(robot, x + 5, y, 0)
    robot.drive_straight(distance_mm(-50), speed_mmps(100)).wait_for_completed()

def step_2(robot: cozmo.robot.Robot):
    # move_object_to_pose(robot, 150, 50)
    move_object_to_pose(robot, 300, -100)

# For using the robot modification
# cozmo.run_program(robot_mod)
# For using the environment modification
# cozmo.run_program(enviro_mod)
cozmo.run_program(step_2)
