from pywinauto import Application
app = Application().start("firefox")

# Connect to the actual firefox process forked by launcher
app = Application()
app.connect(path="firefox")