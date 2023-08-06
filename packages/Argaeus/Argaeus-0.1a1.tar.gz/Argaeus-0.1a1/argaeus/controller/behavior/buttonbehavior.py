from enum import Enum


class ButtonBehavior(Enum):
    ToDefaultMode = 0  # change current mode to defined default mode
    ToggleActivePassive = 1  # change behavior of thermostat from observer to actuator (connect DAC to out)
    ResetToDefaultTemp = 2  # set-point for mode is changed to default temp

    @staticmethod
    def factory(name):
        if name.lower() == "to-default-mode":
            return ButtonBehavior.ToDefaultMode
        elif name.lower() == "toggle-active-passive":
            return ButtonBehavior.ToggleActivePassive
        elif name.lower() == "reset-to-default-temp":
            return ButtonBehavior.ResetToDefaultTemp
        else:
            raise ValueError("ButtonBehavior.factory - unknown value '{}'.".format(name))
