class Motion:
    def __init__(self, input_dict):
        self.motion = input_dict["motion"].decode()
        self.weight = int(input_dict["weight"])
        self.description_template = input_dict["description"].decode()

        if "name" in input_dict:
            # A custom name for the motion was given, e.g. CTRL-f rather than \<C-f>
            self.name = input_dict["name"].decode()
        else:
            self.name = self.motion

    def description(self, count):
        return self.description_template.replace("{count}", str(count))
