from PIL import Image, ImageFont, ImageDraw
from config import ParaDialog
import barcode, os, wx
import numpy as np


bufferimg = Image.new("RGB", (1,1), "white")
f = open('font.txt')
fontlist = [i.replace('\n', '') for i in f.readlines()]
f.close()

class Rect:
	def __init__(self):
		self.para = {'x':0, 'y':0}

	def setpos(self, x, y):
		self.para['x'], self.para['y'] = x, y

	def getpos(self):
		return self.para['x'], self.para['y']

	def getrect(self):pass

	def show(self, parent):
		self.dialog = ParaDialog(parent, self.title)
		self.dialog.init_view(self.view, self.para, True)
		self.dialog.set_handle(lambda x:parent.update())
		if self.dialog.ShowModal() == wx.ID_OK:
			parent.update()
		self.dialog.Destroy()

class TextObj(Rect):
	title = 'Text'
	def __init__(self, para=None):
		if para is None: para = {'x':0, 'y':0, 'txt':'TEXT', 'size':36, 
			'font':fontlist[0]}
		self.para = para
		self.view = [(str, 'text', 'txt', ''),
					 (int, (1,1024), 0, 'X', 'x', 'pix'),
					 (int, (1,1024), 0, 'Y', 'y', 'pix'),
					 (int, (1,200), 0, 'size', 'size', ''),
					 (list, fontlist, str, 'font', 'font', '')
					 ]
	def rect(self):
		p = self.para
		truetype=ImageFont.truetype(p['font'], p['size'])
		draw = ImageDraw.Draw(bufferimg)
		size = draw.multiline_textsize(p['txt'], font=truetype)
		del draw
		return (p['x'], -p['y']-size[1]-2), size

	def draw(self, image, para):
		draw = ImageDraw.Draw(image)
		truetype=ImageFont.truetype(self.para['font'], self.para['size'])
		draw.text((para['x'], para['y']), para['txt'], (0,0,0), font=truetype)
		del draw

	def __str__(self):
		return 'TXT>'+str(self.para)

def draw_bar(img,code, font,x,y,w, h,dh, dtxt, fs):
    bar=barcode.upc.UniversalProductCodeA(code.replace(' ',''),make_ean=True).to_ascii()
    bar=bar.replace(' ','0').replace('|','1')
    d = ImageDraw.Draw(img)
    index = [int(94.5/(w-1)*i) for i in range(w)]
    for i in range(len(index)):
        if bar[index[i]]=='0':continue
        j = index[i]
        if j<11 or (j>44 and j<50) or j>84:
            d.line([x+i,y,x+i,y+h+dh], 'black')
        else: d.line([x+i,y,x+i,y+h], 'black')
    truetype=ImageFont.truetype(font, fs)
    fw = d.multiline_textsize(text=code,font=truetype)[0]
    d.text((x+(w-fw)/2,y+h+dh+dtxt),code,(0,0,0),font=truetype)
    del d

class BarObj(Rect):
	title = 'Barcode'
	def __init__(self, para=None):
		# code,x,y,w, h,dh, dtxt, fs
		if para is None: para = {'x':0, 'y':0, 'code':'8    89532   41399    7', 
			'w':200, 'h':50, 'dh':10, 'mar':0, 'size':24, 'font':fontlist[0]}
		self.para = para
		self.view = [(str, 'code', 'code', ''),
					 (list, fontlist, str, 'font', 'font', ''),
					 (int, (1,1024), 0, 'X', 'x', 'pix'),
					 (int, (1,1024), 0, 'Y', 'y', 'pix'),
					 (int, (1,1024), 0, 'width', 'w', 'pix'),
					 (int, (1,1024), 0, 'height', 'h', 'pix'),
					 (int, (1,1024), 0, 'dh', 'dh', 'pix'),
					 (int, (-100,1024), 0, 'margin', 'mar', 'pix'),
					 (int, (1,200), 0, 'size', 'size', '')]

	def rect(self):
		p = self.para
		return (p['x']-2, -p['y']-p['h']-p['dh']-2), (p['w']+4, p['h']+p['dh']+4)

	def draw(self, image, para):
		draw_bar(image, para['code'], para['font'], para['x'], para['y'], para['w'], 
			para['h'], para['dh'], para['mar'], para['size'])

	def __str__(self):
		return 'BAR>'+str(self.para)

def parserect(cont):
	title, para = cont.split('>')
	if title == 'TXT':
		return TextObj(eval(para))
	if title == 'BAR':
		return BarObj(eval(para))


if __name__ == '__main__':
	txt = TextObj()
	txt.size()