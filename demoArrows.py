# File: canvasarrow.py
#    http://infohost.nmt.edu/tcc/help/pubs/tkinter//canvas.html

from tkinter import *
from tkinter import ttk
from demopanels import MsgPanel, SeeDismissPanel

class CanvasArrowheadDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='canvasarrowheaddemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Canvas Arrowhead Editor Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self, 
                     ["This widget allows you to experiment with different ",
                      "widths and arrowhead shapes for lines in canvases.  ",
                      "To change the line width or the shape of the arrowhead, ",
                      "drag any of the three boxes attached to the oversized ",
                      "arrow.  The arrows on the right give examples at normal ",
                      "scale.  The text at the bottom shows the configuration ",
                      "options as you'd enter them for a canvas line item."])
            
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = Frame(self)
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)

        self.canvas = Canvas(width=500, height=350, relief=SUNKEN,
                             borderwidth=2)
        self.canvas.pack(in_=demoPanel, expand=Y, fill=BOTH)
        
        self._define_arrow()    # setup arrow dimensions and appearance
        self._arrow_setup(None) # draw the arrow and descriptions
        self._add_bindings()    # bind the reshape rectangles

    def _define_arrow(self):
        # arrow feature definitions
        # (a,b,c) define the arrowhead's shape
        # 'motion' - method to use during drag
        #            of the active reshape rectangle
        # 'x1' - used to position descriptive text
        # 'x2' - used to position arrowhead
        # 'y' - used to position arrowhead
        # 'width' - width of arrowhead shaft
        # 'box', 'active' - reshape rectangle styles
        # value are used/re-defined during arrow edits
        d = {'a': 8,    
             'b': 10,
             'c': 3,
             'motion': None,
             'x1': 40,
             'x2': 350,
             'y': 150,
             'width': 2,
             'box': {'fill': ''},
             'active': {'fill': 'red'}}
        
        self.canvas.arrowInfo = d

    # ================================================================================
    # Canvas bindings
    # ================================================================================
    def _add_bindings(self):
        # apply reshape rectangle fill colours on mouse enter/leave
        self.canvas.tag_bind('box','<Enter>', self._box_enter)
        self.canvas.tag_bind('box', '<Leave>', self._box_leave)

        # ignore reshape rectangle enter/leave while rect is dragged
        self.canvas.tag_bind('box', '<B1-Enter>', ' ')  
        self.canvas.tag_bind('box', '<B1-Leave>', ' ')  
        
        # capture selection of reshaping rectangles
        self.canvas.tag_bind('vertex', '<1>', self._set_motion)
        self.canvas.tag_bind('tip', '<1>', self._set_motion)
        self.canvas.tag_bind('shaft', '<1>', self._set_motion)
        
        # handle reshape rectangle dragging
        self.canvas.bind('<B1-Motion>', lambda evt: self.canvas.arrowInfo['motion'](evt))
        self.canvas.bind('<Button1-ButtonRelease>', self._arrow_setup)

    # ================================================================================
    # Bound methods - handle the arrow reshaping edits
    # ================================================================================
    def _set_motion(self, evt):
        tags = self.canvas.gettags('current')
        if 'box' not in tags:
            return
        
        # use Python's ability to reference a function through a variable to 
        # assign the appropriate motion method to the arrowInfo 'motion'
        # dictionary key; the assigned method will be called when 
        # <B1-Motion> is detected
        for t in tags:
            if t == 'vertex':
                self.canvas.arrowInfo['motion'] = self._move_vertex
            elif t == 'tip':
                self.canvas.arrowInfo['motion'] = self._move_tip
            elif t == 'shaft':
                self.canvas.arrowInfo['motion'] = self._move_shaft
                                                
    def _move_vertex(self, evt):
        # handle drag of the vertex reshape rectangle
        # limited to horizontal motion
        v = self.canvas.arrowInfo
        
        newA = (v['x2'] + 5 - round(self.canvas.canvasx(evt.x)))//10
                
        if newA < 0: newA = 0
        if newA > 25: newA = 25
        
        if newA != v['a']:
            self.canvas.move('vertex', 10*(v['a']-newA), 0)
            v['a'] = newA    
              
        
    def _move_tip(self, evt):
        # handle drag of the tip reshape rectangle
        # the tip can be dragged horizontally and vertically
        v = self.canvas.arrowInfo
        
        newB = (v['x2'] + 5 - round(self.canvas.canvasx(evt.x)))//10
        if newB < 0: newB = 0
        if newB > 25: newB = 25
        
        newC = (v['y'] + 5 - round(self.canvas.canvasy(evt.y)) - 5 * v['width'])//10
        if newC < 0: newC = 0
        if newC > 20: newC = 20

        if newB != v['b'] or newC != v['c']:
            self.canvas.move('tip',
                             10*(v['b']-newB),
                             10*(v['c']-newC))
            v['b'] = newB
            v['c'] = newC    
        
    def _move_shaft(self, evt):
        # handle drag of shaft reshape rectangle
        # limited to vertical motion
        v = self.canvas.arrowInfo
        
        newWidth = (v['y'] + 2 - round(self.canvas.canvasy(evt.y)))//5
        if newWidth < 0: newWidth = 0
        if newWidth > 20: newWidth = 20
        
        if newWidth != v['width']:
            self.canvas.move('shaft', 0, 5*(v['width'] - newWidth))
            v['width'] = newWidth
        
    def _box_enter(self, evt):
        # set fill colour to 'active' style
        self.canvas.itemconfigure('current', self.canvas.arrowInfo['active'])
        
    def _box_leave(self, evt):
        # set fill colour to 'normal' style
        self.canvas.itemconfigure('current', self.canvas.arrowInfo['box'])
        
    def _arrow_setup(self, evt):
        # this method is called when the canvas is created and
        # whenever the arrow is edited; all objects are deleted
        # and redrawn with each edit
        
        # assign canvas and arrowInfo to temp variables for
        # easier reading
        c = self.canvas
        v = self.canvas.arrowInfo
                
        tags = c.gettags('current') # save existing tags, if any      
        c.delete(ALL)      # remove all objects        
                
        # Create the arrow shaft and head
        c.create_line(v['x1'], v['y'], v['x2'], v['y'],
                      fill='SkyBlue1',
                      arrow=LAST, width=10*v['width'],
                      arrowshape=(10*v['a'], 10*v['b'], 10*v['c']))

        # draw black outline around arrowhead
        xtip = v['x2'] - 10*v['b']
        deltaY = 10*v['c'] + 5*v['width']
        c.create_line(v['x2'], v['y'], xtip, v['y']+deltaY,
                      v['x2'] - 10*v['a'], v['y'], xtip, v['y']-deltaY,
                      v['x2'], v['y'], width=2, capstyle=ROUND,
                      joinstyle=ROUND)
        
        # create boxes for reshaping the arrow
        c.create_rectangle(v['x2']-10*v['a']-5, v['y']-5,
                           v['x2']-10*v['a']+5, v['y']+5,
                           outline='black', width=1,
                           tags=('vertex', 'box'))
        
        c.create_rectangle(xtip-5, v['y']-deltaY-5,
                           xtip+5, v['y']-deltaY+5,
                           outline='black', width=1,
                           tags=('tip', 'box'))

        c.create_rectangle(v['x1']-5, v['y']-5 * v['width']-5,
                           v['x1']+5, v['y']-5 * v['width']+5,
                           outline='black', width=1,
                           tags=('shaft', 'box'))

        # if a reshape box is selected, set it to 'active' style
        for t in tags:
            if t in ('vertex', 'tip', 'shaft'):
                c.itemconfigure('current', v['active'])
                
        # create dividing line on the right
        c.create_line(v['x2']+50, 0, v['x2']+50, 1000, width=2)

        # create 3 arrows, normal size, with same parameters
        start = v['x2']+100
        arrowShape = (v['a'], v['b'], v['c'])
        c.create_line(start, v['y']-125, start, v['y']-75,
                      width=v['width'], arrow=BOTH,
                      arrowshape=arrowShape)
        
        c.create_line(start-25, v['y'], start+25, v['y'],
                      width=v['width'], arrow=BOTH,
                      arrowshape=arrowShape)

        c.create_line(start-25, v['y']+75, start+25, v['y']+125,
                      width=v['width'], arrow=BOTH,
                      arrowshape=arrowShape)      
        
        # create small descriptive arrows with text
        arrowShape = (5,5,2)    
        
        # half height of arrow head  
        # (changes when 'tip' box is dragged)
        start = v['x2'] + 10
        c.create_line(start, v['y']-5*v['width'], start, v['y']-deltaY,
                      arrow=BOTH, arrowshape=arrowShape)
        c.create_text(v['x2']+15, v['y']-deltaY+5*v['c'],
                      text=v['c'], anchor=W)
        
        # width of shaft (changes when 'shaft' box is dragged)
        start = v['x1'] - 10
        c.create_line(start, v['y']-5*v['width'], start, v['y']+5*v['width'],
                      arrow=BOTH, arrowshape=arrowShape)
        c.create_text(v['x1']-15, v['y'], text=v['width'], anchor=E)

        # centre width of arrowhead (changes when 'vertex' box is dragged)
        start = v['y'] + 5 * v['width'] + 10 * v['c'] + 10
        c.create_line(v['x2']-10*v['a'], start, v['x2'], start,
                      arrow=BOTH, arrowshape=arrowShape)
        c.create_text(v['x2']-5*v['a'], start+5, text=v['a'], anchor=N)

        # full width of arrowhead (changes when 'tip' box is dragged)
        start = start + 25
        c.create_line(v['x2']-10*v['b'], start, v['x2'], start,
                      arrow=BOTH, arrowshape=arrowShape)
        c.create_text(v['x2']-5*v['b'], start+5, text=v['b'], anchor=N)

        # create text describing current values of arrowInfo keys: a, b, c, width
        c.create_text(v['x1'], 310, text='width: {}'.format(v['width']),
                      anchor=W, font=('Helv', 18))
        c.create_text(v['x1'], 330, 
                      text='arrowshape: ({}, {}, {})'.format(v['a'],v['b'],v['c']),
                      anchor=W, font=('Helv', 18))
        
if __name__ == '__main__':
    CanvasArrowheadDemo().mainloop()