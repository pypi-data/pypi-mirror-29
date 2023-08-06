import wx
from doc import Doc
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, GUIMode
from tools import tools

class MainFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, None, title='Barcode Editor', **kwargs)
        self.SetIcon(wx.Icon('../imgdata/barcode.ico', wx.BITMAP_TYPE_ICO))
        self.CreateStatusBar()
        self.toolbar = wx.ToolBar( self, wx.ID_ANY) 
        self.doc = None
        titledic = {}
        for i in tools:
            self.toolbar.AddTool(100+tools.index(i),'',wx.Bitmap(i.img)) 
            titledic[100+tools.index(i)] = i
        self.toolbar.Bind(wx.EVT_TOOL, lambda event: 
            titledic[event.GetId()]().start(self, self.doc))
        self.toolbar.Realize() 
        # Add the Canvas
        self.canvas = canvas = FloatCanvas.FloatCanvas(
            self, size = (500,500), BackgroundColor = "LIGHT GRAY")
        canvas.MaxScale=3 # sets the maximum zoom level
        self.BindEvents()

        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        bSizer1.Add(self.toolbar, 0, wx.ALL | wx.GROW, 0)
        bSizer1.Add(self.canvas, 1, wx.ALL | wx.GROW, 0 )
        self.SetSizerAndFit( bSizer1 )
        self.Layout()
        self.Show()
        self.moving = False
        
    def BindEvents(self):
        self.canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.OnLeftDown)
        self.canvas.Bind(FloatCanvas.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove)
        self.canvas.Bind(FloatCanvas.EVT_LEFT_UP, self.OnLeftUp)
        self.canvas.Bind(FloatCanvas.EVT_RIGHT_UP, self.OnRightDown)

    def OnLeftUp(self, event):
        self.moving = False

    def OnRightDown(self, event):
        cur = self.doc.pick(*(event.Coords))
        if not cur is None:self.doc.remove(cur)
        self.update()

    def OnLeftDClick(self, event):
        cur = self.doc.pick(*(event.Coords))
        if not cur is None:cur.show(self)

    def OnLeftDown(self, event):
        x,y = event.Coords
        cur = self.doc.pick(x, y)
        self.update()
        if cur is None:return
        self.dp = cur.getpos() - event.Coords*(1,-1)
        self.moving = True
        
    def SetMode(self, pan='switch'):
        if pan=='switch':
            pan = isinstance(self.canvas.GUIMode, GUIMode.GUIMouse)
        mode = (GUIMode.GUIMouse, GUIMode.GUIMove)[pan]()
        self.canvas.SetMode(mode)

    def update(self):
        if self.doc is None: return
        self.canvas.ClearAll(ResetBB=False)
        image = self.doc.img()
        width, height = image.size
        bmp = wx.Bitmap.FromBuffer(width, height, image.tobytes())
        img = FloatCanvas.ScaledBitmap( bmp, (0,0), Height=height, Position = 'tl')
        self.canvas.AddObject(img)

        
        if not self.doc.cur is None:
            rect = self.doc.cur.rect()
            self.canvas.AddRectangle(*(rect), LineColor='Blue', LineStyle='DotDash')
        self.canvas.BoundingBoxDirty = False
        self.canvas.Draw()
        #self.canvas.SetToNewScale(DrawFlag=True)
        #self.canvas.Zoom(1, (width/2, -height//2))



    def Binding(self, event):
        print("Writing a png file:")
        self.Canvas.SaveAsImage("junk.png")
        print("Writing a jpeg file:")
        self.Canvas.SaveAsImage("junk.jpg",wx.BITMAP_TYPE_JPEG)

        

    def OnMove(self, event):
        self.SetStatusText("%i, %i"%tuple(event.Coords))
        if not self.moving:return
        if self.doc.cur is None:return
        self.doc.cur.setpos(*(self.dp+event.Coords*(1,-1)))
        self.update()


if __name__ == "__main__":
    app = wx.App(False)
    mainFrame = MainFrame(None)
    mainFrame.Show()
    app.MainLoop()