from PIL import Image, ImageFont, ImageDraw

class Doc:
	def __init__(self, para=None):
		self.rects = []
		if para is None: para = {'w':300, 'h':512}
		self.para =  para
		self.cur = None

	def save(self):pass

	def add(self, obj, center=True):
		if center: 
			obj.setpos(self.para['w']//2, self.para['h']//2)
		self.rects.append(obj)

	def remove(self, obj):
		if self.cur is obj: self.cur = None
		del self.rects[self.rects.index(obj)]

	def img(self, thre = False):
		size = (self.para['w'], self.para['h'])
		image = Image.new("RGB", size, "white")
		for i in self.rects:
			i.draw(image, i.para)
		draw = ImageDraw.Draw(image)
		if thre: image = image.point(lambda p: p > 128 and 255)
		return image

	def pick(self, x, y):
		for r in self.rects:
			p1, p2 = r.rect()
			if x<p1[0] or x>p1[0]+p2[0]: continue
			if y<p1[1] or y>p1[1]+p2[1]: continue
			self.cur = r
			return self.cur
		self.cur = None

	def __str__(self):
		ls = []
		ls.append(str(self.para))
		for i in self.rects:
			ls.append(str(i))
		return '\n'.join(ls)

def parsedoc(cont):
	from rects import parserect
	lines = cont.split('\n')
	doc = Doc(eval(lines[0]))
	for i in lines[1:]:
		if '>' in i: doc.add(parserect(i), False)
	return doc

if __name__ == '__main__':
	doc = Doc()
	from rects import *
	doc.add(TextObj())
	ss = str(doc)
	print(ss)
	print('========')
	doc = parsedoc(ss)
	print(doc)