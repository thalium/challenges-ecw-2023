import requests
import shutil

#########################################
# pip install requests
#########################################

BUTTON_RIGHT_ARROW  = 0x001
BUTTON_LEFT_ARROW   = 0x002
BUTTON_UP_ARROW     = 0x004
BUTTON_DOWN_ARROW   = 0x008
BUTTON_A            = 0x010
BUTTON_B            = 0x020
BUTTON_SELECT       = 0x040
BUTTON_START        = 0x080
BUTTON_RESET        = 0x100

PORT = 1337         # <---------- CHANGE ME
HOST = "localhost"  # <---------- CHANGE ME

def press_button(button: int):
    """
    Send a button press to the remote emulator
    """

    requests.get(f"http://{HOST}:{PORT}/setState?state={button}")
    requests.get(f"http://{HOST}:{PORT}/setState?state=0")

def save_frame(path: str):
    """
    Save the current frame to a PNG image
    """
    response = requests.get(f"http://{HOST}:{PORT}/render", stream=True)
    response.raw.decode_content = True

    with open(path, "wb") as f:
        shutil.copyfileobj(response.raw, f)

    print(f"[*] Frame saved at '{path}'")

def main():
    # PUT YOUR CODE HERE
    #
    # ...
    #
    # press_button(BUTTON_A)
    # press_button(BUTTON_START)
    #
    # ...
    #
    # PUT YOUR CODE HERE
    pass

if __name__ == "__main__":
    main()