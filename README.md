my READMEs are not normaly like this, just an fyi, also I still need to get spellcheck installed on my IDE
as of right now, this can't tell if someone has keysmashed or not. it also can't give zappies, i wont be able to test that till I get my PiShock either, but the PiShock api seems to be stright forward

I have stuff from oxford 5000, corncobs misspelling list, 
keysmashes were made from https://github.com/galenguyer/galenguyer.github.io.v1/blob/7bac2fa62bf89dd97e4321faa745bf3fd2a08c06/keysmash.html

this came out of a converstion in the [PiShock (18+)](https://pishock.com) Discord, 

where someone told me to make a keysmash sensor that would shock me when I keysmash.

this was a joke, why did I actualy decide to do this... 
help.


I need a better dataset as well, that or the algthoerm im using isnt right for this.

# IGNORE ALL BELOW FOR  NOW! THIS IS THE KERAS BRANCH! BASED ON https://towardsdatascience.com/character-level-cnn-with-keras-50391c3adf33


note that if you get 
```ValueError: np.nan is an invalid document, expected byte or unicode string.```
when running train.py
check to see if you have any of the following in any of the datasets coulumes, if you do, remove that line from it.

```
#N/A
#N/A N/A
#NA
-1.#IND
-1.#QNAN
-NaN
-nan
1.#IND
1.#QNAN
<NA>
N/A
NA
NULL
NaN
n/a
nan
null
```

```notsmash,null,,,``` would cause an error but ```notsmash,nulled``` would not

