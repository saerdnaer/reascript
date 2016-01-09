#!/usr/bin/env python3

from reaper import newAction, show_message

def print(s):
  show_message(s)
  show_message("\n")


def find_slide_track(project):
    for track in project.tracks:
        if track.name == "Slides":
            return track
    return None


def cleanup_slides():
    with newAction("Cleanup slide items") as project:
        track = find_slide_track(project)
        prev_item = None
        for item in track.items:
            # Ensure that the slide is looped until the end of it's item
            item.set("B_LOOPSRC", True)
            #print(item.activeTake.source.type)
              
            if prev_item is not None:                
                # if items are not connected with each other, make previous item longer to fill the gap
                if prev_item.end < item.position:
                    prev_item.length = item.position - prev_item.position
              
            prev_item = item


def distribute_slide_items():
    with newAction("Distribute slide items") as project:
        slide_track = find_slide_track(project)
  
        total_length = project.end
        new_item_length = total_length/slide_track.items_count
        
        pos = 0
        
        # store items to list, because we will do nasty things with them 
        # (items will be temporary out of order during the loop iteration)
        items = list(slide_track.items)
        
        for item in items:
            # Ensure that the slide is looped until the end of it's item
            item.set("B_LOOPSRC", True)
                        
            item.position = pos
            item.length = new_item_length
            pos += new_item_length
 
 
 
             
if __name__ == "__main__":
    distribute_slide_items()
    #cleanup_slides()
