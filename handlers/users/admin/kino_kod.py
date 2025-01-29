import random
class CodeManager:
    def __init__(self, min_value=100, max_value=100000):
        self.available_codes = set(range(min_value, max_value))
        self.used_codes = set()
    def generate_kod(self):
        if not self.available_codes:
            raise Exception("Barcha mumkin bo'lgan kodlar ishlatib bo'lingan.")
        kod = random.choice(list(self.available_codes))
        self.available_codes.remove(kod)
        self.used_codes.add(kod)
        return kod
    def release_kod(self, kod):
        if kod in self.used_codes:
            self.used_codes.remove(kod)
            self.available_codes.add(kod)

