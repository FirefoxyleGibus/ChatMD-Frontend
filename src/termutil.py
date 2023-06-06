from blessed import *
from blessed.keyboard import *

term = Terminal()

# shamelessly stolen from HastagGuigui/shellrhythm, by HastagGuigui himself

def print_at(x,y,test):
    print(term.move_xy(int(x), int(y)) + test)

def prng (beat = 0.0, seed = 0): return int(beat * 210413 + 2531041 * (seed+1.3)/3.4) % 2**32 #quick pseudorandomness don't mind me

def colorText(text = "", beat = 0.0):
	#Here, replace something like {cf XXXXXX} with the corresponding terminal color
	#Combinaisons to support: 
	# - cf RRGGBB		Foreground color
	# - cb RRGGBB		Background color
	# - b				Bold text
	# - i				Italic text
	# - u				Underline text
	# - n				Reverts text back to normal state
	# - r				Flips foreground and background
	# - k				Glitchifies text

	text = text.replace("\{", "￼ø").replace("\}", "ŧ￼").replace("{", "�{").replace("}", "}�") 
	#If you are using � or "￼" genuiunely, what the #### is wrong with you /gen
	data = text.split("�")
	renderedText = ""
	glitchifyNext = False
	for i in data:
		if i.startswith("{") and i.endswith("}"):
			ac = i.strip("{}")
			if ac.startswith("cf"):
				col = color_code_from_hex(ac.replace("cf ", "", 1))
				renderedText += term.color_rgb(col[0], col[1], col[2])
				continue
			if ac.startswith("cb"):
				col = color_code_from_hex(ac.replace("cb ", "", 1))
				renderedText += term.on_color_rgb(col[0], col[1], col[2])
				continue
			if ac == "b":
				renderedText += term.bold
				continue
			if ac == "i":
				renderedText += term.italic
				continue
			if ac == "u":
				renderedText += term.underline
				continue
			if ac == "n":
				renderedText += term.normal
				glitchifyNext = False
				continue
			if ac == "r":
				renderedText += term.reverse
				continue
			if ac == "k":
				glitchifyNext = True
				continue
			if glitchifyNext:
				#this big chunk will generate a random string with characters from 0x20 to 0x7e
				renderedText += "".join([chr(int(prng(beat, k))%(0x7e-0x20) + 0x20) for k in range(len(i.replace("￼ø", "{").replace("ŧ￼", "}")))])
			else:
				renderedText += i.replace("￼ø", "{").replace("ŧ￼", "}")
		else:
			if glitchifyNext:
				renderedText += "".join([chr(int(prng(beat, k))%(0x7e-0x20) + 0x20) for k in range(len(i.replace("￼ø", "{").replace("ŧ￼", "}")))])
			else:
				renderedText += i.replace("￼ø", "{").replace("ŧ￼", "}")
	return renderedText

def color_code_from_hex(hexcode:str) -> list:
	# hexcode is string built like "RRGGBB"
	output = [0,0,0]
	if len(hexcode) == 6: #No more, no less
		try:
			output = [int(hexcode[i:i+2], 16) for i in range(0, len(hexcode), 2)]
		except ValueError:
			pass
	return output

def hexcode_from_color_code(code:list) -> str:
	output = "000000"
	if len(code) == 3:
		output = hex((code[0] * 256**2) + (code[1] * 256) + code[2]).replace("0x", "")
	if len(output) < 6:
		output = "0"*(6-len(output)) + output
	return output

def textbox_logic(curText, cursorPos, val):
	if val.name == "KEY_BACKSPACE":
		if curText != "":
			curText = curText[:len(curText)-(cursorPos+1)] + curText[len(curText)-cursorPos:]
	elif val.name == "KEY_LEFT":
		cursorPos += 1
		if cursorPos > len(curText):
			cursorPos = len(curText)
	elif val.name == "KEY_RIGHT":
		cursorPos -= 1
		if cursorPos < 0:
			cursorPos = 0
	else:
		if val.name == None:
			if cursorPos == 0:
				curText += str(val)
			else:
				curText = curText[:len(curText)-cursorPos] + str(val) + curText[len(curText)-cursorPos:]
	
	return curText, cursorPos