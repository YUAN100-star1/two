import pyautogui
import time
import threading
from pynput import mouse, keyboard

class AutoClicker:
    def __init__(self):
        self.positions = []
        self.running = False
        self.clicking = False
        self.click_interval = 95
        self.click_thread = None
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()  

    def on_click(self, x, y, button, pressed):
        if not self.running or self.clicking:
            return
        if pressed and button == mouse.Button.left:
            self.positions.append((x, y))
            print(f"位置 {len(self.positions)} 已记录: ({x}, {y})")
            if len(self.positions) == 2:
                print("开始自动点击...")
                self.start_clicking()

    def on_press(self, key):
        try:
            if key == keyboard.Key.f9:
                self.toggle_program()
            elif key == keyboard.Key.esc:
                print("正在退出程序...")
                self.stop_program()
                self.keyboard_listener.stop()
                return False
        except AttributeError:
            pass

    def start_clicking(self):
        self.clicking = True
        self.click_thread = threading.Thread(target=self.click_loop)
        self.click_thread.daemon = True
        self.click_thread.start()

    def click_loop(self):
        position_index = 0
        while self.clicking and self.running:
            x, y = self.positions[position_index]
            pyautogui.moveTo(x, y)
            pyautogui.click()
            position_index = 1 - position_index
            time.sleep(self.click_interval)

    def toggle_program(self):
        if self.running:
            self.stop_program()
        else:
            self.start_program()

    def start_program(self):
        self.running = True
        self.positions = []
        self.clicking = False
        if not self.mouse_listener.is_alive():
            self.mouse_listener.start()
        print("程序已启动，请点击两个位置...")

    def stop_program(self):
        self.running = False
        self.clicking = False
        print("程序已停止")

    def run(self):
        print("自动点击程序已就绪")
        print("按 F9 键开始/停止程序")
        print("按 ESC 键退出程序")
        
        
        self.keyboard_listener.join()

if __name__ == "__main__":
    auto_clicker = AutoClicker()
    auto_clicker.run()