'''
Created on 06.11.2012

@author: Manuel Graf
'''
import wx
import gui.view
import gui.interactor
import gui.presenter

if __name__ == '__main__':
	
    app = wx.PySimpleApp()
    frame = gui.view.MainFrame(parent = None, id = -1) 
    frame.Show()
    self.interactor = gui.interactor.Interactor(gui.presenter, gui.view)
  #  self.interactor.setup()
    app.MainLoop()