'''
Created on Jan 22, 2013
Presenter / ViewModel for trendindicator app
@author: Pyranja
'''
import core.trader

class SettingsPresenter(object):
    '''
    Accepts and validates settings input and invokes processing. 
    '''

    def __init__(self, view, index_repo):
        '''
        Requires its view and processing core.
        '''
        self.view = view
        self.idx_repo = index_repo
        self.idx_key = None
    
    def updateIndex(self):
        '''
        Fetch index data for set symbol and date range
        '''
        if self.idx_key:
            self.idx_repo.remove(self.idx_key)
        symbol = self.view.stock_symbol
        start = self.view.stock_start
        end = self.view.stock_end
        # validation
        try:
            self.idx_key = self.idx_repo.fetch(symbol, start, end)
        except StandardError as e:
            self.view.notify(e)
            
    def updateSettings(self):
        '''
        Validate input and set up processing pipe 
        '''
        pass

class GraphPresenter(object):
    '''
    Prepares graph data for plotting.
    '''
    pass
