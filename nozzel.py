import math

class NozzleDesign:
    def __init__(self, F, Pc, Pa, γ, CF, ε):
        self.F = F 
        self.Pc = Pc  
        self.Pa = Pa  
        self.γ = γ  
        self.CF = CF  
        self.ε = ε  

    def calculate_At(self):
        At = self.F / (self.CF * self.Pc)
        return At

    def calculate_Ae(self, At):
        return self.ε * At

    def calculate_exit_pressure(self):
        Pe = self.Pc * (2 / (self.γ + 1)) ** (self.γ / (self.γ - 1)) / self.ε ** ((self.γ - 1) / self.γ)
        return Pe

    def calculate_convergent_angle(self):
        return 45.0 

    def calculate_divergent_angle(self):
        if self.ε < 10:
            return 15.0  
        elif self.ε < 50:
            return 12.0  
        else:
            return 10.0  

    def design_nozzle(self):
        At = self.calculate_At()
        Ae = self.calculate_Ae(At)
        Pe = self.calculate_exit_pressure()
        convergent_angle = self.calculate_convergent_angle()
        divergent_angle = self.calculate_divergent_angle()

        return {
            "Throat Area (At)": At,
            "Exit Area (Ae)": Ae,
            "Exit Pressure (Pe)": Pe,
            "Convergent Angle": convergent_angle,
            "Divergent Angle": divergent_angle,
        }
