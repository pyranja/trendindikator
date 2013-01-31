'''
Created on 06.11.2012

@author: Manuel Graf
'''
import wx, os
import gui.view
import gui.interactor
import gui.presenter

from core.index import CsvRepository

if __name__ == '__main__':
	try:
		repo = CsvRepository(os.getcwd())
		app = wx.PySimpleApp()
		frame = gui.view.MainFrame(None, -1, title = "Trendindikator", size = (800, 600)) 
		frame.Show()
		graph_presenter = gui.presenter.GraphPresenter(frame, repo)
		main_presenter = gui.presenter.SettingsPresenter(frame, graph_presenter, repo)
		interactor = gui.interactor.Interactor(main_presenter, frame)
		main_presenter.validate_view(None)
		app.MainLoop()
	finally:
		repo.clear()