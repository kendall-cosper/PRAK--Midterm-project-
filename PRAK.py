import RPi.GPIO as GPIO 
GPIO.setwarnings(False)
from RPLCD.gpio import CharLCD
import board
import digitalio
from gpiozero import Button
from signal import pause
import time
from datetime import datetime
import yagmail

# LCD SETUP
lcd_columns = 16
lcd_rows = 2
lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    pin_rs=22,
    pin_e=17,
    pins_data=[25, 24, 23, 18]
)

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
BUTTON_PIN = 13

# TXT FILE SETUP
with open('/home/pi/Desktop/PRAK/pattern.txt', 'r') as f:
    lines = [line.strip() for line in f if line.strip()]
current_index = 0
def show_line():
    lcd.clear()
    lcd.write_string(lines[current_index][:16])

# EMAIL MESSAGE SETUP
last_row = None
now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
yag_mail = yagmail.SMTP(user='YOUR EMAIL', password="*******", host='smtp.gmail.com')
  
To= "USER'S EMAIL" 
Subject = f'knit log {now}!'
 

# PRIMARY FUNCTION!
def button_pressed(channel):
    global last_row

    now = time.time()

    if last_row is not None:
        time_elapsed = now - last_row
        message = f"you finished a row! congratulations! this row took you {time_elapsed:.2f} seconds to complete. keep knitting!"
        print(message)
        yag_mail.send(to=To, subject=Subject, contents=message)

    last_row = now
    
    global current_index
    current_index += 1
    if current_index >= len(lines):
        current_index = 0
    show_line()

# INITIAL DISPLAY 
if lines:
    show_line()

GPIO.add_event_detect(
    BUTTON_PIN,
    GPIO.FALLING,
    callback=button_pressed,
    bouncetime=300
)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    lcd.clear()
    GPIO.cleanup()

