class Employees:
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    
    def __str__(self):
        return '{} {} {}'.format(self.first, self.last, self.pay)