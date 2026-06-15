class Taxi:
    def __init__(self,name):
        self.name = name 
        self.curr_pos = "A"
        self.tot_amt = 0
        self.time = 0
        self.is_avail = True

    def get_id(self):
        return self.name

    def get_total_amt(self):
        return self.tot_amt
    
    def set_total_amt(self,amt):
        self.tot_amt += amt

    def get_curr_pos(self):
        return self.curr_pos
    
    def set_curr_pos(self,pos):
        self.curr_pos = pos

    def __str__(self):
        return f"""Taxi - {self.name}         Total Earning: {self.get_total_amt()}"""
    
    
