grammar CityDistances;

// Parser

table
    : row+;

row
    : city NUMBER (','? NUMBER)*;

city
    : STRING;



// Lexer

STRING
    : '"' DOUBLE_QUOTE_CHAR* '"'
    | '\'' SINGLE_QUOTE_CHAR* '\''
    ;

NUMBER
    : INT ('.' INT*)?
    ;

fragment INT
    : '0'
    | [1-9] [0-9]*
    ;

fragment DOUBLE_QUOTE_CHAR
    : ~["\\\r\n]
    | '\\u' HEX HEX HEX HEX
    ;

fragment SINGLE_QUOTE_CHAR
    : ~['\\\r\n]
    | '\\u' HEX HEX HEX HEX
    ;

fragment UNICODE_SEQUENCE
    : '\\u' HEX HEX HEX HEX
    ;

fragment HEX
    : [0-9a-fA-F]
    ;

WS
    : [ \t\n\r\u00A0\uFEFF\u2003]+ -> skip
    ;
