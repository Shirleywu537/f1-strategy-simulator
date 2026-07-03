class Track:

    def __init__(self, name, base_lap_time, pit_stop_time, safety_car_probability=0.05):
        self.name = name
        self.base_lap_time = base_lap_time
        self.pit_stop_time = pit_stop_time
        self.safety_car_probability = safety_car_probability