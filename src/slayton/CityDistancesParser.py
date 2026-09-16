# Generated from CityDistances.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,4,25,2,0,7,0,2,1,7,1,2,2,7,2,1,0,4,0,8,8,0,11,0,12,0,9,1,1,1,
        1,1,1,3,1,15,8,1,1,1,5,1,18,8,1,10,1,12,1,21,9,1,1,2,1,2,1,2,0,0,
        3,0,2,4,0,0,24,0,7,1,0,0,0,2,11,1,0,0,0,4,22,1,0,0,0,6,8,3,2,1,0,
        7,6,1,0,0,0,8,9,1,0,0,0,9,7,1,0,0,0,9,10,1,0,0,0,10,1,1,0,0,0,11,
        12,3,4,2,0,12,19,5,3,0,0,13,15,5,1,0,0,14,13,1,0,0,0,14,15,1,0,0,
        0,15,16,1,0,0,0,16,18,5,3,0,0,17,14,1,0,0,0,18,21,1,0,0,0,19,17,
        1,0,0,0,19,20,1,0,0,0,20,3,1,0,0,0,21,19,1,0,0,0,22,23,5,2,0,0,23,
        5,1,0,0,0,3,9,14,19
    ]

class CityDistancesParser ( Parser ):

    grammarFileName = "CityDistances.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "','" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "STRING", "NUMBER", "WS" ]

    RULE_table = 0
    RULE_row = 1
    RULE_city = 2

    ruleNames =  [ "table", "row", "city" ]

    EOF = Token.EOF
    T__0=1
    STRING=2
    NUMBER=3
    WS=4

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class TableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def row(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CityDistancesParser.RowContext)
            else:
                return self.getTypedRuleContext(CityDistancesParser.RowContext,i)


        def getRuleIndex(self):
            return CityDistancesParser.RULE_table

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTable" ):
                listener.enterTable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTable" ):
                listener.exitTable(self)




    def table(self):

        localctx = CityDistancesParser.TableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_table)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 7 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 6
                self.row()
                self.state = 9 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==2):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RowContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def city(self):
            return self.getTypedRuleContext(CityDistancesParser.CityContext,0)


        def NUMBER(self, i:int=None):
            if i is None:
                return self.getTokens(CityDistancesParser.NUMBER)
            else:
                return self.getToken(CityDistancesParser.NUMBER, i)

        def getRuleIndex(self):
            return CityDistancesParser.RULE_row

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRow" ):
                listener.enterRow(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRow" ):
                listener.exitRow(self)




    def row(self):

        localctx = CityDistancesParser.RowContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_row)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 11
            self.city()
            self.state = 12
            self.match(CityDistancesParser.NUMBER)
            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==3:
                self.state = 14
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==1:
                    self.state = 13
                    self.match(CityDistancesParser.T__0)


                self.state = 16
                self.match(CityDistancesParser.NUMBER)
                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CityContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(CityDistancesParser.STRING, 0)

        def getRuleIndex(self):
            return CityDistancesParser.RULE_city

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCity" ):
                listener.enterCity(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCity" ):
                listener.exitCity(self)




    def city(self):

        localctx = CityDistancesParser.CityContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_city)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self.match(CityDistancesParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





