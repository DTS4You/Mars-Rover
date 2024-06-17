######################################################
### Main-Program                                   ###
### Projekt: Hera-Mission                          ###
### Version: 1.00                                  ###
######################################################
from machine import Pin, Timer                              # type: ignore
from libs.module_init import Global_Module as MyModule
import time                                                 # type: ignore

anim_loop_div = 1

state_0_flag = False

class AnimSeq:
    def __init__(self):
        self.pos = 0
        self.max = 7
        self.end = False
        self.state_flag = False
        self.button_flag = False
        self.wait_tick = 0
        self.wait_count = 100
    
    def reset(self):
        self.pos = 0
        self.end = False
        self.state_flag = False
        self.button_flag = False

    def get_state(self):
        return self.pos

    def next_state(self):
        if self.pos > self.max and not self.end:
            self.pos = 0
            self.end = True
        else:
            self.pos = self.pos + 1
            self.state_flag = False
        return self.pos
    
    def wait(self):
        if self.wait_tick < self.wait_count:
            self.wait_tick = self.wait_tick + 1
        else:
            self.wait_tick = 0
            self.next_state()

def anim_step():
    #print("Anim-Step")
    if myseq.get_state() == 0:
        if myseq.state_flag == False:
            print("State -> 0")
            MyWS2812.do_all_def()
            MyGPIO.i2c_write(7, False)
            myseq.state_flag = True
    
    if myseq.get_state() == 1:
        if myseq.state_flag == False:
            print("State -> 1")
            MyWS2812.do_all_off()
            MyGPIO.i2c_write(7, True)
            myseq.state_flag = True
        myseq.wait()
    
    if myseq.get_state() == 2:
        if myseq.state_flag == False:
            print("State -> 2")
            myseq.state_flag = True
            MyWS2812.do_show_def(5)
            MyWS2812.do_show_def(4)
        if not MyWS2812.get_anim_end(5):
            MyWS2812.do_anim_step(5)
        else:
            MyWS2812.set_anim_end(5)
            myseq.next_state()
        if not MyWS2812.get_anim_end(4):
            MyWS2812.do_anim_step(4)
        else:
            MyWS2812.set_anim_end(4)

    if myseq.get_state() == 3:
        if myseq.state_flag == False:
            print("State -> 3")
            MyWS2812.set_anim_pos(0, 3)
            myseq.state_flag = True
        if not MyWS2812.get_anim_end(5):
            MyWS2812.do_anim_step(5)
            if MyWS2812.get_anim_pos(5) > ( 161 - 31 - 4 ):          # Trefferposition auf Außenbahn bei 161
                if not MyWS2812.get_anim_end(0):
                    MyWS2812.do_anim_step(0)
                else:
                    MyWS2812.set_anim_end(0)
                    myseq.next_state()
        if not MyWS2812.get_anim_end(4):
            MyWS2812.do_anim_step(4)
        else:
            MyWS2812.set_anim_end(4)
    
    if myseq.get_state() == 4:                  # Aufschlag
        if myseq.state_flag == False:
            print("State -> 4")
            MyWS2812.do_all_off()
            #MyWS2812.do_show_def(1)
            myseq.state_flag = True
        if not MyWS2812.get_anim_end(1):
            MyWS2812.do_anim_step(1)
        else:
            MyWS2812.set_anim_end(1)
            myseq.next_state()
    
    if myseq.get_state() == 5:                  # Neue Bahn
        if myseq.state_flag == False:
            print("State -> 5")
            MyWS2812.do_all_off()
            myseq.state_flag = True
            MyWS2812.set_anim_pos(2, 135)
            MyWS2812.set_anim_pos(3, 137)
        if not MyWS2812.get_anim_end(3):
            MyWS2812.do_anim_step(3)
        else:
            MyWS2812.set_anim_end(3)
            myseq.next_state()
        if not MyWS2812.get_anim_end(2):
            MyWS2812.do_anim_step(2)
        else:
            MyWS2812.set_anim_end(2)

    if myseq.get_state() == 6:
        if myseq.state_flag == False:
            print("State -> 6")
            #MyWS2812.do_all_def()
            myseq.state_flag = True
        if not MyWS2812.get_anim_end(3):
            MyWS2812.do_anim_step(3)
        else:
            MyWS2812.set_anim_end(3)
            myseq.next_state()
        if not MyWS2812.get_anim_end(2):
            MyWS2812.do_anim_step(2)
        else:
            MyWS2812.set_anim_end(2)

    if myseq.get_state() == 7:
        if myseq.state_flag == False:
            print("State -> 7")
            MyWS2812.do_all_def()
            MyGPIO.button_reset()
            MyGPIO.i2c_all_off()
            myseq.reset()

# ------------------------------------------------------------------------------
# --- Main Function                                                          ---
# ------------------------------------------------------------------------------
def main():
    
    global myseq

    myseq = AnimSeq()

    print("=== Start Main ===")
    
    anim_couter = 0
    
    MyGPIO.i2c_write(0, True)

    try:
        print("Start Main Loop")
 
        while MySerial.sercon_read_flag():
            
            if anim_couter > anim_loop_div:     # Loop / Loop_div -> anim_step
                    anim_couter = 0
                    anim_step()

            MyGPIO.button_poll()

            if MyGPIO.button_get_state() and not myseq.button_flag:
                myseq.next_state()
                myseq.button_flag = True
                
            
            MySerial.sercon_read_line()
            if MySerial.get_ready_flag():       # Zeichenkette empfangen
                #print(MySerial.get_string())
                MyDecode.decode_input(str(MySerial.get_string()))
                #MyDecode.decode_printout()
                if MyDecode.get_valid_flag() == True:
                    #print("Valid Command")
                    if MyDecode.get_cmd_1() == "do":
                        #print("do")
                        if MyDecode.get_cmd_2() == "all":
                            #print("all")
                            if MyDecode.get_value_1() == 0:
                                #print("off")
                                MyWS2812.do_all_off()
                            if MyDecode.get_value_1() == 1:
                                #print("on")
                                MyWS2812.do_all_on()
                            if MyDecode.get_value_1() == 2:
                                #print("def")
                                MyWS2812.do_all_def()
                        if MyDecode.get_cmd_2() == "obj":
                            #print("obj")
                            #print(MyDecode.get_value_1())
                            #print(segment_map[MyDecode.get_value_1()])
                            if MyDecode.get_value_1() == 1:
                                MyWS2812.set_led_obj(0, MyDecode.get_value_2())
                            
                            if MyDecode.get_value_1() == 2:
                                MyWS2812.set_led_obj(1, MyDecode.get_value_2())

                            # ------------------------------------------------------------------
                            if MyDecode.get_value_1() == 81:
                                print("Motor 1 -> " + MyDecode.get_value_2())
                                if MyDecode.get_value_2() == "on":
                                    MyGPIO.i2c_write(0, True)
                                else:
                                    MyGPIO.i2c_write(0, False)
                            
                            if MyDecode.get_value_1() == 82:
                                print("Motor 2 -> " + MyDecode.get_value_2())
                                if MyDecode.get_value_2() == "on":
                                    MyGPIO.i2c_write(1, True)
                                else:
                                    MyGPIO.i2c_write(1, False)

                            if MyDecode.get_value_1() == 83:
                                print("Motor 3 -> " + MyDecode.get_value_2())
                                if MyDecode.get_value_2() == "on":
                                    MyGPIO.i2c_write(2, True)
                                else:
                                    MyGPIO.i2c_write(2, False)
                                
                            if MyDecode.get_value_1() == 84:
                                print("Motor 4 -> " + MyDecode.get_value_2())
                                if MyDecode.get_value_2() == "on":
                                    MyGPIO.i2c_write(3, True)
                                else:
                                    MyGPIO.i2c_write(3, False)

                            if MyDecode.get_value_1() == 85:
                                print("Motor 5 -> " + MyDecode.get_value_2())
                                if MyDecode.get_value_2() == "on":
                                    MyGPIO.i2c_write(4, True)
                                else:
                                    MyGPIO.i2c_write(4, False)

                            if MyDecode.get_value_1() == 86:
                                print("Motor 6 -> " + MyDecode.get_value_2())
                                if MyDecode.get_value_2() == "on":
                                    MyGPIO.i2c_write(5, True)
                                else:
                                    MyGPIO.i2c_write(5, False)
                        
                            if MyDecode.get_value_1() == 87:
                                print("Motor -> " + MyDecode.get_value_2())
                                if MyDecode.get_value_2() == "on":
                                    MyGPIO.i2c_write(6, True)
                                else:
                                    MyGPIO.i2c_write(6, False)

                            if MyDecode.get_value_1() == 88:
                                print("Lampe -> " + MyDecode.get_value_2())
                                if MyDecode.get_value_2() == "on":
                                    MyGPIO.i2c_write(7, True)
                                else:
                                    MyGPIO.i2c_write(7, False)

                    if MyDecode.get_cmd_1() == "test":
                        #print("Test")
                        if MyDecode.get_cmd_2() == "led":
                            #print("LED")
                            MyWS2812.test_led(MyDecode.get_value_1(), MyDecode.get_value_2())
                    

            anim_couter = anim_couter + 1
            # Loop-Delay !!!
            time.sleep_ms(10)        # 10ms
    
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    finally:
        print("Exiting the program")
        MyWS2812.do_all_off()
        MyGPIO.i2c_all_off()   

    print("=== End of Main ===")

# ==============================================================================
# ==============================================================================
    
# ###############################################################################
# ### Main                                                                    ###
# ###############################################################################


if __name__ == "__main__":

    if MyModule.inc_i2c:
        #print("I2C_MCP23017 -> Load-Module")
        import libs.module_i2c as MyGPIO
        #print("I2C -> Setup")
        MyGPIO.i2c_setup()
        ### Test ###
        #print("I2C -> SetOutput")
        #MyGPIO.i2c_write(0,True)
        #time.sleep(0.5)
        #MyGPIO.i2c_write(0,False)

    if MyModule.inc_ws2812:
        #print("WS2812 -> Load-Module")
        import libs.module_ws2812_v3 as MyWS2812         # Modul WS2812  -> WS2812-Ansteuerung
        #print("WS2812 -> Setup")
        MyWS2812.setup_ws2812()
        ### Test ###
        #print("WS2812 -> Run self test")
        #MyWS2812.self_test()
        #print("WS2812 -> Blink Test")
        #MyWS2812.do_blink_test()
        #print("WS2812 -> Dot-Test")
        #MyWS2812.do_dot_test()

    if MyModule.inc_decoder:
        #print("Decode -> Load-Module")
        import libs.module_decode as MyDecode
        #print("Decode -> Setup")
        MyDecode.decode_setup()
        ### Test ###
        #print("Decode -> Test")
        #MyDecode.decode_input("Test")

    if MyModule.inc_serial:
        #print("Serial-COM -> Load-Module")
        import libs.module_serial as MySerial
        #print("Serial-Con -> Setup")
        MySerial.sercon_setup()
        ### Test ###
        #print("Serial-Con -> Test")
        #MySerial.sercon_write_out("Start Test")

    main()      # Start Main $$$

# Normal sollte das Programm hier nie ankommen !
print("___End of Programm___ !!!")

# ##############################################################################
