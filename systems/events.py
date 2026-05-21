import random

class Event:
    def __init__(self):
        self.events = ["ENGINE STABILITY: NOMINAL",
                       "WARNING: MICROMETEOROID FIELD",
                       "UNKNOWN SIGNAL DETECTED",
                       "HULL INTEGRITY DROPPING",
                       "SENSOR INTERFERENCE"]
        self.timer = 0
        self.interval = 180
        self.current_event = ""
    def update(self):
        self.timer += 1
        if self.timer >= self.interval:
            self.timer = 0
            self.current_event = random.choice(self.events)
    def get_event(self):
        return self.current_event