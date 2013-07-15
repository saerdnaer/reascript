
import sys
from contextlib import contextmanager
from reaper_python import *

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


class MediaItem(_Pointer):

    def getPosition(self):
        return RPR_GetMediaItemInfo_Value(self.obj, "D_POSITION")
    def setPosition(self, value):
        RPR_SetMediaItemInfo_Value(self.obj, "D_POSITION", value)
    position = property(getPosition, setPosition)


class Track(_Pointer):

    @property
    def name(self):
        return RPR_GetSetMediaTrackInfo_String(self.obj, "P_NAME", "", False)[3]

    @property
    def items(self):
        track = self.obj
        # nItems = RPR_GetNumMediaItems(track)
        nItems = RPR_CountTrackMediaItems(track)
        for idx in range(nItems):
            item = RPR_GetTrackMediaItem(track, idx)
            yield MediaItem(item)


class Project(_Pointer):

    def __init__(self, project=0):
        """project=0 for current project"""
        super().__init__(project)

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


def newTask(description, target=0):
    return Project(target).undoable(description)


def loadTable(filename):
    ms = lambda x: x/1000.0
    samples = lambda samples,khz: ms(samples/khz)
    _trimComment = lambda x: x[:x.index("#")] if "#" in x else x
    return eval('{{{0}}}'.format(
            ",".join( '"{}": {}'.format(*line.strip().split(":",1))
                for line in map(_trimComment,open(filename))
                    if ":" in line and line.strip())))
