# KRC-Touchless
Kindle Remote Ctrol but Touchless

I like to lie back in my chair and read on my Kindle, but after a while, holding it up gets tiring. So, I wanted a way to turn pages remotely. However, the Kindle does not support Bluetooth page turners, and adding an external page-turning device would be too bulky and inelegant.

## Device Information

- Kindle Paperwhite 5
  - Firmware version: **5.17.1.0.3**

## Prerequisites

- **Kindle Jailbreak**
- **USBNetLite installed** (If your device firmware is below **5.16.2**, you may need **USBNet** instead)
- **Python 3.12 installed** on your computer (*Mediapipe does not support Python 3.13*)

## Steps

1. **Connect your Kindle and your computer to the same Wi-Fi network**

   - You can find your Kindle’s IP address by entering `;711` in the Kindle search bar.

2. **Connect to your Kindle via SSH and ensure USBNet is working properly**

   ```
   ssh root@Kindle_IP
   ```

   - The default password for **USBNetLite** is `kindle`.

3. **Copy the `FlipCmd/` folder to the root directory of your Kindle (`/mnt/us/`)**

4. **Install the required Python libraries on your computer**

   * paramiko
   * mediapipe
   * pynput \# pynput is optional (needed for keyboard control mode)

5. **Modify the Kindle IP in `Hand_Tracking_Turner.py` to match your device**

6. **Run the script**

   - You may be prompted to grant permissions, such as access to the camera or enabling terminal accessibility options.
   - By default, the camera feed is turned **off** because it distracts me while reading. You can enable it by running the script with the `--debug` flag.
   - My version only supports **right-hand page turning**. I intentionally disabled left-hand input—if the left hand is detected, page turning is blocked. This way, I can use my left hand to eat or drink while reading. If you're left-handed or *Yang Guo*, you can modify the relevant parts of the code.

## Demo

- **[Kindle Gesture Remote Page Turning](https://youtube.com/shorts/Up9GAZ5MwEQ?si=uKGT7GlC87j-Y36v)**

## References & Related Projects

1. [ESPKindleTouch](https://github.com/bneo99/ESPKindleTouch/tree/main)
2. [Kindle Jailbreaking Guide](https://kindlemodding.org/jailbreaking/WinterBreak/)
3. [Kindle USBNetLite](https://github.com/notmarek/kindle-usbnetlite/releases/tag/1.0.M)
