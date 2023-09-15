#from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
        #interbotix_xs_modules.xs_robot.arm
from xs_robot import InterbotixManipulatorXS
# The robot object is what you use to control the robot
robot = InterbotixManipulatorXS("px100", "arm", "gripper")
mode = 'h'
f = open("/tmp/myfifo", "r")
# Let the user select the position

waist = 0
robot.gripper.release()
robot.arm.set_single_joint_position("wrist_angle", 0.90)
robot.arm.set_single_joint_position("waist", waist)
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
        
    # elif mode == "r":
    #     robot.arm.set_single_joint_position("waist", 0.0)
    #     robot.arm.set_single_joint_position("shoulder", -1.2)
    #     robot.arm.set_single_joint_position("elbow", 1.20)
    #     robot.arm.set_single_joint_position("wrist_angle", 0.50)
    #     # # cartesian measured in meters
    #     # robot.arm.set_ee_cartesian_trajectory(0.01, 0, 0.01, 0, 0, 0)
    #     # print(robot.arm.core.js_index_map)
    # elif mode == "k":
    #     #robot.arm.set_single_joint_position("waist", 0.31)
    #     robot.arm.set_ee_cartesian_trajectory(-0.05, 0, 0.03, 0, 0, 0)
    #     print(robot.arm.core.js_index_map)
    # elif mode == "z":
    #     robot.arm.set_ee_pose_components(0.085, 0, 0.18)


    txt = f.readline()
    txt = txt.strip("\n")
    point_str = txt.split(",")
    #print(f"point_str: {point_str}")

    if point_str[0] == '' or point_str[1] == '' or point_str[2] == '':
        continue

    point = [float(point_str[0]), float(point_str[1]), float(point_str[2])]
    #print(f"point: {point}")

    # Manipulate robot
    #if point[2] in range(160,500) and point[1] in range(-80,80) and point[0] in range(-55,70):
    xr = (point[0] + 85)/1000
    yr = (point[2] - 300)/1000
    zr = (-1*point[1]+100)/1000
    
    # pose = robot.arm.get_ee_pose()
    # xee = pose[0][3]
    # yee = pose[1][3]
    # zee = pose[2][3]
    yr = yr*6

    diff = yr - waist

    print(f"yr: {yr}, waist: {waist}")
    if diff > 0.05:
        if waist > -1 and waist < 1:
            waist = waist + 0.05
            robot.arm.set_single_joint_position("waist", waist)
    elif diff < -0.05:
        if waist > -1 and waist < 1:
            waist = waist - 0.05
            robot.arm.set_single_joint_position("waist", waist)
    elif diff <= 0.05 and diff >= -0.05:
        robot.arm.set_single_joint_position("wrist_angle", 0.10)
        robot.gripper.grasp()
        break
    # print(f"yr: {yr}")
    # waist = yr/0.08
    # print(f"waist: {waist}")

    # # robot.arm.set_ee_cartesian_trajectory(xr, yr, zr)
    # try: 
    #     robot.arm.set_single_joint_position("waist", waist)
    # except:
    #     print("I CANT MOVE THERE")
