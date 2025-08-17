import asyncio
from gamepad import GamePadServer
from burgerbot import Burgerbot

bot = Burgerbot()
bot.speed = 0.75

async def monitor_gamepad(gamepad):
    """
    Monitor the gamepad for commands and act on them.
    """
    
    # This is ugly code - there are better ways of doing this, but it works
    while True:

        if gamepad.is_up:
            print('Robot forward')
            bot.forward()
        elif gamepad.is_down:
            print('Robot backward')
            bot.backward()
        elif gamepad.is_left:
            print('Robot left')
            bot.turn_left()
        elif gamepad.is_right:
            print('Robot right')
            bot.turn_right()
        elif gamepad.is_a:
            print('A button pressed - pen up')
            bot.pen_up()
        elif gamepad.is_b:
            print('B button pressed - pen down')
            bot.pen_down()
        elif gamepad.is_x:
            print('X button pressed')
        elif gamepad.is_y:
            print('Y button pressed')
        elif gamepad.is_start:
            print('Start button pressed')
        elif gamepad.is_select:
            print('Select button pressed')
        elif gamepad.is_menu:
            print('Menu button pressed')
        else:
            pass
            bot.stop()
        await asyncio.sleep(0.1)  # Avoid tight looping


async def main():
    """
    Run the gamepad server and command monitoring concurrently.
    """
    gamepad = GamePadServer()
    
    #Create the background tasks
    blink = asyncio.create_task(gamepad.blink_task())
    monitor = asyncio.create_task(monitor_gamepad(gamepad))

    # Add the tasks to the tasks queue
    gamepad.tasks.append(monitor)
    gamepad.tasks.append(blink)
    
    await gamepad.main()
    
# Run the main coroutine
while True:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
        import sys
        sys.exit()
