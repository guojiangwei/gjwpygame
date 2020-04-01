## design
status of a game:  
init
start
reset
stop  
stop:0(terminal) stop:1(succell) stop:2(failed) stop:3
### mygame_framework 
1,  AbstractGame  
attribute  
function  
2,  AbstractGamePanel  
attribute  
function  
3,  AbstractScoreBoard  
attribute  
function  

## The main process of Russia box 
### What should be done
####  the game starts

####  the game resets

####  game over

####  game stop

## how to add a new game 
from mygame_framework import *

### 1,AbstractGame
these var must be init in when init a instance  
        self.sb = None  
        self.game_panel = None  
        self.game_result = None
### 2,AbstractGamePanel
### 3,AbstractScoreBoard
### 4,GameResult(Panel):
