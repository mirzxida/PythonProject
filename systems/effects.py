class Effects:
    def __init__(self):
        self.flash = 0
        self.shake = 0
    def trigger(self):
        self.flash = 10
        self.shake = 6
    def update(self):
        if self.flash > 0:
            self.flash -= 1
        if self.shake > 0:
            self.shake -= 1