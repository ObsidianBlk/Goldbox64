# Goldbox 64
Written for the (LOWREZJAM 2018)[https://itch.io/jam/lowrezjam-2018], Goldbox64 was intended as a 1980s SSI Goldbox RPG styled game. Sadly, I never got to writting the game portion of the project. As it stands, this is an editor which allows the user to make a map with three different wall sets. These maps can be loaded and saved, but not much else.

Goldbox 64 is written in Python (3.6.6) using the PyGame library (1.9.4).

## Controls
### Main Menu
* w - Move up an option
* s - Move down an option
* enter/return - Select highlighted option
* escape - Quit

### Editor
* w - Move Forward
* s - Move Backward
* d - Turns Right
* a - Turn Left
* q - Select previous wall index (output to terminal)
* e - Select next wall index (output to terminal)
* spacebar - Place wall
* o - Save map
* l - Load map
* escape - (When saving/loading) Cancels operation, otherwise quit to Main Menu
* enter/return - (When saving/loading) Saves/loads the map to/from the entered name.

When saving or loading, it will initially appear as if nothing happened, but upon entering keys you will see their output display at the top of the screen. This is intended to be the file name.
__NOTE:__ There is no filter for bad filenames and some characters will not display (such as spaces) even though they are valid names.

All maps are saved in the maps folder.


## License
I release this under the MIT license. 
