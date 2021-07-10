class Jumper:
    def __init__(self, name, country, inrun, takeoff, flight, style):
        self.name = name
        self.country = country
        self.inrun = inrun
        self.takeoff = takeoff
        self.flight = flight
        self.style = style

    def get_name(self):
        return self.name

    def get_country(self):
        return self.country

    def get_inrun_coeff(self):
        return (100 - self.inrun) / 30

    def get_takeoff_speed(self):
        return 1 + self.takeoff / 100 * 2

    def get_flight_coeffs(self):
        return self.flight

    def get_style(self):
        return self.style

    def __str__(self):
        return f"{self.name} {self.country} | {self.inrun} {self.takeoff} {self.flight} {self.style}"


if __name__ == '__main__':
    x = Jumper("Kamil Stoch", "POL", 80, 85, 95, 98)
    print(x)
