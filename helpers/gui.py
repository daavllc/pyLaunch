import tkinter as tk
from tkinter import ttk

from helpers.style import Style

def Label(parent: tk.Frame, text: str, justify: str ='center', anchor: str = None, width: int = None, height: int = None, wraplength = None, font = Style.Get().FONT_TEXT, bg: int = -1, fg: int = 0):
    return tk.Label(parent, text=text, justify=justify, anchor=anchor, width=width, height=height, wraplength=wraplength, font=font, bg=_GetLabelBackground(bg), fg=_GetTextForeground(fg))

def MonoLabel(parent: tk.Frame, text: str, justify: str ='center', anchor: str = None, width: int = None, height: int = None, wraplength = None, font = Style.Get().FONT_TEXT_MONO, bg: int = -1, fg: int = 0):
    return Label(parent, text=text, justify=justify, anchor=anchor, width=width, height=height, wraplength=wraplength, font=font, bg=bg, fg=fg)

def Title(parent: tk.Frame, text: str, justify: str ='center', anchor: str = None, width: int = None, height: int = None, wraplength = None, font = Style.Get().FONT_TITLE, bg: int = -1, fg: int = 0):
    return Label(parent, text=text, justify=justify, anchor=anchor, width=width, height=height, wraplength=wraplength, font=font, bg=bg, fg=fg)

def SmallLabel(parent: tk.Frame, text: str, justify: str ='center', anchor: str = None, width: int = None, height: int = None, wraplength = None, font = Style.Get().FONT_TEXT_SMALL, bg: int = -1, fg: int = 0):
    return Label(parent, text=text, justify=justify, anchor=anchor, width=width, height=height, wraplength=wraplength, font=font, bg=bg, fg=fg)

def LargeLabel(parent: tk.Frame, text: str, justify: str ='center', anchor: str = None, width: int = None, height: int = None, wraplength = None, font = Style.Get().FONT_TEXT_LARGE, bg: int = -1, fg: int = 0):
    return Label(parent, text=text, justify=justify, anchor=anchor, width=width, height=height, wraplength=wraplength, font=font, bg=bg, fg=fg)

def Button(parent: tk.Frame, text: str, justify: str ='center', anchor: str = None, width: int = None, height: int = None, command = None, bg: int = -1, fg: int = 0):
    return tk.Button(parent, text=text, justify=justify, anchor=anchor, width=width, height=height, command=command, font=Style.Get().FONT_TEXT, bg=_GetButtonBackground(bg), fg=_GetButtonForeground(fg))

def Text(parent: tk.Frame, width: int = None, height: int = None, bg: int = -1, fg: int = 0):
    return tk.Text(parent, width=width, height=height, font=Style.Get().FONT_TEXT, bg=_GetTextBackground(bg), fg=_GetTextForeground(fg))

def Checkbutton(parent: tk.Frame, text: str, variable, command = None, font = Style.Get().FONT_TEXT, bg: int = -1, fg: int = 0):
    return tk.Checkbutton(parent, text=text, variable=variable, command=command, font=font, background=_GetLabelBackground(bg), fg=_GetTextForeground(fg), selectcolor=_GetLabelBackground(bg))

def FillVerticalSeparator(parent, padx: int = 0, pady: int = 5):
    ttk.Separator(parent, orient='vertical').pack(fill='y', padx=padx, pady=pady)

def FillHorizontalSeparator(parent, padx: int = 5, pady: int = 0):
    ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=padx, pady=pady)

#def GridVerticalSeparator(parent, column: int, padx: int = 0, pady: int = 5):
#    ttk.Separator(parent, orient='vertical').grid(fill='y', padx=padx, pady=pady)
#
#def GridHorizontalSeparator(parent, row: int, padx: int = 5, pady: int = 0):
#    ttk.Separator(parent, orient='horizontal').grid(fill='x', padx=padx, pady=pady, row=row)



# Background Color helpers
def _GetBackground(bg: int) -> str:
    if bg == 0:
        return Style.Get().FRAME_BG
    elif bg == 1:
        return Style.Get().FRAME_BG_ALT
    else:
        return "#FF00FF"

def _GetLabelBackground(bg: int) -> str:
    if bg == -1:
        return Style.Get().LABEL_BG
    else:
        return _GetBackground(bg)

def _GetButtonBackground(bg: int) -> str:
    if bg == -1:
        return Style.Get().BUTTON_BG
    else:
        return _GetBackground(bg)

def _GetTextBackground(bg: int) -> str:
    if bg == -1:
        return Style.Get().TEXT_BG
    else:
        return _GetBackground(bg)

# Foreground color helpers
def _GetTextForeground(fg: int) -> str:
    if fg == -1:
        return Style.Get().TEXT_ERROR
    return Style.Get().TEXT_FG

def _GetButtonForeground(fg: int) -> str:
    return Style.Get().BUTTON_FG
