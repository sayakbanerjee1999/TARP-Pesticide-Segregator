import RPi.GPIO as GPIO
import time
from time import sleep
 
# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 17
LCD_D5 = 4
LCD_D6 = 3
LCD_D7 = 2
LCD_CON = 27
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
 
def main():
	 
	# Initialise display
	lcd_init()
	print("Game on");
	run_once = 0
	while run_once==0:
		print("LCD");
		# Send some test
		lcd_string("Pestiside",LCD_LINE_1)
		lcd_string("Given",LCD_LINE_2)
    
		sleep(5)
		run_once = 1
      
def lcd_init():
	lcd_display(0x28,LCD_CMD) # Selecting 4 - bit mode with two rows
	lcd_display(0x0C,LCD_CMD) # Display On,Cursor Off, Blink Off
	lcd_display(0x01,LCD_CMD) # Clear display

  	sleep(E_DELAY)
 
def lcd_display(bits, mode):
  	# Send byte to data pins
  	# bits = data
  	# mode = True  for character
  	#        False for command
 
  	GPIO.output(LCD_RS, mode) # RS
 
  	# High bits
  	GPIO.output(LCD_D4, False)
  	GPIO.output(LCD_D5, False)
  	GPIO.output(LCD_D6, False)
  	GPIO.output(LCD_D7, False)
  	if bits&0x10==0x10:
    		GPIO.output(LCD_D4, True)
  	if bits&0x20==0x20:
    		GPIO.output(LCD_D5, True)
  	if bits&0x40==0x40:
    		GPIO.output(LCD_D6, True)
  	if bits&0x80==0x80:
    		GPIO.output(LCD_D7, True)
 
  	# Toggle 'Enable' pin
  		lcd_toggle_enable()
 
  	# Low bits
  		GPIO.output(LCD_D4, False)
  		GPIO.output(LCD_D5, False)
  		GPIO.output(LCD_D6, False)
  		GPIO.output(LCD_D7, False)
  	if bits&0x01==0x01:
    		GPIO.output(LCD_D4, True)
  	if bits&0x02==0x02:
    		GPIO.output(LCD_D5, True)
  	if bits&0x04==0x04:
    		GPIO.output(LCD_D6, True)
  	if bits&0x08==0x08:
    		GPIO.output(LCD_D7, True)
 
  	# Toggle 'Enable' pin
  	lcd_toggle_enable()
 
def lcd_toggle_enable():
	# Toggle enable
	time.sleep(E_DELAY)
	GPIO.output(LCD_E, True)
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, False)
	time.sleep(E_DELAY)
 
def lcd_string(message,line):
	# Send string to display
 
	message = message.ljust(LCD_WIDTH," ")
 
	lcd_display(line, LCD_CMD)
 
	for i in range(LCD_WIDTH):
		lcd_display(ord(message[i]),LCD_CHR)
 

# Pins for Motor Driver Inputs 
Motor1A = 24
Motor1B = 23
Motor1E = 25
 
def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)				# GPIO Numbering
	GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
	GPIO.setup(Motor1B,GPIO.OUT)
	GPIO.setup(Motor1E,GPIO.OUT)
	GPIO.setup(LCD_E, GPIO.OUT)  # E
	GPIO.setup(LCD_RS, GPIO.OUT) # RS
	GPIO.setup(LCD_D4, GPIO.OUT) # DB4
	GPIO.setup(LCD_D5, GPIO.OUT) # DB5
	GPIO.setup(LCD_D6, GPIO.OUT) # DB6
	GPIO.setup(LCD_D7, GPIO.OUT) # DB7
	GPIO.setup(LCD_CON, GPIO.OUT)
 
def loop():
	# Going forwards
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)
 
	sleep(5)
 	# Going backwards
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor1B,GPIO.HIGH)
	GPIO.output(Motor1E,GPIO.HIGH)
 
	sleep(5)
	# Stop
	GPIO.output(Motor1E,GPIO.LOW)

def destroy():	
	GPIO.cleanup()

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		main()
    		loop()
  	except KeyboardInterrupt:
		destroy()
	finally:
    		lcd_display(0x01, LCD_CMD)
    		GPIO.cleanup()
