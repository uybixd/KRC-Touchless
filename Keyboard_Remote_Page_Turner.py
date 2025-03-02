import paramiko
from pynput import keyboard

kindle_ip = "REPLACE_WITH_YOUR_KINDLE_IP"
username = "REPLACE_WITH_YOUR_USERNAME"
password = "REPLACE_WITH_YOUR_PASSWORD"

forward_command = "cat /mnt/us/FlipCmd/next.event > /dev/input/event1 && /usr/bin/powerd_test -i"
prev_command = "cat /mnt/us/FlipCmd/prev.event > /dev/input/event1 && /usr/bin/powerd_test -i"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(kindle_ip, username=username, password=password)
    print("SSH Connection established.")
except Exception as e:
    print(f"SSH Error: {e}")
    exit(1)

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

def on_press(key):
    try:
        if key == keyboard.Key.right:
            print("Next Page")
            send_command(forward_command)
        elif key == keyboard.Key.left:
            print("Previous Page")
            send_command(prev_command)
        elif key == keyboard.Key.esc:
            print("Exiting...")
            ssh.close()
            return False
    except AttributeError:
        pass

print("Listening for key presses... Press ESC to exit.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
