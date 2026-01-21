import time
from controller import PIController, get_pwr_target
import hardware as helpers
import csv

R1 = 100e3   # top resistor (Ω)
R2 =  10e3   # bottom resistor (Ω)
DIV_INV = 1.0
#(R1 + R2) / R2

LOCAL_PATH = "/home/pi/data/wind_data.csv"



def main():
    Ts = 0.001  # 1 ms loop time → 1 kHz
    ctrl = PIController(Kp=0.35, Ki=0.01)


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

            Vout_target = 2.5

            Vout_target = min(Vout_target, vin)

            duty =  Vout_target/vin

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
