How to use conlleval.pl?
 - perl conlleval.pl -d "\t" <   <crf++-output-file>

What orthographic features do we use?
 - Column 0: token itself
 - C1: token in lower case
 - C2: prefix 1
 - C3: prefix 2
 - C4: prefix 3
 - C5: suffix 1
 - C6: suffix 2
 - C7: suffix 3
 - C8: initial cap
 - C9: all cap
 - C10: has digit
 - C11: has dot
 - C12: has both digit and dot
 - C13: has () at the end
 - C14: has underscore
 - C15: has Cap inside
 - C16: has dash
 - C17~C21: word clustering features
