import networkx as nx
import graph_tool.all as gt
import numpy as np
from matplotlib import pyplot as plt

class sbm:
    
    def __init__(self, graph):
        
        self.g = graph
        
    def fitSBM(self, deg_corr_1 = False, verbose_1 = False, wait_1 = 10, nbreaks_1 = 2, n = 10, verbose_2 = False):
        """
        Fit a nested SBM to graph
        Pass arguments to graph-tools minimize_nested_blockmodel_dl
        """
        
        state = gt.minimize_nested_blockmodel_dl(self.g,deg_corr = deg_corr_1,verbose = verbose_1, 
                                           mcmc_equilibrate_args = dict(wait = wait_1, nbreaks = nbreaks_1, 
                                                                        mcmc_args = dict(niter = n), verbose = verbose_2))
        return state
        
    def blackAssignment(self, state):
        """
        After fitting SBM to graph, take output from fitSBM() to get block assignment
        for each node
        """
    
        return state.get_bs()
        
    def sbmplot(self,state):
        
        state.draw(edge_color = gt.prop_to_size(graph.ep.weight, power = 1, log = True), ecmap = (plt.cm.inferno, .6),
             eorder = graph.ep.weight, edge_pen_width = gt.prop_to_size(graph.ep.weight,1,4,power = 1, log = True),
             edge_gradient = [])
    
    def sbmHeatMap(self, state, level):
        
        s = state.get_levels()[level].get_matrix()
        plt.matshow(s.todense())
        plt.colorbar()
        
    def sbmEntropy(self, state):
        return state.entropy()