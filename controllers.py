import pygame
from enum import IntEnum

class Controller:
    """
       Abstract class to make using pygame's joysticks easier.
       The goal of this class is to be pretty generic, so as to allow for specific controller types to be created from this class.
    """
    def __init__(self, joystickId):
        """
            initializes this controller with the passed joystickId
            :param joystickId: the number of the joystick you want to initialize this controller with. must be at least 0 and less than the number of joysticks obtained by `pygame.joystick.get_count()` 
        """
        # create a joystick from that passed joystickId and initialize that joystick
        self.__joystick = pygame.joystick.Joystick(joystickId)
        self.__joystick.init()
        # create a dict for the button mappings
        self.__buttonMappings = {}
        """
            a dict of integer -> dict values.
            The integer key is the number associated with the button on our joystick,
            and the dict value contains a string of either 'press' or 'release',
            the value of that key being a 0-argument function to be called when that button is either pressed or released.
            for example, and entry may look like this::
            
                {0: {
                    'press': lambda: print('pressed'),
                    'release': lambda: print('released')
                    }
                }
        """
        # create a dict for the directional mappings
        self.__directionalMappings = {}
        """
            a dict of integer -> dict values.
            The integer key is the number associated with the id of the corresponding axis on our joystick,
            and the dict value contains a string of either 'positive', 'negative', or 'release'.
            For each of those keys, the value is a 0-argument function that gets called when that axis is pushed in that direction.
            for example, and entry may look like this::
            
                {0: {
                    'positive': lambda: print('moved in the positive direction'),
                    'negative': lambda: print('moved in the negative direction'),
                    'release': lambda: print('released axis')
                    }
                }
        """
        # set the id of this controller to the one passed in
        self.__joystickId = joystickId
        # an empty function to default to for button commands
        self.__UNMAPPED_COMMAND = (lambda: None)
        
    def get_controllerNumber(self):
        return self.__joystickId
    
    def get_buttonState(self, buttonId):
        """
            Wrapper method for `pygame.joystick.get_button()`
            
            :param buttonId: the number assigned to the button we are getting the state of
            :return: the value returned by `pygame.joystick.get_button()`
        """
        return self.__joystick.get_button(buttonId)

    def map_button(self, buttonId, pressCommand = None, releaseCommand = None):
        """
            Used to bind a function to the pressing and releasing of a button with the passed buttonId.
            
            :param buttonId: the number associated with the button on the controller we are mapping the functions to
            :param pressCommand: a 0-length function to be called when the button is pressed down. If `None` is passed in, then the button's press command will be unmapped
            :param releaseCommand: a 0-length function to be called when the button is released. If `None` is passed in, then the button's release command will be unmapped
        """
        # delete the existing mapping if it exists, as no matter how this function is called, the mappings would be overwritten
        if buttonId in self.__buttonMappings:
            del self.__buttonMappings[buttonId]
        # if press command is None, turn it into a lambda that does nothing
        pressCommand = self.__UNMAPPED_COMMAND if pressCommand is None else pressCommand
        # ... same with release command
        releaseCommand = self.__UNMAPPED_COMMAND if releaseCommand is None else releaseCommand
        # now add the mapping
        self.__buttonMappings[buttonId] = {'press': pressCommand, 'release': releaseCommand}
        
    def map_directionalButton(self, axisId, positiveCommand = None, negativeCommand = None, releaseCommand = None):
        """
            Used to bind a function to the change in state of one of the controller's axes (e.g. a directional pad).
            Each axis has 2 directions, positive and negative. In pygame, they are represented with a positive number and a negative number (approximately 1/-1).
            Pygame also has a state for when an axis is released, denoted as 0
            
            :param axisId: the number associated with the axis on the controller we are mapping functions to
            :param positiveCommand: a 0-length function to be called when the axis's positive end is pushed. If `None` is passed in, then the positive command for that action will be unmapped
            :param negativeCommand: a 0-length function to be called when the axis's negative end is pushed. If `None` is passed in, then the negative command for that action will be unmapped
            :param releaseCommand: a 0-length function to be called when one of the axis's ends was released. If `None` is passed in, then the release command for that action will be unmapped
        """
        # delete the existing mappings for the axis if they already exist, as no matter what they will be overwritten
        if axisId in self.__directionalMappings:
            del self.__directionalMappings[axisId]
        # for each of the commands that are None, assign an empty lambda to them
        positiveCommand = self.__UNMAPPED_COMMAND if positiveCommand is None else positiveCommand
        negativeCommand = self.__UNMAPPED_COMMAND if negativeCommand is None else negativeCommand
        releaseCommand = self.__UNMAPPED_COMMAND if releaseCommand is None else releaseCommand
        # now add the mappings for the axis
        self.__directionalMappings[axisId] = {'positive': positiveCommand, 'negative': negativeCommand, 'release': releaseCommand}
    
    def press_button(self, buttonId):
        """
            Calls the function mapped to when the button with the associated buttonId is pressed. If the button has nothing mapped to it being pressed, nothing will happen
            
            :param buttonId: the id of the button being pressed
        """
        # first check if the buttonId is in our mappings before we try to access it
        if buttonId in self.__buttonMappings:
            # call the associated function
            self.__buttonMappings[buttonId]['press']()
    
    def release_button(self, buttonId):
        """
            Calls the function mapped to when the button with the associated buttonId is released. If the button has nothing mapped to it being released, nothing will happen
            
            :param buttonId: the id of the button being released
        """
        # first check if the buttonId is in our mappings before we try to access it
        if buttonId in self.__buttonMappings:
            # call the associated function
            self.__buttonMappings[buttonId]['release']()
    
    def press_directionalButton(self, axisId, direction):
        """
            Executes the function bound to the passed direction on the axis with the associated axisId. If there is no function bound to that direction or axis, nothing is called.
            
            :param axisId: the id of the axis being pushed in a direction
            :param direction: a positive number, negative number, or 0. This number represents the state of the axis, with a positive number for the positive end, a negative number for the negative end, and 0 for one of the ends being released
        """
        if axisId in self.__directionalMappings:
            # determine which function to call based on the state of the axis (negative, 0, or positive)
            if direction < 0:
                self.__directionalMappings[axisId]['negative']()
            elif direction == 0:
                self.__directionalMappings[axisId]['release']()
            else:
                self.__directionalMappings[axisId]['positive']()
