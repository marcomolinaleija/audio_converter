import logging
import wx
import os
import winreg as reg

# Configura el logging
logging.basicConfig(filename='addPath.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class addPath(wx.Frame):
    def __init__(self, parent, title):
        super(addPath, self).__init__(parent, title=title, size=(300, 200))
        self.InitUi()
        self.Centre()
        self.Show()

    def InitUi(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        name_folder = wx.StaticText(panel, label="Carpeta a añadir")
        vbox.Add(name_folder, flag=wx.LEFT | wx.TOP, border=10)

        self.entry_folder = wx.TextCtrl(panel, style=wx.TE_READONLY)
        vbox.Add(self.entry_folder, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        self.select_folder = wx.Button(panel, label="Selecciona una carpeta")
        self.select_folder.Bind(wx.EVT_BUTTON, self.select_path)
        vbox.Add(self.select_folder, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        self.exit = wx.Button(panel, label="Salir")
        self.exit.Bind(wx.EVT_BUTTON, self.Exit)
        vbox.Add(self.exit, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def select_path(self, event):
        logging.info("Intentando seleccionar una carpeta")
        dirDialog = wx.DirDialog(self, "Elige una carpeta", style=wx.DD_DEFAULT_STYLE)
        if dirDialog.ShowModal() == wx.ID_OK:
            folderPath = dirDialog.GetPath()
            self.entry_folder.SetValue(folderPath)
            logging.info(f"Carpeta seleccionada: {folderPath}")
            self.add_to_path(folderPath)
        else:
            logging.info("Selección de carpeta cancelada por el usuario")
        dirDialog.Destroy()

    def add_to_path(self, new_path):
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, 'Environment', 0, reg.KEY_ALL_ACCESS) as key:
                path, _ = reg.QueryValueEx(key, 'PATH')
                if new_path not in path:
                    newPath = f"{path};{new_path}"
                    reg.SetValueEx(key, 'PATH', 0, reg.REG_EXPAND_SZ, newPath)
                    wx.MessageBox(f"La carpeta {new_path} se ha añadido al PATH del sistema.", "Listo", wx.OK | wx.ICON_INFORMATION)
                    logging.info(f"La carpeta {new_path} se ha añadido al PATH del sistema.")
                else:
                    wx.MessageBox("La carpeta ya está en el PATH del sistema.", "Información", wx.OK | wx.ICON_INFORMATION)
                    logging.info("La carpeta ya estaba en el PATH del sistema.")
        except Exception as e:
            logging.exception("Error al añadir la carpeta al PATH del sistema.")
            wx.MessageBox(f"Error al añadir la carpeta al PATH: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def Exit(self, event):
        logging.info("Cerrando la aplicación")
        self.Close(True)

if __name__ == "__main__":
    logging.info("Iniciando la aplicación")
    app = wx.App(False)
    frame = addPath(None, "Añadir al PATH")
    app.MainLoop()
