class Motion:
    def __init__(self, input_dict):
        self.motion = input_dict["motion"].decode()
        self.weight = int(input_dict["weight"])
        self.description_template = input_dict["description"].decode()

    def description(self, count):
        return self.description_template.format(count=count)
