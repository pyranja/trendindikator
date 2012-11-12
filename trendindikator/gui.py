'''
Created on 06.11.2012

@author: Manuel Graf
'''
import wx
import wx.lib.plot
from wx.lib.plot import PlotCanvas


class MainFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Trendindikator vs Buy and Hold', size=(1000,500))
        
        panel = wx.Panel(self) # panel for entire frame
        
        hboxMain = wx.BoxSizer(wx.HORIZONTAL) # sizer for entire frame
        
        vboxInput = wx.BoxSizer(wx.VERTICAL)
        
        # horizontal box containing labels for index including date (from-to)
        hboxIndexLabel = wx.BoxSizer(wx.HORIZONTAL)
        
        staticTextIndex = wx.StaticText(panel, label='Index')
        hboxIndexLabel.Add(staticTextIndex, flag = wx.RIGHT, border = 81)
        
        staticTextDateFrom = wx.StaticText(panel, label='Begin')
        hboxIndexLabel.Add(staticTextDateFrom, flag = wx.RIGHT, border = 70)
        
        staticTextDateTo = wx.StaticText(panel, label='Ende')
        hboxIndexLabel.Add(staticTextDateTo)
        
        vboxInput.Add(hboxIndexLabel, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 10)
        
        
        # horizontal box containing value-fields for index including date (from-to)
        hboxIndexValue = wx.BoxSizer(wx.HORIZONTAL)
        
        textCtrlIndex = wx.TextCtrl(panel)
        hboxIndexValue.Add(textCtrlIndex, flag = wx.RIGHT, border = 8)
        
        datePickerFrom = wx.DatePickerCtrl(panel, -1, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        hboxIndexValue.Add(datePickerFrom)
        
        datePickerTo = wx.DatePickerCtrl(panel, -1, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        hboxIndexValue.Add(datePickerTo)
        
        vboxInput.Add(hboxIndexValue, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 10)
        
        
        vboxInput.Add((-1, 10)) # spacer between hboxes
        
        
        # horizontal box containing labels for trendindicator
        hboxTrendindicatorLabel = wx.BoxSizer(wx.HORIZONTAL)
        
        staticTextTrendindicator = wx.StaticText(panel, label='Trendindikator')
        hboxTrendindicatorLabel.Add(staticTextTrendindicator, flag = wx.RIGHT, border = 61)
        
        staticTextTrendindicatorOption = wx.StaticText(panel, label='Trendindikator-Optionen')
        hboxTrendindicatorLabel.Add(staticTextTrendindicatorOption)
        
        vboxInput.Add(hboxTrendindicatorLabel, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 10)
        
        
        # horizontal box containing trendindicator
        hboxTrendindicatorValue = wx.BoxSizer(wx.HORIZONTAL)
        
        trendindicatorList = ["abc", "def"]
        comboTrendindicator = wx.ComboBox(panel, choices = trendindicatorList, style=wx.CB_READONLY)
        hboxTrendindicatorValue.Add(comboTrendindicator)
        
        #vertical static line seperating trendindicator-combobox from trendindicator-options
#        vline = wx.StaticLine(panel, -1, style = wx.LI_VERTICAL)
#        vline.SetSize((300, 10))
#        hboxTrendindicatorValue.Add(vline)
        
        # vertical box nested in 'hboxTrendindicatorValue' containing trendindicator-options
        vboxTrendindicatorValueOption = wx.BoxSizer(wx.VERTICAL)
        
        toggleButtonOption1 = wx.ToggleButton(panel, label = 'Option 1')
        vboxTrendindicatorValueOption.Add(toggleButtonOption1)
        
        toggleButtonOption2 = wx.ToggleButton(panel, label = 'Option 2')
        vboxTrendindicatorValueOption.Add(toggleButtonOption2)
        
        hboxTrendindicatorValue.Add(vboxTrendindicatorValueOption, flag = wx.LEFT, border = 83)

        vboxInput.Add(hboxTrendindicatorValue, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 10)

        hboxMain.Add(vboxInput)
        
        # panle for plotting the graph
        canvas = PlotCanvas(panel)
        canvas.SetEnableZoom(True)
        canvas.SetEnableAntiAliasing(True)
        canvas.Draw(drawGraph())
        
        hboxMain.Add(canvas, 1, wx.EXPAND)
        
        panel.SetSizer(hboxMain)

        self.Bind(wx.EVT_CLOSE, self.closeWindow)

        # Statusbar
        statusbar = self.CreateStatusBar()

        # Menubar
        menubar = wx.MenuBar()
        menuFile = wx.Menu()
        menuFile.Append(wx.NewId(), "New File", "open new file")
        menubar.Append(menuFile, "File")
        menuSettings = wx.Menu()
        menuSettings.AppendRadioItem(-1, 'Indikator Moving Averages')
        menuSettings.AppendRadioItem(-1, 'Indikator Standard')
        menuIndikator = wx.Menu()
        menuIndikator.AppendCheckItem(wx.ID_ANY, 'Option 1')
        menuIndikator.AppendCheckItem(wx.ID_ANY, 'Option 2')
        menuSettings.AppendMenu(wx.ID_ANY, 'Indikator-Options', menuIndikator)
        menubar.Append(menuSettings, "Settings")

        self.SetMenuBar(menubar)
        

    def closeWindow(self, event):
#        # dialog-box close programm
#        box = wx.MessageDialog(None, 'Are you shure you wan\'t exit', 'Exit', wx.YES_NO)
#        selection = box.ShowModal()
#        if selection == 5103:
            self.Destroy()
        

        
def drawGraph():
    data10 = [(x,y) for x, y in zip(range(10),range(10))]
    lines1 = wx.lib.plot.PolyLine(data10, legend= 'Red Line', colour='black')
    
    return wx.lib.plot.PlotGraphics([lines1],"Title", "X axis", "Y axis")