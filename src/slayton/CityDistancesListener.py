# Generated from CityDistances.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CityDistancesParser import CityDistancesParser
else:
    from CityDistancesParser import CityDistancesParser

# This class defines a complete listener for a parse tree produced by CityDistancesParser.
class CityDistancesListener(ParseTreeListener):

    # Enter a parse tree produced by CityDistancesParser#table.
    def enterTable(self, ctx:CityDistancesParser.TableContext):
        pass

    # Exit a parse tree produced by CityDistancesParser#table.
    def exitTable(self, ctx:CityDistancesParser.TableContext):
        pass


    # Enter a parse tree produced by CityDistancesParser#row.
    def enterRow(self, ctx:CityDistancesParser.RowContext):
        pass

    # Exit a parse tree produced by CityDistancesParser#row.
    def exitRow(self, ctx:CityDistancesParser.RowContext):
        pass


    # Enter a parse tree produced by CityDistancesParser#city.
    def enterCity(self, ctx:CityDistancesParser.CityContext):
        pass

    # Exit a parse tree produced by CityDistancesParser#city.
    def exitCity(self, ctx:CityDistancesParser.CityContext):
        pass



del CityDistancesParser