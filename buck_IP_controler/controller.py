# Scripts/buck/controller.py
import bisect

class PIController:
    def __init__(self, Kp=0.35, Ki=0.01):
        """
        Kp: Proportional gain
        Ki: Integral gain
        """
        self.Kp = Kp
        self.Ki = Ki
        self.integral = 0.0

    def update(self, Vref, Vout, Ts):
        """
        Compute duty cycle based on PI control law.
        Returns a float in [0,1].
        """
        error = Vref - Vout # how far the actual output is from the desired output
        self.integral += error * Ts #sums the error over time also scaled by sampling period
        u = self.Kp * error + self.Ki * self.integral 
        
        '''
        Kp * error: proportional term (immediate reaction to error).
        Ki * self.integral: integral term (correction based on accumulated past error)
        '''
        
        # Anti-windup
        return max(0.0, min(u, 1.0))


def get_pwr_target(wind_speed, lookup_table):

    # Extract/verify sorted speeds
    speeds = [s for s, _ in lookup_table]
    assert speeds == sorted(speeds), "lookup_table must be sorted by wind speed"

    idx = bisect.bisect_left(speeds, wind_speed) #first table entry ≥ your speed
    
    #edge cases
    if idx == 0:
        return lookup_table[0][1] #first entry
    if idx >= len(lookup_table):
        return lookup_table[-1][1]#last entry

    #look at other index 
    s0, v0 = lookup_table[idx - 1] #entry just below your wind speed.
    s1, v1 = lookup_table[idx]#entry just above

    if s1 == s0:
        return v0
    
    #how far you are between those two speeds
    frac = (wind_speed - s0) / (s1 - s0)

    #try and get somewhere in the middle
    return v0 + frac * (v1 - v0)
