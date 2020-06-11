from pathfinder.debytes import debytes


class Motion:
    def __init__(self, input_dict):
        self.motion = debytes(input_dict["motion"])
        self.weight = int(input_dict["weight"])
        self.description_template = debytes(input_dict["description"])

        if "name" in input_dict:
            # A custom name for the motion was given, e.g. CTRL-f rather than \<C-f>
            self.name = debytes(input_dict["name"])
        else:
            self.name = self.motion

    def description(self, count):
        return self.description_template.replace("{count}", str(count))
