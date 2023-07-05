from App.main_app_window_base import MainAppWindowBase
from Core import algorithm
from Core.core_types import Point

class MainAppWindow(MainAppWindowBase):
    
    def __init__(self, tk_root):
        super().__init__(tk_root)
        
        # Init variables
        self.start_point = None

    def getGeneralColor(self):
        """ Returns the color of the general measurement """
        return super().getGeneralColor()
    
    def getHeartColor(self):
        """ Returns the color of the heart measurement """
        return super().getHeartColor()
    
    def getThoraxColor(self):
        """ Returns the color of the thorax measurement """
        return super().getThoraxColor()
    
    def on_mouse_click(self, event):
        """ Called when the user clicks or starts a drag on the canvas """
        self.start_point = Point(event.x, event.y)

    def on_mouse_drag(self,event):
        if self.start_point:
            self.update_current_line(self.start_point, Point(event.x, event.y), label=f"({event.x}, {event.y})")
        """ Called continuously while the user is dragging the mouse on the canvas """


    def on_mouse_release(self, event):
       
        if self.start_point and self.current_line:
            line_length = algorithm.distance(self.start_point.x, self.start_point.y, event.x, event.y)
            self.update_current_measurement(line_length)
            print(f"Line length: {line_length}")
           
            self.start_point = None
            
            self.current_line = None
    
    def save_measurement(self):
        """ Called when the user clicks the save button """
        print("TODO: Save the measurement")