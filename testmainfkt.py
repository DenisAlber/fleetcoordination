#from zumi.zumi import Zumi
import time
from Graph_Library import Graph as gr
import personalmap as pm

zumimap = gr()

zumimap = pm.initPersonalMap(zumimap)
zumimap.PrintAllCrossingNamesAndReachableCrossings()
