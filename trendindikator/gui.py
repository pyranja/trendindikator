'''
Created on 06.11.2012

@author: Manuel Graf
'''
import wx


class TestFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Trendindikator vs Buy and Hold', size=(500,500))
        
        panel = wx.Panel(self) #panel for entire frame
        
        vbox = wx.BoxSizer(wx.VERTICAL) #sizer for entire frame
        
        #horizontal box containing labels for index including date (from-to)
        hboxIndexLabel = wx.BoxSizer(wx.HORIZONTAL)
        
        staticTextIndex = wx.StaticText(panel, label='Index')
        hboxIndexLabel.Add(staticTextIndex, flag = wx.RIGHT, border = 81)
        
        staticTextDateFrom = wx.StaticText(panel, label='Begin')
        hboxIndexLabel.Add(staticTextDateFrom, flag = wx.RIGHT, border = 70)
        
        staticTextDateTo = wx.StaticText(panel, label='Ende')
        hboxIndexLabel.Add(staticTextDateTo)
        
        vbox.Add(hboxIndexLabel, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 10)
        
        
        #horizontal box containing value-fields for index including date (from-to)
        hboxIndexValue = wx.BoxSizer(wx.HORIZONTAL)
        
        textCtrlIndex = wx.TextCtrl(panel)
        hboxIndexValue.Add(textCtrlIndex, flag = wx.RIGHT, border = 8)
        
        datePickerFrom = wx.DatePickerCtrl(panel, -1, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        hboxIndexValue.Add(datePickerFrom)
        
        datePickerTo = wx.DatePickerCtrl(panel, -1, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        hboxIndexValue.Add(datePickerTo)
        
        vbox.Add(hboxIndexValue, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 10)
        
        
        vbox.Add((-1, 10)) #spacer between hboxes
        
        #horizontal box containing trendindicator
        hboxTrendindicator = wx.BoxSizer(wx.HORIZONTAL)
        
        trendindicatorList = ["abc", "def"]
        comboTrendindicator = wx.ComboBox(panel, choices = trendindicatorList)
        comboTrendindicator.SetEditable(False)
        hboxTrendindicator.Add(comboTrendindicator)

        
        vbox.Add(hboxTrendindicator, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 10)
        
        #panelTest
#        panelTest = wx.Panel(self)
#        button = wx.Button(panelTest, label = "exit", pos = (130, 10), size = (60, 30))
#        self.Bind(wx.EVT_BUTTON, self.closeButton, button)
#
#        button2 = wx.Button(panelTest, label = "open Graph", pos = (10, 10), size = (80, 30))
##        self.Bind(wx.EVT_BUTTON, self.openGraph, button)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_CLOSE, self.closeWindow)

        #Statusbar
        statusbar = self.CreateStatusBar()

        #Menubar
        menubar = wx.MenuBar()
        menuFile = wx.Menu()
        menuSettings = wx.Menu()
        menuFile.Append(wx.NewId(), "New File", "open new file")
        menubar.Append(menuFile, "File")
        menubar.Append(menuSettings, "Settings")
        self.SetMenuBar(menubar)

    def closeButton(self, event):
        #Dialog-Box
        box = wx.MessageDialog(None, 'Are you shure you wan\'t exit', 'Exit', wx.YES_NO)
        selection = box.ShowModal()
        if selection == 5103:
            self.Close(True)

##    def openGraph(self, event):
        

    def closeWindow(self, event):
        self.Destroy()