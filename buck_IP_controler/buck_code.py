import time
from controller import PIController, get_pwr_target
import hardware as helpers
from parse import  get_last_wind_speed
import csv

R1 = 100e3   # top resistor (Ω)
R2 =  10e3   # bottom resistor (Ω)
DIV_INV = 1.0
#(R1 + R2) / R2

LOCAL_PATH = "/home/pi/data/wind_data.csv"



def main():
    Ts = 0.001  # 1 ms loop time → 1 kHz
    ctrl = PIController(Kp=0.35, Ki=0.01)

    # open CSV and write header
    #csvfile = open('buck_log.csv', 'w', newline='')
    #writer  = csv.writer(csvfile)
    #writer.writerow(['timestamp','step','Vin','Vout','Target','Duty'])

    wind_power_table = [
        (4.0, 16.42),
        (4.5, 23.38),
        (5.0, 32.07),
        (5.5, 42.69),
        (6.0, 55.42),
        (6.5, 70.45),
        (7.0, 87.96),
        (7.5, 108.13),
        (8.0, 131.16),
        (8.5, 157.23),
        (9.0, 186.53),
        (9.5, 219.24),
        (10.0, 255.55),
        (10.5, 295.65),
        (11.0, 339.73),
        (11.5, 387.98),
        (12.0, 440.59),
        (12.5, 497.75),
        (13.0, 559.65),
    ]



    # Initialize ADC & PWM
    helpers.init_adc(bus=0, device=0, max_speed_hz=100000)
    helpers.init_pwm(pin=12, freq_hz=int(1/Ts))

    next_time = time.time()
    step = 0

    try:
        while True:
            # Reading
            measured_vout = helpers.read_voltage(channel=1, vref=5.0) * DIV_INV
            vin = helpers.read_voltage(channel=2, vref=5.0) * DIV_INV
            current = helpers.read_current(channel=3, vref=5.0) * DIV_INV


    
            try:
                wind_speed = get_last_wind_speed(LOCAL_PATH)
            except Exception:
                wind_speed = None

                        
            if wind_speed is not None and current > 0:
                pwr_target = get_pwr_target(wind_speed, wind_power_table)
                Vout_target = pwr_target / current
            else:
                Vout_target = 60
            

            Vout_target = min(Vout_target, vin)
            duty =  ctrl.update(Vout_target, measured_vout, Ts)

            helpers.set_duty_cycle(duty)

            print(f"Step {step:4d} | vout = {measured_vout:6.3f} V | vin = {vin:6.3f} |Current = {current:6.3f} Target Vout = {Vout_target:6.23} V | Duty = {duty*100:5.1f}%")

            #writer.writerow([time.time(), step, vin, measured_vout, Vout_target, duty])
            #csvfile.flush()            
            
            
            step += 1

            # Timing control
            next_time += Ts
            sleep = next_time - time.time()
            if sleep > 0:
                time.sleep(sleep)
            else:
                next_time = time.time()

    except KeyboardInterrupt:
        print("Stopping…")
    finally:
        #csvfile.close()
        helpers.shutdown()
if __name__ == "__main__":
    main()
