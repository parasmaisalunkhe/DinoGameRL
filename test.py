
import numpy as np
import cv2
def is_template_in_image(npimage, template_path, threshold: float = 0.8) -> bool:
    gray_image = cv2.imread(npimage, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    
    res = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    
    match_found = np.any(res >= threshold)
    return match_found

print(is_template_in_image("C://Users//Parasmai//Documents//DinoGameRL//test.png", "C://Users//Parasmai//Documents//DinoGameRL//images//resetLight.png"))
