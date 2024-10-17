class Circle:
    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius

    def __contains__(self, point):
        if (point[0] - self.centre[0]) ** 2 + (
            point[1] - self.centre[1]
        ) ** 2 <= self.radius**2:
            return True
        else:
            return False