#from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
        #interbotix_xs_modules.xs_robot.arm
from xs_robot import InterbotixManipulatorXS
# The robot object is what you use to control the robot
robot = InterbotixManipulatorXS("px100", "arm", "gripper")
mode = 'h'
# Let the user select the position
while mode != 'q':
    mode=input("[h]ome, [s]leep, [q]uit :")
    if mode == "h":
        robot.arm.go_to_home_pose()
    elif mode == "s":
        robot.arm.go_to_sleep_pose()
    elif mode == "g":
        robot.gripper.grasp()
    elif mode == "r":
        #robot.arm.set_single_joint_position("waist", 0.31)
        robot.arm.set_ee_cartesian_trajectory(0.01, 0, 0.01, 0, 0, 0)
        print(robot.arm.core.js_index_map)
    elif mode == "k":
        #robot.arm.set_single_joint_position("waist", 0.31)
        robot.arm.set_ee_cartesian_trajectory(-0.05, 0, 0.03, 0, 0, 0)
        print(robot.arm.core.js_index_map)