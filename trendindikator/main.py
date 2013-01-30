'''
Created on Jan 30, 2013

@author: Pyranja
'''
import os
import gui.presenter
import test.mock_view

from core.index import CsvRepository

if __name__ == '__main__':
    try:
        repo = CsvRepository(os.getcwd())
        view = test.mock_view.MockView()
        graph_view = test.mock_view.GraphView()
        graph_presenter = gui.presenter.GraphPresenter(graph_view, repo)
        main_presenter = gui.presenter.SettingsPresenter(view, graph_presenter, repo)
        main_presenter.validate_view()
        main_presenter.invoke_pipe()
        main_presenter.update_index()
    finally:
        repo.clear()    # clean up!