###############################################################################
### Test Programm                                                           ###
###############################################################################
# YD-RP2040 Board
# User Button (GPIO24)
# User LED    (GPIO25)

from machine import Pin # type: ignore
import time # type: ignore

def int_button(pin):
    value = not(bool(usr_btn.value()))
    print("Schleife", value)
    usr_led.value(value)


# #############################################################################
# ### Main                                                                  ###
# #############################################################################

def main():
    
    global usr_btn
    global usr_led

    usr_btn = Pin(24, Pin.IN, Pin.PULL_UP)
    usr_led = Pin(25, Pin.OUT)

    usr_btn.irq(trigger=usr_btn.IRQ_FALLING | usr_btn.IRQ_RISING, handler=int_button)

    usr_led.value(1)

    try:
        print("Start")
        while(True):
            time.sleep(0.3)
            print("Run")
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        usr_led.value(0)

    finally:
        print("Exiting the program")
 



# #############################################################################

if __name__ == "__main__":
    
    print("___ Start of Programm ___ !!!")
    
    main()      # Start Main $$$

# Normal sollte das Programm hier nie ankommen !
print("___ End of Programm ___ !!!")

# #############################################################################


