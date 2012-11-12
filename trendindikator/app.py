'''
Created on 06.11.2012

@author: Manuel Graf
'''
import wx
import gui

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = gui.MainFrame(parent = None, id = -1) 
    frame.Show()
    app.MainLoop()