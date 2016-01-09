# reascript
Collection of Reaper scripts

# Installation

Run in terminal
```
cd "~/Library/Application Support/REAPER/Scripts"
git clone https://github.com/saerdnaer/reascript.git .
```

# Usage

**Warning: This is script is still in alpha phase.** *I don't know/have not tested yet how to export the slides from reaper again. ;-)*

See Screencast: https://youtu.be/Z6z7e-62Rdg 

[![Screencast](http://img.youtube.com/vi/Z6z7e-62Rdg/0.jpg)](http://www.youtube.com/watch?v=Z6z7e-62Rdg)

* create Reaper project file and add your audio track
* add empty track called 'Slides' 
* convert your slide to one image (e.g. png file) per slide
* drag and drop these images into the slide track 
* open menu 'Actions' -> 'Show Action list…'
* click ReaScript button 'Load…'
* select 'ultraschall_andi_slides.py'
* click ReaScript button 'Edit…'
* click Start script
* fix slides allignment how you need it... notice the two different ways!
* comment `distribute_slide_items()` and uncomment `cleanup_slides()`
* save changes with cmd+S (reaper runs the script automatically)

If something goes wrong just use the undo feature of Reaper.

