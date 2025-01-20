from stable_baselines3 import PPO
import os
import pyautogui
import time
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import cv2
from PIL import Image

def is_template_in_image(npimage, template_path, threshold: float = 0.5):
    gray_image = cv2.cvtColor(npimage, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    match_found = np.any(res >= threshold)
    return match_found

def get_window_id(window_name):
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

        # Open the screenshot with Pillow and crop to the desired window
        with Image.open("screenshot.png") as img:
            img = img.crop(((100, 90, 100+600, 90+150)))
            return img
    else:
        print(f"Failed to capture screenshot for window '{window_name}'")
        return None


# Step 1: Read the image


class DinoGameEnv(gym.Env):

    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0, high=255, shape=(150, 600, 1), dtype=np.uint8)
        self.window_name = "Dino Game"
        self.window_id = get_window_id(self.window_name)
        self.start_time = time.perf_counter()
        pyautogui.press('space')
    def reset(self, seed=None, options=None):
        pyautogui.press('space')
        newobs = np.array(cv2.cvtColor(np.array(capture_screenshot(self.window_id, self.window_name)), cv2.COLOR_RGB2GRAY)).reshape((150, 600, 1))
        return newobs, {}

    def step(self, action):
        done = False
        if action == 0:
            pyautogui.press('up')
        if action == 1:
            pyautogui.press('down')
        newobs = np.array(cv2.cvtColor(np.array(capture_screenshot(self.window_id, self.window_name)), cv2.COLOR_RGB2GRAY)).reshape((150, 600, 1))
        self.reward = (time.perf_counter() - self.start_time) * 1000
        if is_template_in_image(newobs, "images//resetLight.png") or is_template_in_image(newobs, "images//resetDark.png"):
            done = True
            self.reward = -10
            self.start_time = time.perf_counter()
        return newobs, self.reward, done, False, {}

    def close(self):
        cv2.destroyAllWindows()
def main():  
    time.sleep(5)
    print("hi")
    env = DinoGameEnv()
    model = PPO("CnnPolicy", env, verbose=2, device="cuda")
    model.learn(total_timesteps=1000000)
    model.save("ppo_dino")
if __name__ == "__main__":
    main()
