import wx

class Interactor(object):
	def setup(self, presenter, view):
        self.presenter = presenter
        self.view = view
		view.Bind(wx.EVT_CLOSE, self.presenter.closeWindow(evt))
		view.comboTrendindicator.Bind(wx.EVT_COMBOBOX, presenter.onChangeTrendindicator)
		# view.fetchButton.Bind(wx.EVT_BUTTON, self.fetch)
		
	# def fetch(self):
		# self.presenter.drawGraph(self, evt)
	