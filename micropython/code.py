import board
import busio as io
import adafruit_ssd1306
import keypad
import framebuf

i2c = io.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

keymap = [ '1', '2', '3', '+', '4', '5', '6', '-', '7', '8', '9', '*', 'c', '0', '=', '/' ]

km = keypad.KeyMatrix(row_pins = (board.D10, board.D9, board.D8, board.D7), column_pins = (board.D0, board.D1, board.D2, board.D3))

pos = 0
pos_width = 12 
arg1 = 0
arg2 = 0
inputBuf = ''
inputBufMaxLen = 9
operation = '+'
line2_textSize = 2
line3_textSize = 2
line2_ypos = 16
line3_ypos = 40

def show_cursor_and_header(title):
    oled.text(title, 20, 0, True, size = 1)
    oled.line(0, 60, 128, 60, 0)
    oled.line(pos * pos_width, 60, pos * pos_width + pos_width, 60, 1)
    oled.show()

print("Starting event loop:")

# Menu:
#while True:
#    break

# Classic Mode:
show_cursor_and_header("Calculator Mode")
while True:
    event = km.events.get()
    if event:
        if event.released:
            print(keymap[event.key_number])
            print("len(inputBuf): " + str(len(inputBuf)))
            print("len(arg1): " + str(len(str(arg1))))
            print("len(arg2): " + str(len(str(arg2))))
            key = keymap[event.key_number]
            if ((key == '+' or key == '-' or key == '*' or key == '/') and 
                    len(inputBuf) <= (inputBufMaxLen - 2) and
                    (len(str(arg1)) + len(str(arg2)) + 2) <= (inputBufMaxLen - 2) and
                    (len(str(arg2)) + len(inputBuf) + 1) <= (inputBufMaxLen - 2) and
                    (len(str(arg1)) + len(inputBuf) + 1) <= (inputBufMaxLen - 2)):
                if (inputBuf != ""):
                    operation = key
                    print("Ok, doing a '" + operation + "' operation on " + inputBuf)
                    try:
                        arg1 = int(float(inputBuf))
                        inputBuf = ''
                        oled.text(operation, pos * pos_width, line3_ypos, True, size = line3_textSize)
                    except:
                        pass
                    pos = pos + 1
            elif (key == '='):
                try:
                    print("Calculating... (" + inputBuf + ")")
                    arg2 = int(float(inputBuf))
                    if (arg1 == 123 and arg2 == 987):
                        print("Secret code entered.")
                        break
                    print("Now performing: '" + str(arg1) + " " + operation + " " + str(arg2) + "'")
                    inputBuf = ''
                    answer = 0
                    if (operation == '+'):
                        answer = arg1 + arg2
                    if (operation == '-'):
                        answer = arg1 - arg2
                    if (operation == '*'):
                        answer = arg1 * arg2
                    if (operation == '/'):
                        answer = arg1 / arg2
                    print('Answer: ' + str(answer))
                    problem = str(arg1) + str(operation) + str(arg2) + "="
                    oled.fill_rect(0, 16, 128, 64, 0)
                    oled.text(problem, 0, line2_ypos, True, size = line2_textSize)
                    oled.text(str(answer), 0, line3_ypos, True, size = line3_textSize)
                except ValueError:
                    print("VE")
                    pass
                pos = 0
                inputBuf = ''
                arg1 = 0
                arg2 = 0
            elif (key == 'c'):
                pos = 0
                inputBuf = ''
                arg1 = 0
                arg2 = 0
                oled.fill(0)
            elif (len(inputBuf) <= inputBufMaxLen and
                    (len(str(arg1)) + len(str(arg2)) + 2) <= inputBufMaxLen and
                    (len(str(arg2)) + len(inputBuf) + 1) <= inputBufMaxLen and
                    (len(str(arg1)) + len(inputBuf) + 1) <= inputBufMaxLen):
                inputBuf = inputBuf + key
                if pos == 0:
                    oled.fill_rect(0, 16, 128, 64, 0)
                oled.text(key, pos * pos_width, line3_ypos, True, size = line3_textSize)
                pos = pos + 1
            #if (pos > inputBufMaxLen):
            #    pos = 0
            #    # oled.fill_rect(0, 16, 128, 64, 0)
            #    oled.fill(0)
            show_cursor_and_header('Calculator Mode')
            oled.show()

# Bonus mode:
pos = 0
inputBuf = ''
arg1 = 0
arg2 = 0
oled.fill(0)

show_cursor_and_header('Time Mode')
while True:
    event = km.events.get()
    if event:
        if event.released:
            key = keymap[event.key_number]
            print(key)
            #if (key == '+' or key == '-')
            oled.text(key, pos * pos_width, line3_ypos, True, size = line3_textSize)
            pos = pos + 1
            show_cursor_and_header('Time Mode')
 
