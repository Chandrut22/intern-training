from Taxi import Taxi

class BookingSystem:
    def __init__(self):
        self.taxi_details = []

        for i in range(0,4):
            self.taxi_details.append(Taxi(str(i+1)))

    def booking(self,pickup_point,drop_point,pickup_time):
        avail = []
        for taxi in self.taxi_details:
            if(taxi.time <= pickup_time and ord(taxi.get_curr_pos()) <= ord(pickup_point) ):
                avail.append(taxi)
        
        if avail == []: print("Taxi is not available")
        elif(len(avail) > 1): 
            book_taxi = avail[0]
            for i in range(1,len(avail)):
                if(book_taxi.get_total_amt() > avail[i].get_total_amt()): book_taxi = avail[i]
            
            km = abs(ord(drop_point) - ord(pickup_point)) * 15
            amt = 100 + (km - 5) * 10
            book_taxi.set_total_amt(amt)
            book_taxi.set_curr_pos(drop_point)
            book_taxi.time = pickup_time + abs(ord(drop_point) - ord(pickup_point))
            print(f"Taxi {book_taxi.get_id()} is allocated")
        else:
            book_taxi = avail[0]
            km = abs(ord(drop_point) - ord(pickup_point)) * 15
            amt = 100 + (km-5)*10
            book_taxi.set_total_amt(amt)
            book_taxi.set_curr_pos(drop_point)
            book_taxi.time = pickup_time + abs(ord(drop_point) - ord(pickup_point))
            print(f"Taxi {book_taxi.get_id()} is allocated")

    def __str__(self):
        result = ""
        for taxi in self.taxi_details:
            result += str(taxi) + "\n"
        return result



    
