from dronekit import connect, VehicleMode
import time

def move_in_direction(distance, direction):
    """
    ドローンを指定された方向に移動させる関数。

    :param distance: 移動する距離（単位: 度）
    :param direction: 移動する方向（"east", "west", "north", "south"）
    """
    # メートルを度に変換
    distance = distance * 0.0000009

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

# ドローンに接続
vehicle = connect('tcp:127.0.0.1:5762')

# モードをGUIDEDに変更
vehicle.mode = VehicleMode("GUIDED")

# アーム
vehicle.arm()

# ドローンを離陸させる
target_altitude = 10  # 離陸したい高さ（メートル）
target_move_distance = 10 # 移動したい距離（メートル）

# 離陸したことを通知
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

    # 移動完了まで待機
    while True:
        remaining_distance = 0
        if direction in ["east", "west"]:
            remaining_distance = abs(vehicle.location.global_relative_frame.lon - target_location.lon)
        elif direction in ["north", "south"]:
            remaining_distance = abs(vehicle.location.global_relative_frame.lat - target_location.lat)

        if remaining_distance < 0.00005:  # 0.00005度未満の距離になったら移動完了とみなす
            break
        time.sleep(1)

# 東に指定した距離分を移動
move_in_direction(target_move_distance, "east")

# 北に指定した距離分を移動
move_in_direction(target_move_distance, "north")

# 西に指定した距離分を移動
move_in_direction(target_move_distance, "west")

# 南に指定した距離分を移動
move_in_direction(target_move_distance, "south")

# LAND
print("Moving in different directions completed. Landing...")
vehicle.mode = VehicleMode("LAND")

# 着陸完了まで待機
while vehicle.armed:
    time.sleep(1)

# 接続を切断
vehicle.close()
