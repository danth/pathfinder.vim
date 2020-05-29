class Motion:
    def __init__(self, dict):
        self.motion = dict["motion"].decode()
        self.weight = dict["weight"]
        self.description_template = dict["description"].decode()

    def description(self, count):
        return self.description_template.format(count=count)
