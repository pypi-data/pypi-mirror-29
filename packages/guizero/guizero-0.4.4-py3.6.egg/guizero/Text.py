from tkinter import Label, StringVar
from .mixins import WidgetMixin
from .tkmixins import ScheduleMixin, DestroyMixin, EnableMixin, FocusMixin, DisplayMixin, TextMixin, ColorMixin, ReprMixin
from . import utilities as utils

class Text(
    WidgetMixin, 
    ScheduleMixin, 
    DestroyMixin, 
    EnableMixin, 
    FocusMixin, 
    DisplayMixin, 
    TextMixin,
    ColorMixin,
    ReprMixin):

    def __init__(self, master, text="", size=12, color="black", bg=None, font="Helvetica", grid=None, align=None):

        self._master = master
        self._grid = grid
        self._align = align
        self._visible = True

        # Description of this object (for friendly error messages)
        self.description = "[Text] object with text \"" + str(text) + "\""

        # Create a tk Label object within this object
        self.tk = Label(master.tk, text=text, fg=color, bg=bg, font=(font, size))

        if bg:
            self.bg = bg
        
        self._text = str(text)

        # Pack this object
        try:
            utils.auto_pack(self, master, grid, align)
       	except AttributeError:
            utils.error_format( self.description + "\n" +
            "Could not add to interface - check first argument is [App] or [Box]")

    # PROPERTIES
    # ----------------------------------

    # The text value
    @property
    def value(self):
        return (self._text)

    @value.setter
    def value(self, value):
        self.tk.config(text=value)
        self._text = str(value)
        self.description = "[Text] object with text \"" + str(value) + "\""

    # The font size
    @property
    def size(self):
        return self.text_size

    @size.setter
    def size(self, size):
        self.text_size = size

    # METHODS
    # -------------------------------------------

    # Clear text (set to empty string)
    def clear(self):
        self._text = ""
        self.tk.config(text="")

    # Append some text onto the end of the existing text
    def append(self, text):
        new_text = self._text + str(text)
        self._text = new_text
        self.tk.config(text=new_text)
        self.description = "[Text] object with text \"" + new_text + "\""


    # DEPRECATED METHODS
    # --------------------------------------------

    # Sets the text colour
    def color(self, color):
        self._current_color = color
        self.tk.config(fg=color)
        utils.deprecated("Text color() is deprecated. Please use the text_color property instead.")

    # Set the font
    def font_face(self, font):
        self._current_font = font
        self.tk.config(font=(self._current_font, self._current_size))
        utils.deprecated("Text font_face() is deprecated. Please use font property instead.")

    # Set the font size
    def font_size(self, size):
        self._current_size = size
        self.tk.config(font=(self._current_font, self._current_size))
        utils.deprecated("Text font_size() is deprecated. Please use the size property instead.")

     # Returns the text
    def get(self):
        return self._text
        utils.deprecated("Text get() is deprecated. Please use the value property instead.")

    # Sets the text
    def set(self, text):
        self._text = str(text)
        self.tk.config(text=self._text)
        self.description = "[Text] object with text \"" + str(text) + "\""
        utils.deprecated("Text set() is deprecated. Please use the value property instead.")
