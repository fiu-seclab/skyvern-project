import asyncio
import random
import time

import pyautogui
import websockets

print("Starting...")

movement_options = [
    pyautogui.easeInOutQuad,
    pyautogui.easeInQuad,
    pyautogui.easeOutQuad,
    pyautogui.easeInCubic,
    pyautogui.easeOutCubic,
    pyautogui.easeInOutCubic,
]


def get_random(min, max):
    return random.uniform(min, max)


def pyautogui_write(text: str, random_min: float = 0.20, random_max: float = 0.30):
    for char in text:
        pyautogui.write(char, interval=random.uniform(random_min, random_max))
        if random.randint(0, 10) == 5:
            time.sleep(random.uniform(random_min * 3, random_max * 3))
            pyautogui.press(
                "backspace", interval=random.uniform(random_min, random_max)
            )
            pyautogui.write(char, interval=random.uniform(random_min, random_max))


def main():
    # Move to the login form and click it
    pyautogui.moveTo(
        get_random(810, 1100),  # X
        get_random(670, 675),
        duration=random.uniform(0.5, 1.5),
        tween=random.choice(movement_options),
    )
    pyautogui.click()

    # Write the username
    pyautogui_write("admin", random_min=0.20, random_max=0.30)
    pyautogui.press("tab")

    # Write the password
    pyautogui_write("=m&8e@g90NAv", random_min=0.30, random_max=0.35)

    # Click the login button
    # login button x= y=760-790
    pyautogui.moveTo(
        get_random(810, 1100),
        get_random(760, 770),
        duration=random.uniform(0.5, 1.5),
        tween=random.choice(movement_options),
    )
    pyautogui.click()


async def handle_message(websocket: websockets.WebSocketClientProtocol):
    async for message in websocket:
        if message == "run":
            main()
            await websocket.send("done")


async def start_server():
    async with websockets.serve(handle_message, "localhost", 8765):
        print("Pyautogui server running on ws://localhost:8765")
        await asyncio.Future()


asyncio.run(start_server())

# main()
