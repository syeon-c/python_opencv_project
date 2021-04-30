from pywinauto.application import Application 
import pywinauto 

app = pywinauto.application.Application() 

app = Application().start("notepad.exe")
app.connect(title="test - 메모장")
mainWindow = app['test']

ctrl=mainWindow['Edit1'] 
mainWindow.set_focus() 
ctrl.click_input()
ctrl.type_keys("test.txt")