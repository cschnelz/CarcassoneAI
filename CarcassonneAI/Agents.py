#from Action import Action

from typing import List

class HumanAgent():
    def __init__(self):
        pass

    def getResponse(self, validActions):
        for index, action in enumerate(validActions):
            print(f"Option {index}: {action}")

        return validActions[int(input("input desired location: "))]
