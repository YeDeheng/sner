How to use conlleval.pl?
 - perl conlleval.pl -d "\t" <   <crf++-output-file>

What orthographic features do we use?
 - Column 0: token itself
 - C1: token in lower case
 - C2: token in upper case
 - C3: prefix 1
 - C4: prefix 2
 - C5: prefix 3
 - C6: suffix 1
 - C7: suffix 2
 - C8: suffix 3
 - C9: initial cap
 - C10: all cap
 - C11: has digit
 - C12: has dot
 - C13: has both digit and dot
 - C14: has () at the end
 - C15: has underscore
 - C16: has Cap inside
 - C17: has dash
 - C18~C27: word clustering features
 - C28: isAndroidClass
 - C29: isPlatform
 - C30: isFram
