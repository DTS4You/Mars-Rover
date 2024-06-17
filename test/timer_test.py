# YD-RP2040 Board
# User Button (GPIO24)
# User LED    (GPIO25)

import time # type: ignore
from machine import Pin, Timer # type: ignore
 
usr_led = Pin(25, Pin.OUT)

Counter_1 = 0
Counter_2 = 0

# ==============================================================================

def timer_1_call(tim):
    global Counter_1
    Counter_1 = Counter_1 + 1
    print("Timer 1 ", Counter_1)
    usr_led.value(Counter_1%2)
 

# ==============================================================================

def timer_2_call(tim):
    global Counter_2
    Counter_2 = Counter_2 + 1
    print("Timer 2 ", Counter_2)

# ###############################################################################
# ### Function ->                                                             ###
# ###############################################################################

def main():

    timer_1 = Timer(-1)
    timer_1.init(period=300, mode=Timer.PERIODIC, callback=timer_1_call)
    
    timer_2 = Timer(-1)
    timer_2.init(period=1000, mode=Timer.PERIODIC, callback=timer_2_call)

    try:
        print("Start")
        while(True):
            time.sleep(4)
            print("Run")

    except KeyboardInterrupt:
        print("-> Keyboard Interrupt")

    finally:
        print("-> Exiting the program")
        timer_1.deinit()
        timer_2.deinit()
        usr_led.value(0)
 

    print("=== End of Main ===")

   

# ###############################################################################
# ### Main                                                                    ###
# ###############################################################################

if __name__ == "__main__":
    
    main()      # Start Main $$$

# Normal sollte das Programm hier nie ankommen !
print("___ End of Programm ___ !!!")

# ##############################################################################
