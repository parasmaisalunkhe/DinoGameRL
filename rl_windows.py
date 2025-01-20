from pywinauto import Application
from pywinauto import Desktop
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
# from sb3_contrib import TQC
import pyautogui
import time
import pygetwindow as gw
from pywinauto import Application
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import cv2

def is_template_in_image(npimage, template_path, threshold: float = 0.5):
    gray_image = cv2.cvtColor(npimage, cv2.IMREAD_GRAYSCALE)
    # cv2.imshow("test", gray_image)
    # cv2.waitKey(0)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_RGB2GRAY)
    # template = cv2.cvtColor(template, cv2.COLOR  _RGB2GRAY)
    res = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    match_found = np.any(res >= threshold)
    return match_found

# Step 1: Read the image


class DinoGameEnv(gym.Env):

    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0, high=255, shape=(150, 600, 1), dtype=np.uint8)
        dino_window = gw.getWindowsWithTitle("Dino Game")[0]
        self.x, self.y, self.width, self.height = dino_window.left+100, dino_window.top+80, dino_window.width-200, dino_window.height-450
        self.start_time = time.perf_counter()
        pyautogui.press('space')
    def reset(self, seed=None, options=None):
        pyautogui.press('space')
        newobs = np.array(cv2.cvtColor(np.array(pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))), cv2.COLOR_RGB2GRAY)).reshape((150, 600, 1))
        return newobs, {}

    def step(self, action):
        # Process the action and generate a new observation
        # Here, we simply return a random binary output based on the action
        done = False
        if action == 0:
            pyautogui.press('up')
        if action == 1:
            pyautogui.press('down')
        newobs = np.array(cv2.cvtColor(np.array(pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))), cv2.COLOR_RGB2GRAY)).reshape((150, 600, 1))
        self.reward = (time.perf_counter() - self.start_time) * 1000
        if is_template_in_image(newobs, "C://Users//Parasmai//Documents//DinoGameRL//images//resetLight.png") or is_template_in_image(newobs, "C://Users//Parasmai//Documents//DinoGameRL//images//resetDark.png"):
            done = True
            self.reward = -10
            self.start_time = time.perf_counter()
        return newobs, self.reward, done, False, {}

    # def render(self, mode='human'):
    #     # Display the current image using OpenCV
    #     cv2.imshow("Image", self.current_image)
    #     cv2.waitKey(1)

    def close(self):
        cv2.destroyAllWindows()

# url = 'https://chrome-dino-game.github.io/'

# Create a webview window
# webview.create_window('Dino Game', url)

# Start the webview

def main():  
    # gw.getWindowsWithTitle('Dino Game')[0].activate()
    

# Create a Desktop object to interact with all top-level windows
#     desktop = Desktop(backend="uia")

#     # Retrieve a list of all top-level windows
#     windows = desktop.windows()

#     # Print the title of each window
#     for window in windows:
#         print(window.window_text())
    

# # Initialize the Application object with the appropriate backend
#     app = Application(backend="uia").connect(title="Dino Game")
#     dino_window = app["Dino Game"]
    # dino_window.set_focus()
    time.sleep(5)
    print("hi")
    env = DinoGameEnv()
    model = PPO("CnnPolicy", env, verbose=2, device="cuda")
    model.learn(total_timesteps=1000000)
    model.save("ppo_dino")
if __name__ == "__main__":
    # check_env(DinoGameEnv())  
    main()
# webview.start(func=main)