# #############################################################################
# ### MyGlobal
# #############################################################################


class Global_Module:
    
    inc_ws2812          = True
    inc_decoder         = True
    inc_serial          = True
    inc_i2c             = True


class Global_WS2812:

    numpix_1            = 36            # Anz. LEDs im 1. Stripe -> Einschlagbahn und Splitter
    numpix_2            = 196           # Anz. LEDs im 2. Stripe -> Umlaufbahn innen innen
    numpix_3            = 196           # Anz. LEDs im 3. Stripe -> Umlaufbahn innen aussen
    numpix_4            = 196           # Anz. LEDs im 4. Stripe -> Umlaufbahn aussen innen
    numpix_5            = 196           # Anz. LEDs im 5. Stripe -> Umlaufbahn aussen aussen
    # numpix_6          = 8             # Anz. LEDs im 6. Stripe -> Splitter-Strahl

    seg_01_strip        = 0             #  1. Seg -> Stripe      # Einschlagbahn
    seg_01_start        = 0             #  1. Seg -> Start
    seg_01_count        = 30            #  1. Seg -> Anzahl

    seg_02_strip        = 0             #  2. Seg -> Stripe      # Splitter
    seg_02_start        = 30            #  2. Seg -> Start
    seg_02_count        = 4             #  2. Seg -> Anzahl

    seg_03_strip        = 1             #  3. Seg -> Stripe      # Umlaufbahn innen innen
    seg_03_start        = 0             #  3. Seg -> Start
    seg_03_count        = 180           #  3. Seg -> Anzahl
    
    seg_04_strip        = 2             #  4. Seg -> Stripe      # Umlaufbahn innen aussen
    seg_04_start        = 0             #  4. Seg -> Start
    seg_04_count        = 180           #  4. Seg -> Anzahl

    seg_05_strip        = 3             #  5. Seg -> Stripe      # Umlaufbahn aussen innen
    seg_05_start        = 0             #  5. Seg -> Start
    seg_05_count        = 180           #  5. Seg -> Anzahl
    
    seg_06_strip        = 4             #  6. Seg -> Stripe      # Umlaufbahn aussen aussen
    seg_06_start        = 0             #  6. Seg -> Start
    seg_06_count        = 180           #  6. Seg -> Anzahl
    

# -----------------------------------------------------------------------------
    #                        R   G   B
    color_def           = (  0,  0,  3)
    color_off           = (  0,  0,  0)
    color_on            = (100,100,100)
    color_dot           = ( 50, 50, 50)
    color_blink_on      = (100,100,100)
    color_blink_off     = ( 30, 30, 30)
    
    color_anim_1_def    = (  0,  0,  3)
    color_anim_1_on     = ( 50, 50,200)
    color_anim_1_half   = (  0,  0,100)
    
    color_anim_2_def    = (  0,  5,  0)
    color_anim_2_on     = (  0,100,  0)
    color_anim_2_half   = (  0, 50,  0)

    color_anim_3_def    = (  5,  0,  0)
    color_anim_3_on     = (100,  0,  0)
    color_anim_3_half   = ( 50,  0,  0)



class Global_Default:

    blink_freq          = 3.0           # Blink Frequenz
    

def main():

    print("Start Global Init")
    mg = Global_WS2812
    print(mg.numpix_1)
    print(mg.numpix_2)
    print(mg.seg_01_strip, mg.seg_01_start, mg.seg_01_count)
    print(mg.seg_02_strip, mg.seg_02_start, mg.seg_02_count)


#------------------------------------------------------------------------------
#--- Main
#------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
