# -*- coding: utf-8 -*-

"""
# see also

#  markerfacecolor
#  linewidth or lw

"""


class LineStyle():
    """
    dispenses row by row a tuple of row style types to
    help make it easy to tell graph lines apart
    use instead of mathplot defaults
    use:
        ( this may be out of date see use in graph_smart_plug )
        import line_style

        self.line_style     = line_style.LineStyle()

        self.current_style  = self.lineStyle.get_next_style()  # ( line, color, marker, width )
        .....plot(  x, y, label= alabel, linestyle = self.current_style[0],   color     = self.current_style[1],
                                         marker    = self.current_style[2] ,  linewidth = self.current_style[3]  )
        or after the get_next_style you can access the instant values
        self.line_style.marker_style ........


        self.line_style.reset()      # for a new set
        !!consider changing to named tuple

        may be more styles....
        matplotlib.lines.Line2D — Matplotlib 3.1.1 documentation
        https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D.set_linestyle

        markers = {'.': 'point', ',': 'pixel', 'o': 'circle', 'v': 'triangle_down', '^': 'triangle_up', '<':
            'triangle_left', '>': 'triangle_right', '1': 'tri_down', '2': 'tri_up', '3': 'tri_left', '4': 'tri_right',
            '8': 'octagon', 's': 'square', 'p': 'pentagon', '*': 'star', 'h': 'hexagon1', 'H': 'hexagon2', '+': 'plus',
            'x': 'x', 'D': 'diamond', 'd': 'thin_diamond', '|': 'vline', '_': 'hline', 'P': 'plus_filled', 'X': 'x_filled', 0:
                'tickleft', 1: 'tickright', 2: 'tickup', 3: 'tickdown', 4: 'caretleft', 5: 'caretright', 6: 'caretup', 7: 'caretdown',
                8: 'caretleftbase', 9: 'caretrightbase', 10: 'caretupbase', 11: 'caretdownbase', 'None': 'nothing', None: 'nothing',
                ' ': 'nothing', '': 'nothing'}¶

    """
	
    # -----------------------------------------------
    def __init__(self ):

        """
        think we want lists to be relatively prime for longest cycle time
        """
        self.lines       = [  '-', '--', ':' ]  #   "-." "_" total of 4 ??
        self.line_ix     = 0
        self.max_line    = len( self.lines  )

        self.colors      = [ 'red', 'blue', 'cyan', 'green', 'black' ]     # want dark colors yellow and orange are light
        self.color_ix    = 0
        self.max_color   = len( self.colors  )

        self.markers     = [ 'o', 'x', '+', '*', 'h', 's', "d", "2" ]       # "1" ......23   "4"
        self.marker_ix   = 0
        self.max_marker  = len( self.markers  )

        self.widths      = [ 1, 2, 3, 4 ]       # "1" ......23   "4"
        self.max_width   = len( self.widths  )

        # setup, need get_next_style before use
        self.linestyle     = None
        self.colorstyle    = None
        self.markerstyle   = None
        self.widthstyle    = None

        #  *>url  https://stackoverflow.com/questions/8409095/matplotlib-set-markers-for-individual-points-on-a-line

        self.reset()
    # -----------------------------------------------
    def reset( self, ):
        """
        reset for reuse from beginning
        need to get next before valid
        """
        self.marker_ix   = -1
        self.color_ix    = -1
        self.line_ix     = -1
        self.width_ix    = -1

    # -----------------------------------------------
    def _getNextWidth_( self, ):
        """
        inside class use only,
        get next line style
        """
        self.width_ix  += 1
        if self.width_ix >= self.max_width:
            self.width_ix = 0
        self.widthstyle  = self.widths[ self.width_ix ]
        return self.widthstyle

    # -----------------------------------------------
    def _getNextLine_( self, ):
        """
        inside class use only,
        get next line style
        """
        self.line_ix  += 1
        if self.line_ix >= self.max_line:
            self.line_ix = 0
        self.linestyle      = self.lines[ self.line_ix ]
        return self.linestyle

    # -----------------------------------------------
    def _getNextColor_( self, ):
        """
        inside class use only,
        get next color style
        """
        self.color_ix  += 1
        if self.color_ix >= self.max_color:
            self.color_ix = 0
        self.colorstyle        = self.colors[ self.color_ix ]
        return self.colorstyle

    # -----------------------------------------------
    def _getNextMarker_( self, ):
        """
        inside class use only,
        get next marker style
        """
        self.marker_ix  += 1
        if self.marker_ix >= self.max_marker:
            self.marker_ix = 0
        self.markerstyle       = self.markers[ self.marker_ix ]
        return self.markerstyle

    # -----------------------------------------------
    def get_next_style( self,  ):
        """
        get the next tuple: ( line, color, marker )
        return tuple see below !! change to named tuple ??
        can use the returned or perhaps clear the instance var like   .markerstyle

        a_linestyle, a_colorstyle, a_markerstyle, a_widthstyle  = line_style.get_next_style()
        or
        line_style.get_next_style()
        a_linestyle   = line_style.linestyle
        a_color       = line_style.colorstyle
        a_widthstyle
        """
        return ( self._getNextLine_() , self._getNextColor_(), self._getNextMarker_(), self._getNextWidth_()  )

# =========================== put a test ===================



# ------------------------------------------------
if __name__ == '__main__':
    """
    run the application as an object
    """
    test   = LineStyle()
    for ix in range(0,20 ):
        print(test.get_next_style())




