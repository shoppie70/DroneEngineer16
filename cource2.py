from dronekit import connect, VehicleMode
import time

# ドローンに接続
vehicle = connect('tcp:127.0.0.1:5762')

# モードをGUIDEDに変更
vehicle.mode = VehicleMode("GUIDED")

# アーム
vehicle.arm()

# ドローンを離陸させる
target_altitude = 10  # 離陸したい高さ（メートル）
print("Taking off to {} meters...".format(target_altitude))

vehicle.simple_takeoff(target_altitude)

# 離陸完了まで待機
while not vehicle.is_armable:
    time.sleep(1)

# 高度が目標に達するまで待機
while True:
    if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
        print("Reached target altitude. Moving in different directions...")
        break
    time.sleep(1)

def move_in_direction(distance, direction):
    """
    ドローンを指定された方向に移動させる関数。

    :param distance: 移動する距離（単位: 度）
    :param direction: 移動する方向（"east", "west", "north", "south"）
    """
    target_location = vehicle.location.global_relative_frame
    if direction == "east":
        target_location.lon += distance
    elif direction == "west":
        target_location.lon -= distance
    elif direction == "north":
        target_location.lat += distance
    elif direction == "south":
        target_location.lat -= distance

    vehicle.simple_goto(target_location)

    # 移動完了まで待機
    while True:
        remaining_distance = 0
        if direction in ["east", "west"]:
            remaining_distance = abs(vehicle.location.global_relative_frame.lon - target_location.lon)
        elif direction in ["north", "south"]:
            remaining_distance = abs(vehicle.location.global_relative_frame.lat - target_location.lat)

        if remaining_distance < 0.00001:  # 0.00001度未満の距離になったら移動完了とみなす
            break
        time.sleep(1)

# 東に50メートル移動
move_in_direction(0.00045, "east")  # 約0.00045度は50メートルに相当

# 北に50メートル移動
move_in_direction(0.00045, "north")  # 約0.00045度は50メートルに相当

# 西に50メートル移動
move_in_direction(0.00045, "west")  # 約0.00045度は50メートルに相当

# 南に50メートル移動
move_in_direction(0.00045, "south")  # 約0.00045度は50メートルに相当

# LAND
print("Moving in different directions completed. Landing...")
vehicle.mode = VehicleMode("LAND")

# 着陸完了まで待機
while vehicle.armed:
    time.sleep(1)

# 接続を切断
vehicle.close()
