###############################################################################
# Module WS2812 V3
###############################################################################
import time # type: ignore
import libs.module_neopixel as module_neopixel
#from libs.module_init import Global_WS2812 as MyGlobal
from libs.module_init import Global_WS2812 as MyGlobal


class LedState:
    def __init__(self):
        self.state = False
        self.blink_state = False

    def set(self, set):
        self.state = set

    def get(self):
        return self.state
    
    def do_blink(self):
        self.blink_state = not self.blink_state

    def get_blink(self):
        return self.blink_state

    def refresh(self):
        self.state = False
        for strips in strip_obj:
            strips.show()


class Ledsegment:

    def __init__(self, neopixel, start, count):
        self.neopixel = neopixel
        self.start = start
        self.stop = self.start + count - 1
        self.count = count
        self.position = 0
        self.direction = True           # False -> Links -> im Uhrzeigersinn | True -> Rechts -> gegen Uhrzeigersinn
        self.run_state = False
        self.mode = True                # False -> 1. Pixel | True -> 4. Pixel
        self.blink_state = False
        self.color_off = (0,0,0)
        self.color_on = (0,0,0)
        self.color_default = (0,0,0)
        self.color_half = (0,0,0)
        self.color_blink_on = (0,0,0)
        self.color_blink_off = (0,0,0)
        self.color_show = (0,0,0)
        self.color_value = (0,0,0)

    def set_color_on(self, color_on):
        self.color_on = color_on

    def set_color_def(self, color_default):
        self.color_default = color_default
        
    def set_color_off(self, color_off):
        self.color_off = color_off

    def set_color_value(self, color_value):
        self.color_value = color_value

    def set_color_show(self, color_value):
        self.color_show = color_value
    
    def set_color_half(self, color_value):
        self.color_half = color_value

    def set_color_blink_off(self, color_value):
        self.color_blink_off = color_value

    def set_color_blink_on(self, color_value):
        self.color_blink_on = color_value

    def set_mode(self, mode):
        self.mode = mode

    def set_pixel(self, pos, color=None):
        if color:
            self.color_value = color
        else:
            self.color_value = self.color_show
        self.neopixel.set_pixel(self.start + pos, self.color_value)

    def show_on(self):
        self.color_show = self.color_on
        self.blink_state = False
        self.set_line()

    def show_def(self):
        self.color_show = self.color_default
        self.blink_state = False
        self.set_line()

    def show_off(self):
        self.color_show = self.color_off
        self.blink_state = False
        self.set_line()

    def show_blink(self):
        self.blink_state = True
        if ledstate.get_blink():
            self.color_show = self.color_blink_on
        else:
            self.color_show = self.color_blink_off
        self.set_line()

    def get_blink_state(self):
        return self.blink_state

    def set_line(self):
        self.neopixel.set_pixel_line(self.start, self.stop, self.color_show)

    def show_stripe(self):
        self.neopixel.show()

    def anim_step(self):
        if self.direction == True:
            if self.position < self.count - 1:
                self.position = self.position + 1
            else:
                self.position = 0
                self.run_state = True
        else:
            if self.position > 0:
                self.position = self.position - 1
            else:
                self.position = self.count - 1
                self.run_state = True
        #print(self.position)
        return self.position
    
    def anim_get_end(self):
        return self.run_state
    
    def anim_set_end(self):
        self.run_state = False

    def anim_show(self):
        self.color_show = self.color_default
        self.set_line()

        if self.mode == True:
            # Draw 1. Pixel
            self.set_pixel(self.position, self.color_half)
            # Draw 2. Pixel
            if self.position > 0:
                self.set_pixel(self.position - 1, self.color_on)
            else:
                self.set_pixel(self.count - 1 + self.position, self.color_on)
            # Draw 3. Pixel
            if self.position > 1:
                self.set_pixel(self.position - 2, self.color_on)
            else:
                self.set_pixel(self.count - 2 + self.position, self.color_on)
            # Draw 4. Pixel
            if self.position > 2:
                self.set_pixel(self.position - 3, self.color_half)
            else:
                self.set_pixel(self.count - 3 + self.position, self.color_half)
        else:
            self.set_pixel(self.position, self.color_on)
        # Draw Stripe
        self.show_stripe()
        self.anim_step()

    def get_position(self):
        return self.position
    
    def set_position(self, pos):
        self.position = pos
    
# =============================================================================

def setup_ws2812():

    global strip_obj
    global led_obj
    global ledstate
    global mg
    
    mg = MyGlobal
    
    led_obj = []
    strip_obj = []

    ledstate = LedState()
    
    strip_obj.append(module_neopixel.Neopixel(mg.numpix_1, 0, 2, "GRB"))
    strip_obj.append(module_neopixel.Neopixel(mg.numpix_2, 1, 3, "GRB"))
    strip_obj.append(module_neopixel.Neopixel(mg.numpix_3, 2, 4, "GRB"))
    strip_obj.append(module_neopixel.Neopixel(mg.numpix_4, 3, 5, "GRB"))
    strip_obj.append(module_neopixel.Neopixel(mg.numpix_5, 4, 6, "GRB"))
    
    led_obj.append(Ledsegment(strip_obj[mg.seg_01_strip], mg.seg_01_start, mg.seg_01_count))      #  (01) -> LED Position -> # 01 #
    led_obj.append(Ledsegment(strip_obj[mg.seg_02_strip], mg.seg_02_start, mg.seg_02_count))      #  (02) -> LED Position -> # 02 #
    led_obj.append(Ledsegment(strip_obj[mg.seg_03_strip], mg.seg_03_start, mg.seg_03_count))      #  (03) -> LED Position -> # 03 #
    led_obj.append(Ledsegment(strip_obj[mg.seg_04_strip], mg.seg_04_start, mg.seg_04_count))      #  (04) -> LED Position -> # 04 #
    led_obj.append(Ledsegment(strip_obj[mg.seg_05_strip], mg.seg_05_start, mg.seg_05_count))      #  (05) -> LED Position -> # 05 #
    led_obj.append(Ledsegment(strip_obj[mg.seg_06_strip], mg.seg_06_start, mg.seg_06_count))      #  (06) -> LED Position -> # 06 #
    
    for strips in strip_obj:
        strips.brightness(255)
   
    # Alle Leds auf Vorgabewert -> aus
    for strips in strip_obj:
        strips.set_pixel_line(0, strips.num_leds - 1, mg.color_off)
    for strips in strip_obj:
        strips.show()

    # Setze Farbwerte in alle LED-Objekte
    for leds in led_obj:
        leds.set_color_off(mg.color_off)
        leds.set_color_def(mg.color_def)
        leds.set_color_on(mg.color_on)
        leds.set_color_value(mg.color_dot)
        leds.set_color_show(mg.color_dot)
        leds.set_color_blink_off(mg.color_blink_off)
        leds.set_color_blink_on(mg.color_blink_on)
    
    led_obj[0].set_color_def(mg.color_anim_1_def)
    led_obj[0].set_color_on(mg.color_anim_1_on)
    led_obj[0].set_color_half(mg.color_anim_1_half)

    led_obj[1].set_color_def(mg.color_off)
    led_obj[1].set_color_on(mg.color_anim_1_on)
    led_obj[1].set_color_half(mg.color_anim_1_half)
    led_obj[1].set_mode(False)

    led_obj[2].set_color_def(mg.color_anim_3_def)
    led_obj[2].set_color_on(mg.color_anim_3_on)
    led_obj[2].set_color_half(mg.color_anim_3_half)

    led_obj[3].set_color_def(mg.color_anim_3_def)
    led_obj[3].set_color_on(mg.color_anim_3_on)
    led_obj[3].set_color_half(mg.color_anim_3_half)

    led_obj[4].set_color_def(mg.color_anim_2_def)
    led_obj[4].set_color_on(mg.color_anim_2_on)
    led_obj[4].set_color_half(mg.color_anim_2_half)

    led_obj[5].set_color_def(mg.color_anim_2_def)
    led_obj[5].set_color_on(mg.color_anim_2_on)
    led_obj[5].set_color_half(mg.color_anim_2_half)
    
    # Blinken aus
    do_all_no_blink()

#==============================================================================

def test_led(stripe, pos):
    do_all_off()
    strip_obj[stripe].set_pixel(pos, (70,70,70))
    ledstate.refresh()

def do_all_on():
    # Setze Farbwerte in alle LED-Objekte
    for leds in led_obj:
        leds.show_on()
    ledstate.refresh()

def do_all_off():
    # Setze Farbwerte in alle LED-Objekte
    for leds in led_obj:
        leds.show_off()
    ledstate.refresh()

def do_all_def():
    # Setze Farbwerte in alle LED-Objekte
    for leds in led_obj:
        leds.show_def()
    ledstate.refresh()

def do_all_no_blink():
    for leds in led_obj:
        leds.blink_state = False

def do_blink():
    ledstate.do_blink()
    for leds in led_obj:
        if leds.get_blink_state():
            leds.show_blink()
        else:
            pass
    
    ledstate.set(True)
    ledstate.refresh()

def do_test_on():
    #print("Test on")
    led_obj[0].show_on()
    led_obj[1].show_on()
    ledstate.set(True)
 
def do_test_off():
    #print("Test off")
    led_obj[0].show_off()
    led_obj[1].show_off()
    ledstate.set(True)

def do_refresh():

    ledstate.refresh()

def do_get_state():

    return ledstate.get()

def set_all_off():                          # Setze Farbwerte in alle LED-Objekte
    # Setze Farbwerte in alle LED-Objekte
    for leds in led_obj:
        leds.show_off()
    ledstate.refresh()

def set_all_def():                          # Setze Farbwerte in alle LED-Objekte
    for leds in led_obj:
        leds.show_def()
    ledstate.refresh()

def set_all_on():                           # Setze Farbwerte in alle LED-Objekte
    for leds in led_obj:
        leds.show_def()
    ledstate.refresh()

def self_test():                                # Pro Stripe einmal Aus-RGB(25%) -Aus 
    for strips in strip_obj:
        # Alle Aus
        strips.set_pixel_line(0, strips.num_leds - 1, (0,0,0))
        strips.show()
        time.sleep(0.3)
        # Alle Rot
        strips.set_pixel_line(0, strips.num_leds - 1, (30,0,0))
        strips.show()
        time.sleep(0.3)
        # Alle Grün
        strips.set_pixel_line(0, strips.num_leds - 1, (0,30,0))
        strips.show()
        time.sleep(0.3)
        # Alle Blau
        strips.set_pixel_line(0, strips.num_leds - 1, (0,0,30))
        strips.show()
        time.sleep(0.3)
        # Alle Aus
        strips.set_pixel_line(0, strips.num_leds - 1, (0,0,0))
        strips.show()
        time.sleep(0.3)


def do_blink_test():
    loops = 4
    looptime = 0.15
    #print(len(led_obj))
    for x in range(len(led_obj)):
        led_obj[x].show_blink()
        for i in range(loops):
            do_blink()
            time.sleep(looptime)
        led_obj[x].show_off()
        do_refresh()
    

def do_obj_on_off_def_off():
    
    delay_time = 0.3
    for x in range(len(led_obj)):
        led_obj[x].show_on()
        do_refresh()
        time.sleep(delay_time)
        led_obj[x].show_off()
        do_refresh()
        time.sleep(delay_time)
        led_obj[x].show_def()
        do_refresh()
        time.sleep(delay_time)
        led_obj[x].show_off()
        do_refresh()

def do_dot_test():
    delay_time = 0.05
    color_now = (0,10,60)
    for y in range(len(led_obj)):
        for x in range(led_obj[y].count):
            if x > 0:
                led_obj[y].set_pixel(x - 1, (0,0,0))
            led_obj[y].set_pixel(x, color_now)
            do_refresh()
            time.sleep(delay_time)
        led_obj[y].show_off()
        do_refresh()
        time.sleep(delay_time)
        
def set_led_obj(obj,state):
    if state == "off":
        led_obj[obj].show_off()
    if state == "def":
        led_obj[obj].show_def()
    if state == "on":
        led_obj[obj].show_on()
    if state == "blink":
        led_obj[obj].show_blink()
    do_refresh()

def do_anim_step(obj):
    led_obj[obj].anim_show()
    #print("Anim Step")

def get_anim_pos(obj):
    return led_obj[obj].get_position()

def set_anim_pos(obj, pos):
    led_obj[obj].set_position(pos)

def set_anim_end(obj):
    led_obj[obj].anim_set_end()

def get_anim_end(obj):
    return led_obj[obj].anim_get_end()

def do_show_off(obj):
    led_obj[obj].show_off()

def do_show_def(obj):
    led_obj[obj].show_def()

def do_show_on(obj):
    led_obj[obj].show_on()

# -----------------------------------------------------------------------------

def main():

    try:
        print("Start")
        
        print("WS2812 -> Setup")
        setup_ws2812()
        
        #print("WS2812 -> Run self test")
        #self_test()
    
        #print("WS2812 -> Start -> Stop")
        #for i in range (0,4):
        #    start_led = 0
        #    stop_led = led_obj[i].count - 1
        #    print("Start -> ", start_led)
        #    print("Stop  -> ", stop_led)
        #    led_obj[i].set_pixel(start_led, (0,60,0))
        #    led_obj[i].set_pixel(stop_led, (60,0,0))
        #do_refresh()

        print("WS2812 -> Anim Test")
        #for i in range(0,80):
        #    if not get_anim_end(0):
        #        do_anim_step(0)
        #    print(get_anim_pos(0))
        #    time.sleep(0.2)

        while(not get_anim_end(0)):
            do_anim_step(0)
            print(get_anim_pos(0))
            time.sleep(0.2)
        set_anim_end(0)
        while(not get_anim_end(0)):
            do_anim_step(0)
            print(get_anim_pos(0))
            time.sleep(0.2)
        print("WS2812 -> Anim End ")

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        
    finally:
        print("Exiting the program")
        # Aufräumen
        do_all_off()
    
    print("WS2812 -> End of Program !!!")

# End

#------------------------------------------------------------------------------
#--- Main
#------------------------------------------------------------------------------

if __name__ == "__main__":
    
    main()
