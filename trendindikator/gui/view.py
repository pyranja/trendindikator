'''
Created on 06.11.2012

@author: Manuel Graf
'''
import wx.lib.intctrl
import wx.lib.masked.numctrl
from wx.lib.plot import PlotCanvas
import datetime
import core.indicator
import core.trader

INDICATOR_TYPES = [core.indicator.SIG_BUY_HOLD, core.indicator.SIG_BREAK_RANGE, core.indicator.SIG_SIMPLE_MOVING_AVERAGE, core.indicator.SIG_DUAL_MOVING_AVERAGE]
TRADER_MODES = [core.trader.TRADE_SHORTLONG, core.trader.TRADE_LONG, core.trader.TRADE_SHORT]

CTRL_BORDER = 3
COMP_BORDER = 5

def wxDateToPyDate(date):
    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        return datetime.date(*ymd)
    else:
        return None
    
def pyDateToWxDate(date):
    assert isinstance(date, (datetime.datetime, datetime.date))
    tt = date.timetuple()
    dmy = (tt[2], tt[1]-1, tt[0])
    return wx.DateTimeFromDMY(*dmy)


class IndicatorView(wx.Panel):
    '''
    indicator options container
    '''
    def __init__(self, parent, id, name, **kwargs):
        wx.Panel.__init__(self, parent, id, **kwargs)
        self.parent = parent
        self.name = name
        sizer = self.build()
        self.SetSizer(sizer)
        self.signaler_type = core.indicator.SIG_BUY_HOLD
    
    def build(self):
        root_box = wx.BoxSizer(wx.HORIZONTAL)
        left_box = wx.BoxSizer(wx.VERTICAL)
        right_box = wx.BoxSizer(wx.VERTICAL)
        
        name_label = wx.StaticText(self, label=self.name)
        self.type_chooser = wx.ComboBox(self, choices = INDICATOR_TYPES, style = wx.CB_READONLY)
        
        self.threshold_spinner = wx.SpinCtrl(self, min = 0)
        self.factor_ctrl = wx.lib.masked.numctrl.NumCtrl(self, integerWidth = 1, fractionWidth = 2, min = 0.0, max = 1.0)
        self.history1_spinner = wx.SpinCtrl(self, min = 0)
        self.history2_spinner = wx.SpinCtrl(self, min = 0)
        
        left_box.Add(name_label, flag = wx.ALL, border = 5)
        left_box.Add(self.type_chooser, flag = wx.ALL, border = 5)
        right_box.Add(wx.StaticText(self, label = "signal lag"))
        right_box.Add(self.threshold_spinner, flag = wx.TOP, border = 2)
        right_box.Add(wx.StaticText(self, label = "envelope"), flag = wx.TOP, border = 5)
        right_box.Add(self.factor_ctrl, flag = wx.TOP, border = 2)
        right_box.Add(wx.StaticText(self, label = "fast range"), flag = wx.TOP, border = 5)
        right_box.Add(self.history1_spinner, flag = wx.TOP, border = 2)
        right_box.Add(wx.StaticText(self, label = "slow range"), flag = wx.TOP, border = 5)
        right_box.Add(self.history2_spinner, flag = wx.TOP, border = 2)

        root_box.Add(left_box, flag = wx.ALL, border = 10)
        root_box.Add(right_box, flag = wx.ALL, border = 10)
        return root_box
            
    @property
    def signaler_type(self):
        return self.type_chooser.GetValue()
        
    @signaler_type.setter
    def signaler_type(self, value):
        self.type_chooser.SetValue(value)
    
    @property
    def signal_threshold(self):
        return self.threshold_spinner.GetValue()
        
    @signal_threshold.setter
    def signal_threshold(self, value):
        self.threshold_spinner.SetValue(value)
    
    @property
    def envelope_factor(self):
        return self.factor_ctrl.GetValue()
        
    @envelope_factor.setter
    def envelope_factor(self, value):
        self.factor_ctrl.SetValue(value)
    
    @property
    def history_param1(self):
        if self.history1_spinner.IsEnabled():
            return self.history1_spinner.GetValue()
        else:
            return None
        
    @history_param1.setter
    def history_param1(self, value):
        self.history1_spinner.Enable()
        self.history1_spinner.SetValue(value)
        
    @history_param1.deleter
    def history_param1(self):
        self.history1_spinner.Disable()
    
    @property
    def history_param2(self):
        if self.history2_spinner.IsEnabled():
            return self.history2_spinner.GetValue()
        else:
            return None
        
    @history_param2.setter
    def history_param2(self, value):
        self.history2_spinner.Enable()
        self.history2_spinner.SetValue(value)
        
    @history_param2.deleter
    def history_param2(self):
        self.history2_spinner.Disable()

class MainFrame(wx.Frame):
    
    def __init__(self, parent, id, **kwargs):
        wx.Frame.__init__(self, parent, id, **kwargs)
        self.parent = parent
        panel = wx.Panel(self) # panel for entire frame
        self.indicator1 = IndicatorView(panel, -1, "indicator1")
        self.indicator2 = IndicatorView(panel, -1, "indicator2")
        self.build(panel)
        self.trader_mode = core.trader.TRADE_SHORTLONG
        self.initial_funds = 10000
        self.stock_symbol = "aapl"
        self.stock_start = datetime.datetime(2008,1,30)
        self.stock_end = datetime.datetime(2013,1,30)
        self.btn_process.Disable()
        
    def build(self, panel):
        hboxMain = wx.BoxSizer(wx.HORIZONTAL)
        
        vboxInput = wx.BoxSizer(wx.VERTICAL)
        
        # horizontal box containing labels for index including date (from-to)
        hboxIndexLabel = wx.BoxSizer(wx.HORIZONTAL)
        hboxIndexLabel.Add(wx.StaticText(panel, label='Index'), flag = wx.RIGHT, border = 81)
        hboxIndexLabel.Add(wx.StaticText(panel, label='Begin'), flag = wx.RIGHT, border = 70)
        hboxIndexLabel.Add(wx.StaticText(panel, label='Ende'))
        
        vboxInput.Add(hboxIndexLabel, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 10)
        
        # horizontal box containing value-fields for index including date (from-to)
        hboxIndexValue = wx.BoxSizer(wx.HORIZONTAL)
        
        self.ctrl_stock_name = wx.TextCtrl(panel)
        hboxIndexValue.Add(self.ctrl_stock_name, flag = wx.RIGHT, border = 8)
        self.ctrl_stock_start = wx.DatePickerCtrl(panel, -1, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        hboxIndexValue.Add(self.ctrl_stock_start)
        self.ctrl_stock_end = wx.DatePickerCtrl(panel, -1, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        hboxIndexValue.Add(self.ctrl_stock_end)
        
        vboxInput.Add(hboxIndexValue, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 10)
        
        # fetch button
        self.btn_update_index = wx.Button(panel, label = "Fetch Index")
        vboxInput.Add(self.btn_update_index, flag = wx.ALL, border = 5)
        self.btn_process = wx.Button(panel, label = "Process")
        vboxInput.Add(self.btn_process, flag = wx.ALL, border = 5)
        
        vboxInput.Add((-1, 10)) # space between index and trader
        
        # trader options
        vboxTraderLeft = wx.BoxSizer(wx.VERTICAL)
        self.ctrl_trader_mode = wx.ComboBox(panel, choices = TRADER_MODES, style = wx.CB_READONLY)
        vboxTraderLeft.Add(wx.StaticText(panel, label='Trader'), flag = wx.ALL, border = 5)
        vboxTraderLeft.Add(self.ctrl_trader_mode, flag = wx.ALL, border = 5)

        vboxTraderRight = wx.BoxSizer(wx.VERTICAL)
        
        hboxTraderToggles = wx.BoxSizer(wx.HORIZONTAL)
        self.ctrl_dynamic = wx.CheckBox(panel, label="dynamic")
        self.ctrl_reverse = wx.CheckBox(panel, label="reverse")
        self.ctrl_initial_funds = wx.lib.intctrl.IntCtrl(panel)
        hboxTraderToggles.Add(self.ctrl_dynamic, flag = wx.ALL, border = 5)
        hboxTraderToggles.Add(self.ctrl_reverse, flag = wx.ALL, border = 5)
        vboxTraderRight.Add(hboxTraderToggles, flag = wx.ALL, border = 5)
        vboxTraderRight.Add(self.ctrl_initial_funds, flag = wx.ALL, border = 5)
        
        vboxTraderOptions = wx.BoxSizer(wx.HORIZONTAL)
        vboxTraderOptions.Add(vboxTraderLeft)
        vboxTraderOptions.Add(vboxTraderRight)

        vboxInput.Add(vboxTraderOptions, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 10)
        
        # horizontal box containing labels for trendindicator
        vboxInput.Add(self.indicator1, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 10)
        vboxInput.Add(self.indicator2, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 10)

        # panel for plotting the graph
        vboxOutput = wx.BoxSizer(wx.VERTICAL)
        canvas = PlotCanvas(panel)
        canvas.SetEnableLegend(True)
        canvas.SetEnableDrag(True)
        canvas.SetShowScrollbars(True)
        canvas.SetEnableZoom(True)
        canvas.SetEnableAntiAliasing(True)
        self.canvas = canvas
        self.text_out = wx.StaticText(panel, label = "no text")
        
        vboxOutput.Add(self.canvas, 3, flag = wx.EXPAND)
        vboxOutput.Add(self.text_out, 1)
        
        # sizer for entire frame
        hboxMain.Add(vboxInput)         
        hboxMain.Add(vboxOutput, 1, flag = wx.EXPAND)
        
        panel.SetSizer(hboxMain)

    def closeWindow(self, event):
        self.Destroy()
        
    def notify(self, message):
        new_text = self.text_out.GetLabelText() + "\n" + message
        self.text_out.SetLabel(new_text)
        
    def report(self, text):
        self.text_out.SetLabel(text)
        
    def set_can_process(self, i_can = True):
        if i_can:
            self.btn_process.Enable()
        else:
            self.btn_process.Disable()

    # --> index properties        
    @property
    def stock_symbol(self):
        return self.ctrl_stock_name.GetValue()
    
    @stock_symbol.setter
    def stock_symbol(self, value):
        self.ctrl_stock_name.SetValue(value)

    @property
    def stock_start(self):
        return wxDateToPyDate(self.ctrl_stock_start.GetValue())
        
    @stock_start.setter
    def stock_start(self, value):
        self.ctrl_stock_start.SetValue(pyDateToWxDate(value))
    
    @property
    def stock_end(self):
        return wxDateToPyDate(self.ctrl_stock_end.GetValue())
        
    @stock_end.setter
    def stock_end(self, value):
        self.ctrl_stock_end.SetValue(pyDateToWxDate(value))
    
    # --> trader properties
    @property
    def trader_mode(self):
        return self.ctrl_trader_mode.GetValue()
        
    @trader_mode.setter
    def trader_mode(self, value):
        self.ctrl_trader_mode.SetValue(value)
    
    @property
    def initial_funds(self):
        return self.ctrl_initial_funds.GetValue()
        
    @initial_funds.setter
    def initial_funds(self, value):
        self.ctrl_initial_funds.SetValue(value)
    
    @property
    def dynamic(self):
        return self.ctrl_dynamic.GetValue()
        
    @dynamic.setter
    def dynamic(self, value):
        self.ctrl_dynamic.SetValue(value)
    
    @property
    def reverse(self):
        return self.ctrl_reverse.GetValue()
        
    @reverse.setter
    def reverse(self, value):
        self.ctrl_reverse.SetValue(value)
        
