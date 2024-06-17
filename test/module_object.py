####################################################################
### Objects                                                      ###
####################################################################

class ANIM_SEQ:

    def __init__(self, num_pix = 0, dir = False):
        
        self.num_pix = num_pix      # Number of LED Pixel
        self.pos = 0                # Position
        self.dir = dir              # False = Left | True = Right
        self.anim = False           # Animation State
        self.color_off = 0          # Color-Table "OFF"
        self.color_on = 0           # Color-Table "ON"
        self.color_anim = 0         # Color-Table "ANIM"
    
    def get_num_pix(self):
        return self.num_pix
    
    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos
    
    def set_dir(self, dir):
        self.dir = dir

    def anim_step(self):
        if self.dir == True:
            if self.pos < self.num_pix - 1:
                self.pos = self.pos + 1
            else:
                self.pos = 0
        else:
            if self.pos > 0:
                self.pos = self.pos - 1
            else:
                self.pos = self.num_pix - 1
        return self.pos


# ------------------------------------------------------------------------------
# --- Main Function                                                          ---
# ------------------------------------------------------------------------------
def main():

    print("Object -> Setup")
    led_obj = LED_OBJ(20)
    print("Decode -> Test")
    print("Get -> num_pix = ", led_obj.get_num_pix())
    led_obj.set_pos(10)
    print("Get -> pos = ", led_obj.get_pos())
    print("-----------------------------------")
    led_obj.set_dir(True)
    print("Schleife")
    for i in range(0, 20):
        print("Get -> pos = ", led_obj.anim_step())
        #print("Get -> pos = ", led_obj.get_pos())
        time.sleep(0.5)
    print("-----------------------------------")



# ==============================================================================

# ###############################################################################
# ### Main                                                                    ###
# ###############################################################################

if __name__ == "__main__":

    import time # type: ignore

    main()

    # Normal sollte das Programm hier nie ankommen !
    print("End of Programm !!!")

# ##############################################################################
