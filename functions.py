import wx
from pydub import AudioSegment

class converterApp(wx.Frame):
    def __init__(self, parent, title):
        super(converterApp, self).__init__(parent, title=title, size=(300, 200))
        self.InitUi()
        self.Centre()
        self.Show()

    def InitUi(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Primero el cuadro de edición para la ruta del archivo
        name_to_convert = wx.StaticText(panel, label="Escribe o pega la ruta del archivo a convertir (con formato)")
        vbox.Add(name_to_convert, flag=wx.LEFT | wx.TOP, border=10)

        self.fileName = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        vbox.Add(self.fileName, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        # Luego el botón para añadir el archivo, con atajo de teclado
        self.select_file = wx.Button(panel, label="&Abrir el explorador")
        self.select_file.Bind(wx.EVT_BUTTON, self.file_select)
        vbox.Add(self.select_file, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # Después el cuadro para el nombre del archivo que se creará
        nameFile = wx.StaticText(panel, label="Escribe el nombre del archivo convertido:")
        vbox.Add(nameFile, flag=wx.LEFT | wx.TOP, border=10)
        self.name_from_file = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        vbox.Add(self.name_from_file, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        # Finalmente, los botones restantes con sus atajos
        self.ready = wx.Button(panel, label="&Convertir")
        self.ready.Bind(wx.EVT_BUTTON, self.audio_converter)
        vbox.Add(self.ready, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        self.exit_button = wx.Button(panel, label="&Salir del programa")
        self.exit_button.Bind(wx.EVT_BUTTON, self.exit_program)
        vbox.Add(self.exit_button, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)
    def file_select(self, event):
        with wx.FileDialog(self, "Seleccionar archivo de audio", wildcard="Archivos de audio (*.mp3;*.wav;*.opus;*.flac;*.m4a;*.ogg)|*.mp3;*.wav;*.opus;*.flac;*.m4a;*.ogg", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # El usuario canceló la selección
            path = fileDialog.GetPath()
            self.fileName.SetValue(path)
            self.name_from_file.SetFocus()

    def audio_converter(self, event):
        source_path = self.fileName.GetValue().strip()
        output_path = self.name_from_file.GetValue().strip()

        if not source_path or not output_path:
            wx.MessageBox("llena correctamente todos los campos.", "Error", wx.OK | wx.ICON_ERROR)
            return

        dialog = wx.SingleChoiceDialog(self, "Elige el formato a convertir:", "Selecciona formato", ["mp3", "wav", "m4a", "opus", "flac"])
        if dialog.ShowModal() == wx.ID_OK:
            selected_format = dialog.GetStringSelection()
            
            try:
                audio = AudioSegment.from_file(source_path)
                output_file = f"{output_path}.{selected_format}"
                audio.export(output_file, format=selected_format)
                wx.MessageBox(f'Archivo convertido y guardado en: {output_file}', "Conversión completada", wx.OK | wx.ICON_INFORMATION)
                self.fileName.SetValue("")
                self.name_from_file.SetValue("")
                self.fileName.SetFocus()
            except Exception as e:
                wx.MessageBox(f"Error durante la conversión: {e}", "Error", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

    def exit_program(self, event):
        self.Close(True)
