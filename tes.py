from PIL import Image
import os
import io
import time
def get_window_id(window_name):
    # Use xdotool to get the window ID
    window_id = os.popen(f"xdotool search --name '{window_name}'").read().strip()
    return window_id if window_id else None

def get_window_geometry(window_id):
    try:
        # Get window geometry using xdotool
        window_info = os.popen(f"xdotool getwindowgeometry --shell {window_id}").read().strip()
        geometry = {}
        for line in window_info.split('\n'):
            key, value = line.split('=')
            geometry[key] = int(value)
        return geometry['X'], geometry['Y'], geometry['WIDTH'], geometry['HEIGHT']
    except Exception as e:
        print(f"Error getting window geometry: {e}")
        return None

def capture_screenshot(window_id, window_name):
    geometry = get_window_geometry(window_id)
    if geometry:
        x, y, width, height = geometry
        # Use scrot to capture the screenshot
        os.system(f"scrot -u -o screenshot.png -e 'mv $f screenshot.png'")
        print("Screenshot captured")

        # Open the screenshot with Pillow and crop to the desired window
        with Image.open("screenshot.png") as img:
            img = img.crop((x, y, x + width, y + height))
            return img
    else:
        print(f"Failed to capture screenshot for window '{window_name}'")
        return None

if __name__ == "__main__":
    time.sleep(5)
    window_name = "Dino Game"
    window_id = get_window_id(window_name)
    if window_id:
        print(f"Capturing screenshot for window: {window_name}")
        img = capture_screenshot(window_id, window_name)
        if img:
            img.show()  # Display the image
        else:
            print(f"Failed to capture screenshot for window '{window_name}'")
    else:
        print(f"Window '{window_name}' not found")
