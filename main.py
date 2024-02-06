import wx
from functions import converterApp
def main():
    app=wx.App(False)
    frame=converterApp(None, "convertor de audio")
    app.MainLoop()

if __name__ == "__main__":
    main()