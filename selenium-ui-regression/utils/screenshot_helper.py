import allure
import os

from datetime import datetime
from allure_commons.types import AttachmentType

def take_screenshot(driver, name="Step Screenshot"):
    allure.attach(driver.get_screenshot_as_png(), name=name, attachment_type=AttachmentType.PNG)

def take_screenshot_to_local(driver, name="skip_debug"):
    """手動截圖工具，適合 debug skip 判斷"""
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    path = os.path.join(screenshot_dir, filename)
    
    try:
        driver.save_screenshot(path)
        print(f"📸 Screenshot saved to {path}")
    except Exception as e:
        print(f"❌ Failed to take screenshot: {e}")
    return path