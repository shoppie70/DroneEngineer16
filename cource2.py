from dronekit import connect, VehicleMode
import time

# ドローンに接続
vehicle = connect('tcp:127.0.0.1:5762')
# vehicle = connect('/dev/ttyS6',wait_ready=False, baud=57600)

# モードをGUIDEDに変更
vehicle.mode = VehicleMode("GUIDED")

# アーム
vehicle.arm()

# ドローンを離陸させる
target_altitude = 5  # 離陸したい高さ（メートル）
target_move_distance = 5 # 移動したい距離（メートル）

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
    distance = distance * 0.000009;
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
            print(remaining_distance)
        elif direction in ["north", "south"]:
            remaining_distance = abs(vehicle.location.global_relative_frame.lat - target_location.lat)
        if remaining_distance < 0.00001:  # 0.00001度未満の距離になったら移動完了とみなす
            break
        time.sleep(1)
        
# 東に移動
move_in_direction(target_move_distance, "east")

# 北に移動
move_in_direction(target_move_distance, "north")

# 西に移動
move_in_direction(target_move_distance, "west")

# 南に移動
move_in_direction(target_move_distance, "south")

# LAND
print("Moving in different directions completed. Landing...")
vehicle.mode = VehicleMode("LAND")

# 着陸完了まで待機
while vehicle.armed:
    time.sleep(1)
    
# 接続を切断
vehicle.close()
