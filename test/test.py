###############################################################################
### Test Programm                                                           ###
###############################################################################
import time # type: ignore

pix_array = [[ 1, 1, 1, 1],
             [ 0, 2, 4, 8]]



# #############################################################################
# ### Main                                                                  ###
# #############################################################################

def main():
    for i in range(len(pix_array[0])):
        print(pix_array[1][i])


    try:
        print("Start")
        for i in range(10):
            time.sleep(1)
            print("Schleife")
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    finally:
        print("Exiting the program")
 



# #############################################################################

if __name__ == "__main__":
    
    print("___ Start of Programm ___ !!!")
    
    main()      # Start Main $$$

# Normal sollte das Programm hier nie ankommen !
print("___ End of Programm ___ !!!")

# #############################################################################


