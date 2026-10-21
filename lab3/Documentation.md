The program reads the token list from tokens.json and the source program from a file.
It uses Python regular expressions to recognize keywords, identifiers, integer constants, operators, and separators, while ignoring whitespace.
Identifiers and constants are stored once in a custom hash table, where collisions are handled using lists and repeated symbols keep the same position.
The PIF records each token code and its symbol-table position, using -1 for keywords, operators, and separators.
The program saves the PIF in pif.txt, the symbol table in st.txt, and invalid tokens with their line and column in errors.txt.
