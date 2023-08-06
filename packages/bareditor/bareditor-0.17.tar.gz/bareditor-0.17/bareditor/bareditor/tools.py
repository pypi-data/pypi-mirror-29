from config import ParaDialog
from doc import Doc, parsedoc
from rects import *
import wx, os

class Tool:
	title = 'title'
	para = None
	view = None

	def preview(self, parent, doc, para=None):
		self.run(parent, doc, para)
		parent.update()

	def show(self, parent, doc):
		self.dialog = ParaDialog(parent, self.title)
		self.dialog.init_view(self.view, self.para, True)
		self.dialog.set_handle(lambda x:self.preview(parent,  doc, self.para))

		if self.dialog.ShowModal() == wx.ID_OK:
			self.run(parent, doc, self.para)
			parent.update()
		self.dialog.Destroy()

	def start(self, parent, doc):
		if self.para is None:
			self.run(parent, doc, None)
			parent.update()
		else:
			self.show(parent, doc)

class NewTool(Tool):
	para = {'w':300, 'h':512}
	view = [(int, (100,1000), 0, 'width', 'w', 'pix'),
			(int, (100,1000), 0, 'height', 'h', 'pix')]
	img = '../imgdata/new.png'
	title = 'New'

	def run(self, parent, doc, para):
		parent.doc = Doc()
		parent.doc.para = {'w':para['w'], 'h':para['h']}
		parent.canvas.Zoom(1/parent.canvas.Scale, 
			(para['w']//2, -para['h']//2))
		#parent.canvas.SetFocus()

class SaveTool(Tool):
	img = '../imgdata/save.png'
	title = 'Save'

	def run(self, parent, doc, para):
		dlg = wx.FileDialog(
			parent, message="Choose a file",
			defaultFile="",
			wildcard='Bar File (*.bar)|*.bar',
			style=wx.FD_SAVE | wx.FD_PREVIEW
			)

		if dlg.ShowModal() == wx.ID_OK:
			# This returns a Python list of files that were selected.
			f = open(dlg.GetPath(), 'w')
			f.write(str(doc))
			f.close()
		dlg.Destroy()

class OpenTool(Tool):
	img = '../imgdata/open.png'
	title = 'Open'

	def run(self, parent, doc, para):
		dlg = wx.FileDialog(
			parent, message="Choose a file",
			defaultFile="",
			wildcard='Bar File (*.bar)|*.bar',
			style=wx.FD_OPEN | 
				wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
			)

		if dlg.ShowModal() == wx.ID_OK:
			# This returns a Python list of files that were selected.
			f = open(dlg.GetPath())
			cont = '\n'.join(f.readlines())
			parent.doc = parsedoc(cont)
			center = parent.doc.para['w']//2, -parent.doc.para['h']//2
			parent.canvas.Zoom(1/parent.canvas.Scale, center)
			f.close()
		dlg.Destroy()

class SetTool(Tool):
	para = {'w':256, 'h':256}
	view = [(int, (100,1000), 0, 'width', 'w', 'pix'),
			(int, (100,1000), 0, 'height', 'h', 'pix')]
	img = '../imgdata/set.png'
	title = 'Set'
	def run(self, parent, doc, para):
		doc.para = {'w':para['w'], 'h':para['h']}

class AddText(Tool):
	img = '../imgdata/text.png'
	title = 'Text'

	def run(self, parent, doc, para):
		doc.add(TextObj())

class AddBar(Tool):
	img = '../imgdata/barcode.png'
	title = 'Barcode'

	def run(self, parent, doc, para):
		doc.add(BarObj())

class ZoomIn(Tool):
	img = '../imgdata/zoomin.png'
	title = 'Zoom In'

	def run(self, parent, doc, para):
		parent.canvas.Zoom(1/parent.canvas.Scale, 
			(doc.para['w']//2, -doc.para['h']//2))
		

class ZoomOut(Tool):
	img = '../imgdata/zoomout.png'
	title = 'Zoom Out'

	def run(self, parent, doc, para):
		parent.SetMode()

class FullExtent(Tool):
	img = '../imgdata/full.png'
	title = 'Full Extent'

	def run(self, parent, doc, para):
		parent.canvas.BoundingBoxDirty = True
		parent.canvas.ZoomToBB()
	
class SaveImg(Tool):
	img = '../imgdata/picture.png'
	title = 'Save Image'

	def run(self, parent, doc, para):
		dlg = wx.FileDialog(
			parent, message="Choose a file",
			defaultFile="",
			wildcard='PNG File (*.png)|*.png',
			style=wx.FD_SAVE | wx.FD_PREVIEW
			)

		if dlg.ShowModal() == wx.ID_OK:
			# This returns a Python list of files that were selected.
			doc.img(True).save(dlg.GetPath(), 'png')
		dlg.Destroy()

class Printer(Tool):
	img = '../imgdata/printer.png'
	title = 'Full Extent'

	def run(self, parent, doc, para):
		print('No Printer')

tools = [NewTool, SaveTool, OpenTool, SetTool, AddText, AddBar, ZoomIn, ZoomOut, FullExtent, SaveImg, Printer]