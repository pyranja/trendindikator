'''
Created on Jan 22, 2013
Presenter / ViewModel for trendindicator app
@author: Pyranja
'''
import core.trader
import core.indicator
import core.analyzer
import wx.lib.plot
from core import analyzer


TRADER_MODES = [core.trader.TRADE_SHORTLONG, core.trader.TRADE_SHORT, core.trader.TRADE_LONG]
SIG_TYPES = [core.indicator.SIG_BUY_HOLD, core.indicator.SIG_BREAK_RANGE, core.indicator.SIG_SIMPLE_MOVING_AVERAGE, core.indicator.SIG_DUAL_MOVING_AVERAGE]

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
    
    def update_index(self, evt):
        '''
        Fetch index data for set symbol and date range
        '''
        self.view.set_can_process(False)
        if self.idx_key is not None:
            self.idx_repo.delete(self.idx_key)
            self.idx_key = None
        symbol = self.view.stock_symbol
        start = self.view.stock_start
        end = self.view.stock_end
        # validation ?
        try:
            self.idx_key = self.idx_repo.fetch(symbol, start, end)
            self.view.notify("Loaded %s" % symbol)
            self.graphics.draw_index(self.idx_key, symbol)
            self.view.set_can_process(True)
        except StandardError as e:
            self.view.notify("Error on index update : %r" % e)
            raise

    def invoke_pipe(self, evt):
        '''
        set up processing pipe and process currently set index 
        '''
        v = self.view   # less typing
        pipe = core.pipe.PipeSpec()
        try:
            actor_ids = []
            actor = self._make_actor(v, v.indicator1)
            pipe.add(actor)
            actor_ids.append(actor.name)
            actor = self._make_actor(v, v.indicator2)
            pipe.add(actor)
            actor_ids.append(actor.name)
            index = self.idx_repo.get(self.idx_key)
            plot = pipe.invoke(index)
            if len(plot) > 0:
                # call graphics to draw plot
                self.graphics.draw_plot(plot, actor_ids[0]) # only plot first indicator
                # make statistics
                statistics = []
                for actor_id in actor_ids:
                    stats = core.analyzer.Statistics(actor_id, v.initial_funds)
                    stats.feed(plot, actor_id)
                    statistics.append(stats)
                self.graphics.print_statistics(statistics)
            else:
                v.notify("No data gathered -> index range to small?")
        except StandardError as e:
            v.notify("Error on pipe processing : %r" % e)
            raise
        
    def _make_actor(self, v, i):
        actor = core.pipe.Actor(i.name)
        actor.trader = core.trader.create_trader(v.initial_funds, v.dynamic, v.trader_mode, v.reverse)
        args = []
        if i.history_param1 is not None:
            args.append(i.history_param1)
        if i.history_param2 is not None:
            args.append(i.history_param2)
        actor.signaler = core.indicator.create_signaler(i.signaler_type, i.signal_threshold, i.envelope_factor, *args)
        return actor
    
    def validate_view(self, evt):
        '''
        examine each view property and verify integrity
        '''
        v = self.view   # less typing
        # verify trader
        if v.initial_funds < 100:
            v.initial_funds = 10000
            v.notify("Initial funds must be positive")
        if not v.trader_mode in TRADER_MODES:
            v.trader_mode = core.trader.TRADE_SHORTLONG
            v.notify("Invalid trader mode")
        # verify signaler
        self._display_signaler_options(v.indicator1)
        self._validate_indicator(v.indicator1)
        self._display_signaler_options(v.indicator2)
        self._validate_indicator(v.indicator2)

    def _display_signaler_options(self, iv):
        sig_type = iv.signaler_type
        if sig_type == core.indicator.SIG_BUY_HOLD:
            del iv.history_param1
            del iv.history_param2
        elif sig_type in (core.indicator.SIG_BREAK_RANGE, core.indicator.SIG_SIMPLE_MOVING_AVERAGE):
            if iv.history_param1 is None:
                iv.history_param1 = 30
            del iv.history_param2
        elif sig_type == core.indicator.SIG_DUAL_MOVING_AVERAGE:
            if iv.history_param1 is None:
                iv.history_param1 = 10
            if iv.history_param2 is None:
                iv.history_param2 = 50
                    
    def _validate_indicator(self, i):
        v = self.view
        if i.signal_threshold < 0:
            i.signal_threshold = 0
            v.notify("%s : Signal threshold must be positive" % i.name)
        if i.envelope_factor < 0.0 or i.envelope_factor > 1.0:
            i.envelop_factor = 0.0
            v.notify("%s : Envelope factor must be in [0..1]" % i.name)
        if not i.signaler_type in SIG_TYPES:
            i.signaler_type = core.indicator.SIG_BUY_HOLD
            v.notify("%s : Invalid signaler type" % i.name)
        sig_type = i.signaler_type
        # need one argument
        if sig_type == core.indicator.SIG_BREAK_RANGE or sig_type == core.indicator.SIG_SIMPLE_MOVING_AVERAGE:
            if i.history_param1 < 0:
                i.history_param1 = 30
                v.notify("%s : Chosen signaler needs one positive parameter" % i.name)
        elif sig_type == core.indicator.SIG_DUAL_MOVING_AVERAGE:
            error = False
            if i.history_param2 < 0:
                i.history_param1 = 10
                error = True
            if i.history_param2 < 0:
                i.history_param2 = 50
                error = True
            if error:
                v.notify("%s : Chosen signaler needs two positive parameters" % i.name)


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
            self.view.notify("Error on reading index %s : %r" % (key,e))
            raise
        else:
            index_points = [(idx, price) for idx, (_, price) in enumerate(index)]
            index_line = wx.lib.plot.PolyLine(index_points, legend = "index")
            self.view.canvas.Draw(wx.lib.plot.PlotGraphics([index_line], title = stock_name, xLabel = "", yLabel = "price"))
            
    def draw_plot(self, plot, actor_id):
        '''
        Draw results of pipe processing
        '''
        index_points = []
        lower_points = []
        upper_points = []
        hold_points = []
        short_marker = []
        long_marker = []
        clear_marker = []
        # fill point holder
        for idx, point in enumerate(plot):
            point.context = actor_id
            index_point = (idx, point.price)
            self.append_if_valid(index_points, index_point)
            self.append_if_valid(lower_points, (idx, point.y[core.pipe.KEY_LOWER]))
            self.append_if_valid(upper_points, (idx, point.y[core.pipe.KEY_UPPER]))
            self.append_if_valid(hold_points, (idx, point.y[core.pipe.KEY_HOLD_AT]))
            action = point.y[core.pipe.KEY_ACTION]
            if action == core.pipe.ACTION_CLEAR:
                clear_marker.append(index_point)
            elif action == core.pipe.ACTION_LONG:
                long_marker.append(index_point)
            elif action == core.pipe.ACTION_SHORT:
                short_marker.append(index_point)
        # convert to polylines and markers
        lines = []
        lines.append(wx.lib.plot.PolyLine(index_points, legend = "index"))
        lines.append(wx.lib.plot.PolyLine(lower_points, legend = "lower bound", colour = "red"))
        lines.append(wx.lib.plot.PolyLine(upper_points, legend = "upper bound", colour = "green"))
        #lines.append(wx.lib.plot.PolyLine(hold_points, legend = "held position", colour = "blue"))
        lines.append(wx.lib.plot.PolyMarker(short_marker, legend = "short position", colour = "orange", marker="triangle_down"))
        lines.append(wx.lib.plot.PolyMarker(long_marker, legend = "long position", colour = "violet", marker="triangle"))
        lines.append(wx.lib.plot.PolyMarker(clear_marker, legend = "cleared position", colour = "yellow", marker="cross"))
        # pack
        full_plot = wx.lib.plot.PlotGraphics(lines, xLabel = "", yLabel = "price")
        self.view.canvas.Draw(full_plot)         
    
    def append_if_valid(self, list, point):
        if point[1] is not None:
            list.append(point)
    
    def print_statistics(self, statistics):
        '''
        Print gathered statistics line by line 
        '''
        text = ""
        for stats in statistics:
            text += "Indicator {} :\n".format(stats.name)
            text += "transactions : {} | total yield : {:.2f} <> relative {:.2%}\n".format(stats.tx_count, stats.total_yield, stats.relative_yield, )
            text += "yields : min {:.2f} , max {:.2f} , average {:.2%} | volatility {:.2%}\n".format(stats.min_yield, stats.max_yield, stats.average_yield, stats.volatility)
            text += "{:=^30}\n".format("=")
        self.view.report(text)
        
    