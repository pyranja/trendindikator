'''
Created on Jan 22, 2013
Presenter / ViewModel for trendindicator app
@author: Pyranja
'''
import core.trader
import wx.lib.plot
from core import analyzer

TRADER_MODES = [core.trader.TRADE_SHORTLONG, core.trader.TRADE_SHORT, core.trader.TRADE_LONG]
SIG_TYPES = [core.indicator.SIG_BUY_HOLD, core.indicator.SIG_BUY_HOLD, core.indicator.SIG_SIMPLE_MOVING_AVERAGE, core.indicator.SIG_DUAL_MOVING_AVERAGE]

class SettingsPresenter(object):
    '''
    Accepts and validates settings input and invokes processing. 
    '''

    def __init__(self, view, graphics, index_repo):
        '''
        Requires its view and processing core.
        '''
        self.view = view
        self.graphics = graphics
        self.idx_repo = index_repo
        self.idx_key = None
    
    def update_index(self):
        '''
        Fetch index data for set symbol and date range
        '''
        if self.idx_key:
            self.idx_repo.remove(self.idx_key)
        symbol = self.view.stock_symbol
        start = self.view.stock_start
        end = self.view.stock_end
        # validation ?
        try:
            self.view.freeze()
            self.idx_key = self.idx_repo.fetch(symbol, start, end)
            self.view.can_process = True
            self.graphics.draw_index(self.idx_key, symbol)
        except StandardError as e:
            self.view.notify(e)
        finally:
            self.view.thaw()

    def invoke_pipe(self):
        '''
        set up processing pipe and process currently set index 
        '''
        v = self.view   # less typing
        v.freeze()
        pipe = core.pipe.PipeSpec()
        try:
            actor_ids = []
            actor = self.make_actor(v, v.indicator1)
            pipe.add(actor)
            actor_ids.append(actor.name)
            actor = self.make_actor(v, v.indicator2)
            pipe.add(actor)
            actor_ids.append(actor.name)
            index = self.idx_repo.get(self.idx_key)
            plot = pipe.invoke(index)
            # make statistics
            statistics = []
            for actor_id in actor_ids:
                 stats = analyzer.Statistics(actor_id, v.initial_funds)
                 stats.feed(plot, actor_id)
                 statistics.append(stats)
            # call graphics to draw plot
            self.graphics.draw_plot(plot)
        except StandardError as e:
            v.notify(e)
        finally:
            v.thaw()
        
    def make_actor(self, v, i):
        actor = core.pipe.Actor(i.name)
        actor.trader = core.trader.create_trader(v.initial_funds, v.dynamic, v.trader_mode, v.reverse)
        args = []
        if i.history_param1 is not None:
            args.append(i.history_param1)
        if i.history_param2 is not None:
            args.append(i.history_param2)
        actor.signaler = core.indicator.create_signaler(i.signaler_type, i.signal_threshold, i.envelope_factor, *args)
        return actor
    
    def validate_view(self):
        '''
        examine each view property and verify integrity
        '''
        v = self.view   # less typing
        # verify trader
        if v.initial_funds < 0:
            v.initial_funds = 0
            v.notify("Initial funds must be positive")
        if not v.trader_mode in TRADER_MODES:
            v.trader_mode = core.indicator.SIG_BUY_HOLD
            v.notify("Invalid trader mode")
        # verify signaler
        self.validate_indicator(v.indicator1)
        self.validate_indicator(v.indicator2)
                
    def validate_indicator(self, i):
        if i.signal_threshold < 0:
           i.signal_threshold = 0
           i.notify("Signal threshold must be positive", i)
        if i.envelope_factor < 0.0 or i.envelope_factor > 1.0:
            i.envelop_factor = 0.0
            i.notify("Envelope factor must be in [0..1]", i)
        if not i.signaler_type in SIG_TYPES:
            i.signaler_type = core.indicator.SIG_BUY_HOLD
            i.notify("Invalid signaler type", i)
        sig_type = i.signaler_type
        # need one argument
        if sig_type == core.indicator.SIG_BREAK_RANGE or sig_type == core.indicator.SIG_SIMPLE_MOVING_AVERAGE:
            if i.history_param1 < 0:
                i.history_param1 = 0
                i.notify("Chosen signaler needs one positive parameter", i)
        elif sig_type == core.indicator.SIG_DUAL_MOVING_AVERAGE:
            if i.history_param2 < 0:
                i.history_param1 = 0
                error = True
            if i.history_param2 < 0:
                i.history_param2 = 0
                error = True
            if error:
                i.notify("Chosen signaler need two positive parameters", i)

class GraphPresenter(object):
    '''
    Prepares graph data for plotting.
    '''
    def __init__ (self, view, repo):
        self.view = view
        self.repo = repo
        
    def draw_index(self, key, stock_name):
        '''
        Draw only index from repo
        '''
        try:
            index = self.repo.get(key)
        except StandardError as e:
            self.view.notify(e)
        else:
            index_points = [(idx, point.price) for idx, point in enumerate(index)]
            index_line = wx.lib.plot.PolyLine(index_points, legend = "index")
            self.view.canvas.Draw(wx.lib.plot.PlotGraphics([index_line], title = stock_name, xLabel = "", yLabel = "price"))
            
    def draw_plot(self, plot):
        '''
        Draw results of pipe processing
        '''
        pass
            
    def print_statistics(self, statistics):
        '''
        Print gathered statistics line by line 
        '''
        text = ""
        for stats in statistics:
            text += "Indicator {} :\n".format(statistics.name)
            text += "transactions : {} | total yield : {:.2} <> relative {:.2%}\n".format(statistics.total_yield, statistics.relative_yield, statistics.tx_count)
            text += "yields : min {:.2} , max {:.2} , average {:.2%} | volatility {:.2%}\n".format(statistics.min_yield, statistics.max_yield, statistics.average_yield, statistics.volatility)
            text += "{:=^30}\n".format("=")
        self.view.report(text)
        
    