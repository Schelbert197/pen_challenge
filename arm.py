#from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
        #interbotix_xs_modules.xs_robot.arm
from re import T
from xs_robot import InterbotixManipulatorXS
import math
# The robot object is what you use to control the robot
robot = InterbotixManipulatorXS("px100", "arm", "gripper")
mode = 'h'
f = open("/tmp/myfifo", "r")
# Let the user select the position

waist = 0.0
robot.gripper.release()
# robot.arm.set_single_joint_position("wrist_angle", 0.90)
# robot.arm.set_single_joint_position("waist", waist)
robot.arm.set_joint_positions([0.0, -1.57, 1.45, 0.45], moving_time=1.0, accel_time=0.5, blocking=True)
while mode != 'q':
    # mode=input("[h]ome, [s]leep, [q]uit :")
    # if mode == "h":
    #     robot.arm.go_to_home_pose()
    # elif mode == "s":
    #     robot.arm.go_to_sleep_pose()
    # elif mode == "g":
    #     robot.gripper.release()
    #     pose = robot.arm.get_ee_pose()
    #     print(pose)

    txt = f.readline()
    txt = txt.strip("\n")
    point_str = txt.split(",")
    # print(f"point_str: {point_str}")

    if point_str[0] == '' or len(point_str) < 3:
        continue

    point = [float(point_str[0]), float(point_str[1]), float(point_str[2])]
    # print(f"point: {point}")

    # Manipulate robot
    if 160.0 <= point[2] <= 500.0 and -80.0 <= point[1] <= 80.0 and -55.0 <= point[0] <= 80.0:
        xr = round(((point[0] + 85)/1000),5)
        yr = round(((point[2] - 300)/1000),5)
        zr = round(((-1*point[1]+100)/1000),5)
        
        pose = robot.arm.get_ee_pose()
        xee = round(pose[0][3],5)
        yee = round(pose[1][3],5)
        zee = round(pose[2][3],5)

        rho = math.tan(yr/xr)
        

        diff_c = [xr-xee, yr-yee, zr-zee]
        diff_rho = rho - waist
        print(f"difference [m]: {diff_c} {diff_rho}")



        print(f"yr: {yr}, waist: {waist}")
        if -0.05 <= diff_rho <= 0.05: # Grab the pen
            # robot.arm.set_single_joint_position("wrist_angle", 0.10)
            #robot.arm.set_ee_cartesian_trajectory(x=diff_c[0], z=diff_c[2], wp_accel_time=0.2, wp_moving_time=0.2)
            # robot.arm.set_ee_pose_components(x=xr, z=zr)
            robot.arm.set_joint_positions([waist, 0.0, 0.0, 0.0], accel_time=0.25, moving_time=1.75)
            robot.gripper.grasp()
            break
        elif -1 <= waist + diff_rho <= 1: # move to the pen
            waist = waist + diff_rho
            robot.arm.set_single_joint_position("waist", waist, blocking=True, accel_time=0.5, moving_time=0.5)

    else:
        continue
    # print(f"yr: {yr}")
    # waist = yr/0.08
    # print(f"waist: {waist}")

    # # robot.arm.set_ee_cartesian_trajectory(xr, yr, zr)
    # try: 
    #     robot.arm.set_single_joint_position("waist", waist)
    # except:
    #     print("I CANT MOVE THERE")
