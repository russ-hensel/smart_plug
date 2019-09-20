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
    """
    # -----------------------------------------------
    def __init__(self ):

        """
        think we want lists to be relatively prime for longest cycle time
        """
        self.lines       = [  '-', '--', ':' ]  #   "-." "_" totl of 4 ??
        self.line_ix     = 0
        self.max_line    = len( self.lines  )

        self.colors      = [ 'red', 'blue', 'cyan', 'green', 'black' ]   # want dark colors yellow and oarnge are light
        self.color_ix    = 0
        self.max_color   = len( self.colors  )

        self.markers     = [ 'o', 'x', '+', '*', 'h', 's', "d", "2" ]       # "1" ......23   "4"
        self.marker_ix   = 0
        self.max_marker  = len( self.markers  )

        self.widths      = [ 1, 2, 3, 4 ]       # "1" ......23   "4"
        self.max_width   = len( self.widths  )

        # setup, need get_next_style befor use
        self.line_style     = None
        self.color_style    = None
        self.marker_style   = None
        self.width_style    = None

        #  *>url  https://stackoverflow.com/questions/8409095/matplotlib-set-markers-for-individual-points-on-a-line

        self.reset()
    # -----------------------------------------------
    def reset( self, ):
        """
        reset for reuse from beginning
        need to get next befor valid
        """
        self.marker_ix   = -1
        self.color_ix    = -1
        self.line_ix     = -1
        self.width_ix    = -1

    # -----------------------------------------------
    def _getNextWidth_( self, ):
        """
        inside class use only,
        get next line sytle
        """

        self.width_ix  += 1
        if self.width_ix >= self.max_width:
            self.width_ix = 0
        self.width_style  = self.widths[ self.width_ix ]
        return self.width_style

    # -----------------------------------------------
    def _getNextLine_( self, ):
        """
        inside class use only,
        get next line sytle
        """
        self.line_ix  += 1
        if self.line_ix >= self.max_line:
            self.line_ix = 0
        self.line_style      = self.lines[ self.line_ix ]
        return self.line_style

    # -----------------------------------------------
    def _getNextColor_( self, ):
        """
        inside class use only,
        get next color sytle
        """

        self.color_ix  += 1
        if self.color_ix >= self.max_color:
            self.color_ix = 0
        self.color_style        = self.colors[ self.color_ix ]
        return self.color_style

    # -----------------------------------------------
    def _getNextMarker_( self, ):
        """
        inside class use only,
        get next marker sytle
        """
        self.marker_ix  += 1
        if self.marker_ix >= self.max_marker:
            self.marker_ix = 0
        self.marker_style       = self.markers[ self.marker_ix ]
        return self.marker_style

    # -----------------------------------------------
    def get_next_style( self,  ):
        """
        get the next tuple: ( line, color, marker )
        return tuple see below !! change to named tuple ??
        can use the returned or perhaps cleare the instance var like   .marker_style
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
