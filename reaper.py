
# from https://github.com/teamikl/reascript-latency-compensation/blob/master/rea.py

import sys
from contextlib import contextmanager
from reaper_python import *
from sws_python64 import *

def getScriptPath():
    return sys.path[0]

def command(action):
    RPR_Main_OnCommand(action, 0)

def show_message(msg):
    RPR_ShowConsoleMsg(msg)


class _Pointer:
    def __init__(self, obj):
        self.__obj = obj

    @property
    def obj(self):
        return self.__obj

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, hash(self.obj))

class Source(_Pointer):
    @property
    def type(self):
        return RPR_GetMediaSourceType(self.obj, "", 30)[1]

class MediaItem_Take(_Pointer):
    @property
    def source(self):
        return Source(RPR_GetMediaItemTake_Source(self.obj))

class MediaItem(_Pointer):

    def get(self, name):
        return RPR_GetMediaItemInfo_Value(self.obj, name)
    def set(self, name, value):
        RPR_SetMediaItemInfo_Value(self.obj, name, value)   

    def getPosition(self):
        return RPR_GetMediaItemInfo_Value(self.obj, "D_POSITION")
    def setPosition(self, value):
        RPR_SetMediaItemInfo_Value(self.obj, "D_POSITION", value)
    position = property(getPosition, setPosition)
    
    length = property(lambda self: self.get("D_LENGTH"), 
                   lambda self, v: self.set("D_LENGTH", v))
    
    @property
    def end(self):
        return self.position + self.length 

    def getNote(self):
        return ULT_GetMediaItemNote(self.obj)
    def setNote(self, value):
        ULT_SetMediaItemNote(self.obj, value)
    note = property(getNote, setNote) 


 
    
    @property
    def activeTake(self):
        take = RPR_GetMediaItemTake(self.obj, int(self.get('I_CURTAKE')))
        return MediaItem_Take(take)
    
    

class Track(_Pointer):

    @property
    def name(self):
        return RPR_GetSetMediaTrackInfo_String(self.obj, "P_NAME", "", False)[3]


    @property
    def items_count(self):
        track = self.obj
        return RPR_CountTrackMediaItems(track)

    @property
    def items(self):
        track = self.obj
        # nItems = RPR_GetNumMediaItems(track)
        nItems = self.items_count
        for idx in range(nItems):
            item = RPR_GetTrackMediaItem(track, idx)
            yield MediaItem(item)
    
    @property
    def last_item(self):
         track = self.obj
         item = RPR_GetTrackMediaItem(track, self.items_count-1)
         return MediaItem(item)
     
#    @property
#    def end(self):
#        return self.last_item.end

class Project(_Pointer):

    def __init__(self, project=0):
        """project=0 for current project"""
        #super().__init__(project) # python3 
        _Pointer.__init__(self, project)

    @property
    def path(self):
        return RPR_GetProjectPathEx(self.obj)

    @property
    def tracks(self):
        project = self.obj
        nTracks = RPR_CountTracks(project)
        for idx in range(nTracks):
            track = RPR_GetTrack(project, idx)
            yield Track(track)

    @contextmanager
    def undoable(self, description="", flag=-1):
        project = self.obj
        RPR_Undo_BeginBlock2(project)
        try:
            yield self
        finally:
            RPR_Undo_EndBlock2(project, description, flag)
    
    @property
    def end(self):
        project = self.obj
        return max (
            map(lambda t: t.last_item.end, project.tracks)
        )

def newAction(description, target=0):
    return Project(target).undoable(description)
