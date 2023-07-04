from enum import Enum
from typing import Optional

import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

from Core import algorithm
from Core.core_types import Point

class MainAppWindowBase:
    class MeasurementType(Enum):
        Unset = 0
        Heart = 1
        Thorax = 2

    HEART_POS = Point(10, 10)  # Heart measurement text
    THORAX_POS = Point(10, 30)  # Thorax measurement text
    RATIO_POS = Point(10, 50)  # Ratio measurement text
    CURRENT_POS_OFFSET = Point(10, 10)  # Offset from the mouse
    CURRENT_SELECTION_OFFSET = Point(10, 10)  # Offset from bottom-right corner

    DEFAULT_COLOR_GENERAL = "white"
    DEFAULT_COLOR_HEART = "red"
    DEFAULT_COLOR_THORAX = "blue"

    def __init__(self, tk_root):
        self.tk_root = tk_root

        # Title
        self.title = tk.Label(tk_root, text="Cardiomegaly Measurement Tool", bg="#2176C1", fg='white', relief=tk.RAISED)
        self.title.pack(ipady=5, fill='x')

        # Load Image Button
        self.button_load = tk.Button(self.tk_root, text="Load Image", command=self.load_image)
        self.button_load.pack()

        # Measurement Buttons
        self.button_heart = tk.Button(self.tk_root, text="Heart", command=self.on_heart_measurement)
        self.button_thorax = tk.Button(self.tk_root, text="Thoracic", command=self.on_thoracic_measurement)
        self.button_heart.pack()
        self.button_thorax.pack()

        # Save Measurement
        # TODO - save to a csv?
        self.button_load = tk.Button(self.tk_root, text="Save Measurement", command=self.save_measurement)
        self.button_load.pack()

        # Canvas
        self.canvas_size = Point(800, 600)
        self.canvas = tk.Canvas(tk_root, width=self.canvas_size.x, height=self.canvas_size.y)
        self.canvas.pack()

        self.image = None
        self.photo = None
        self.image_widget = None

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # Init variables
        self.current_measurement = self.MeasurementType.Heart
        self.current_line = None
        self.current_measurement_text = None
        self.last_full_measurement_heart = self.create_heart_measurement_text(0)
        self.last_full_measurement_thorax = self.create_thorax_measurement_text(0)
        self.ratio_measurement = self.create_ratio_text(None)
        self.current_selection = self.create_selection_text("Selection: Heart")

        self.last_full_measurement_heart_val = None
        self.last_full_measurement_thorax_val = None

    def update_image(self, image_path):
        if self.image:
            self.image.close()
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)

        # TODO: Image needs to be scaled to fit the canvas (right now it might get cropped)

        if self.image_widget:
            self.canvas.delete(self.image_widget)
        self.image_widget = self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def load_image(self):
        filename = askopenfilename()
        if filename:
            print(f"Selected {filename}")
            # Should probably first check if that a valid jpg image and gracefully fail if it's not...
            self.update_image(filename)
        else:
            print("No file selected")

    def getHeartColor(self):
        return self.DEFAULT_COLOR_HEART
    
    def getThoraxColor(self):
        return self.DEFAULT_COLOR_THORAX
    
    def getGeneralColor(self):
        return self.DEFAULT_COLOR_GENERAL

    def get_current_color(self):
        if self.current_measurement == self.MeasurementType.Heart:
            return self.getHeartColor()
        if self.current_measurement == self.MeasurementType.Thorax:
            return self.getThoraxColor()
        raise Exception(f"Unexpected MeasurementType! {self.current_measurement}")

    def create_selection_text(self, selection_text: str):
        return self.canvas.create_text(self.canvas_size.x - self.CURRENT_SELECTION_OFFSET.x, self.canvas_size.y - self.CURRENT_SELECTION_OFFSET.y, anchor=tk.SE, fill=self.getGeneralColor(), text=f"Selection: {selection_text}")

    def update_selection_text(self, selection_text: str):
        if self.current_selection:
            self.canvas.delete(self.current_selection)
        self.current_selection = self.create_selection_text(selection_text)

    def create_thorax_measurement_text(self, line_length: float):
        return self.canvas.create_text(self.THORAX_POS.x, self.THORAX_POS.y, anchor=tk.NW, fill=self.getThoraxColor(), text=f"Thorax: {line_length}")

    def create_heart_measurement_text(self, line_length: float):
        return self.canvas.create_text(self.HEART_POS.x, self.HEART_POS.y, anchor=tk.NW, fill=self.getHeartColor(), text=f"Heart: {line_length}")
    
    def create_ratio_text(self, ratio: Optional[float]):
        if ratio is None:
            txt = f"Ratio: Unknown"
        else:
            txt = f"Ratio: {ratio}"
        return self.canvas.create_text(self.RATIO_POS.x, self.RATIO_POS.y, anchor=tk.NW, fill=self.getGeneralColor(), text=txt)
    
    def update_current_measurement(self, line_length: float):
        line_length = int(line_length)
        if self.current_measurement == self.MeasurementType.Heart:
            if self.last_full_measurement_heart:
                self.canvas.delete(self.last_full_measurement_heart)
            self.last_full_measurement_heart = self.create_heart_measurement_text(line_length)
            self.last_full_measurement_heart_val = line_length
        elif self.current_measurement == self.MeasurementType.Thorax:
            if self.last_full_measurement_thorax:
                self.canvas.delete(self.last_full_measurement_thorax)
            self.last_full_measurement_thorax = self.create_thorax_measurement_text(line_length)
            self.last_full_measurement_thorax_val = line_length
        else:
            raise Exception(f"Unexpected MeasurementType! {self.current_measurement}")
        self.update_ratio()

    def update_ratio(self):
        if self.ratio_measurement:
            self.canvas.delete(self.ratio_measurement)
        ratio = None
        if self.last_full_measurement_thorax_val and self.last_full_measurement_heart_val:
            ratio = algorithm.calculate_ratio(self.last_full_measurement_heart_val, self.last_full_measurement_thorax_val)

        self.ratio_measurement = self.create_ratio_text(ratio)

    def on_heart_measurement(self):
        self.current_measurement = self.MeasurementType.Heart
        self.update_selection_text("Heart")

    def on_thoracic_measurement(self):
        self.current_measurement = self.MeasurementType.Thorax
        self.update_selection_text("Thorax")

    def update_current_line(self, start: Point, current: Point, label : str):
        if self.current_line:
            self.canvas.delete(self.current_line)
        if self.current_measurement_text:
            self.canvas.delete(self.current_measurement_text)

        self.current_measurement_text = self.canvas.create_text(current.x - self.CURRENT_POS_OFFSET.x, current.y - self.CURRENT_POS_OFFSET.y, fill=self.get_current_color(), text=label)
        self.current_line = self.canvas.create_line(start.x, start.y, current.x, current.y, fill=self.get_current_color())

    def on_mouse_click(self, event):
        pass

    def on_mouse_drag(self, event):
        pass

    def on_mouse_release(self, event):
        pass

