def titlechange(gui):
    if gui.title == "Icon":
        gui.setWindowTitle('Test')
        gui.title = "Test"
    else:
        gui.setWindowTitle('Icon')
        gui.title = "Icon"