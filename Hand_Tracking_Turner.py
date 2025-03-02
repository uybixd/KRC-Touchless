import cv2
import mediapipe as mp
import paramiko
import time
import sys

DEBUG_MODE = "--debug" in sys.argv

kindle_ip = "REPLACE_WITH_YOUR_KINDLE_IP"  # 你的 Kindle IP 地址
username = "root"  # Kindle 的默认 SSH 用户
password = "kindle"  # USBNetLite 默认密码（请根据实际情况修改）

forward_command = "cat /mnt/us/FlipCmd/next.event > /dev/input/event1 && /usr/bin/powerd_test -i"
prev_command = "cat /mnt/us/FlipCmd/prev.event > /dev/input/event1 && /usr/bin/powerd_test -i"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(kindle_ip, username=username, password=password)
    print("SSH Connection established.")

    def send_command(command):
        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print(f"Output: {output}")
            if error:
                print(f"Error: {error}")
        except Exception as e:
            print(f"SSH Command Error: {e}")

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    start_x = None
    start_time = None
    hand_appear_time = None

    HAND_STABLE_TIME = 0.2
    SWIPE_THRESHOLD = 0.2  # 滑动最小距离（相对图像宽度）
    TIME_THRESHOLD = 0.3  # 滑动最短时间
    COOLDOWN_TIME = 1.5  # 冷却时间，避免误触
    last_swipe_time = 0  # 记录上次滑动的时间

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)
        current_time = time.time()

        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[idx].classification[0].label
                if hand_label != "Right":
                    continue

                index_finger_tip = hand_landmarks.landmark[8]

                if hand_appear_time is None:
                    hand_appear_time = current_time
                    start_x = None
                    continue

                if current_time - hand_appear_time < HAND_STABLE_TIME:
                    start_x = None
                    continue

                if start_x is None:
                    start_x = index_finger_tip.x
                    start_time = current_time
                else:
                    delta_x = index_finger_tip.x - start_x
                    elapsed_time = current_time - start_time

                    if (elapsed_time > TIME_THRESHOLD and 
                        abs(delta_x) > SWIPE_THRESHOLD and 
                        (current_time - last_swipe_time > COOLDOWN_TIME)):

                        if delta_x < -SWIPE_THRESHOLD:
                            print("👉 向左滑（下一页）")
                            send_command(forward_command)
                        elif delta_x > SWIPE_THRESHOLD:
                            print("👈 向右滑（上一页）")
                            send_command(prev_command)

                        last_swipe_time = current_time
                        start_x = None
                        start_time = None
                        hand_appear_time = None

                if DEBUG_MODE:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        else:
            hand_appear_time = None

        if DEBUG_MODE:
            cv2.imshow('Swipe Gesture for Kindle', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    print("Closing SSH connection and releasing resources...")
    ssh.close()
    cap.release()
    cv2.destroyAllWindows()
