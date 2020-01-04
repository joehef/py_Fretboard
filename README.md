
![py Fretboard image](images/pyFretboard.jpg?raw=true "pyFretboard")

##### Python fretboard diagrams for scales and chords

pyFretboard is a utility written in Python to display chord diagrams and scale diagrams of stringed instruments. 

### Features at a glance
- Displays chords and scales from its extensive database including 35 chord qualities, 72 Carnatic Melakarta ragas, 909 Carnatic Janya ragas(ascending and descending) and 43 Non-Indian scales which include the common western scales.
- Includes 9 different commonly used tunings for guitars and stringed instruments like Mandolin, Bouzouki etc.
- Custom tunings are possible and the number of strings can also be changed.
- The images can be saved to “.png” files

#### Dependencies: (Python 3.6 was used)
- tkinter
- Bokeh (1.4 was used)

##### On execution the following window opens
![py Fretboard window image](images/pyfb_win.jpg?raw=true "window")

#### Row 1 Title: 
short text used for naming the HTML file to be displayed
#### Row 2 Tuning dropdown list: 
This is where you select the instruments and tunings available in the database. On selection this would load the tuning into the Text Entry field next to it.
#### Row 2 Tuning Text Entry field: 
For custom tunings and changing the number of strings, you can type in your custom instrument tuning. The number of notes will indicate the number of strings. The permitted values are [ 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B' ]. Spaces or other characters are not allowed, would result in a default tuning being loaded.
#### Row 3 Frets Start / End dropdown lists: 
These selectors determine the part of the fretboard to be displayed. 0 is the neck and the 15th is the last fret available for display. The program increases the last fret value on display if the difference between the two fret numbers is lesser than 3.
#### Row 4 Scales / Chords dropdown list: 
This selector lets you choose from the scales and the chords in the database.
#### Row 4 Scale / Chord Category dropdown list: 
Both scales and chords are divided into sub-categories for ease of use.
##### Scale categories:
- Western (West of India )
- Melakarta (72 primary Carnatic Ragas)
- Janya (906 derived Carnatic Ragas, can have different notes while descending)
##### Chord categories:
- Favorites
- Quality (all)

Note: Ragas are not just a collection of notes but rather a complex set of rules. This program only displays notes.

#### Row 5 Desc dropdown list: 
This works only for scales which have different notes while descending. The scale has to be selected using the left most “Root” and “Scale” selectors. The other Root/Scale selectors will be ignored. If “ignore_desc” is selected the descending part will be ignored and the scale selected using the next set of Root/Scale selectors will be displayed.
Note: up to 2 scales or 3 chords can be displayed together in a page currently.
#### Rows 6 and 7 Root and Scale/Quality dropdown lists: 
There are 3 sets of Root(note) and Scale/Quality selectors.

After all the selections, click on the button “Show” to display “Your Fretboard”, in your browser. 
- The Root notes have a circle around them.
- There are a set of tools to move around the images or zoom in or out.
- PNG files can be saved by clicking on the floppy icon

#### An example Scale Sheet 
(with different descending notes)
![py Fretboard window image](images/pyfb_win.jpg?raw=true "window")
##### Output:
![py Fretboard Output image](images/pyfb_out.jpg?raw=true "Bokeh Out")

#### An example Chord Sheet 
(with different descending notes)
![py Fretboard window 2 image](images/pyfb_win2.jpg?raw=true "window 2")
##### Output:
![py Fretboard Output 2image](images/pyfb_out2.jpg?raw=true "Bokeh Out2")

The window will remain open till you “Close” it.


