import wx

class Interactor(object):
    def __init__(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.btn_update_index.Bind(wx.EVT_BUTTON, presenter.update_index)
        view.btn_process.Bind(wx.EVT_BUTTON, presenter.invoke_pipe)
        view.ctrl_trader_mode.Bind(wx.EVT_COMBOBOX, presenter.validate_view)
        view.indicator1.type_chooser.Bind(wx.EVT_COMBOBOX, presenter.validate_view)
        view.indicator2.type_chooser.Bind(wx.EVT_COMBOBOX, presenter.validate_view)
        
        #? view.Bind(wx.EVT_CLOSE, self.presenter.closeWindow)
