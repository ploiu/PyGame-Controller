# About
PyGame-Controller is an abstraction layer on top of [PyGame](https://www.pygame.org/wiki/about)'s Joystick module. I started this project because I wanted an **easy** and **reusable** way to create controller mappings without cluttering my code with event handlers and conditional blocks. It allows for easy registration of functions to buttons on the controller.

# Features
- Easy setup: give the constructor the controller's number and you're all set!
- Easy button mapping: add, update, and remove button mappings in a single line!
- Easy execution: pass a registered button's id to the `press_button` or `release_button` function and watch the magic!

# Examples:
#### register player 1's controller to print to the console when button 0 is pressed and released:
```python
# ... imports, initialize PyGame, and other logic

# create a list of controllers for each joystick PyGame detects
controllers = [controller.Controller(joystickId) for joystickId in range(pygame.joystick.get_count())]

# bind button 0 on the first controller to do something when pressed and released
controllers[0].map_button(0, lambda: print('button 0 pressed!'), lambda: print('button 0 released!'))

# ... (in event loop) execute the action bound to a button press when a PyGame event is fired
controllerNumber = event.joy
controllerEvent = controllers[controllerNumber]
# Tell the controller to press the button for the event
if event.type == pygame.JOYBUTTONDOWN:
	gamepad.press_button(event.button)
elif event.type == pygame.JOYBUTTONUP:
	gamepad.release_button(event.button)
```
