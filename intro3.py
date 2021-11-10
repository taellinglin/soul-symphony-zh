import sys
from stageflow.core import Stage
from random import randint, choice
from stageflow import Stage

class Intro3(Stage):
    def __init__(self, exit_stage = "main_menu"):
        self.exit_stage = exit_stage
        self.colors = [(1,0,0,1), (0,1,1,1), (1,1,0,1), (1,0,1,1)]
        self.clock = 0
        self.frame_count = 6

    def enter(self, data):
        self.data = data
        print("intro3 Enter")
        base.cam.set_hpr(render, (0,0,0))
        base.cam.look_at(render)
        base.cam.set_z(128)
        #self.load_room()
        self.text_begin()
        base.camera.set_hpr(0,0,0)
        base.bgm.playMusic(None, True)
        base.task_mgr.add(self.update, 'update')
        base.accept('escape', sys.exit)
        
        
    def load_room(self):
        self.room = base.loader.loadModel("rooms/room00.bam")
        self.room.set_p(90)
        self.room_texture = base.loader.loadTexture("graphics/mandala00.png")
        self.room.setTexture(self.room_texture, 1)
        self.room.reparent_to(render)
        
    def text_begin(self):
        self.caption00 = base.loader.loadModel("text_chapters/intro3/frame00.bam")
        self.caption01 = base.loader.loadModel("text_chapters/intro3/frame01.bam")
        self.caption02 = base.loader.loadModel("text_chapters/intro3/frame03.bam")
        self.caption03 = base.loader.loadModel("text_chapters/intro3/frame04.bam")
        self.caption04 = base.loader.loadModel("text_chapters/intro3/frame04.bam")
        self.caption05 = base.loader.loadModel("text_chapters/intro3/frame05.bam")
        self.caption06 = base.loader.loadModel("text_chapters/intro3/frame06.bam")
        
        
        
        self.frames = [self.caption00, self.caption01, self.caption02, self.caption03, self.caption04, self.caption05, self.caption06]
        
        for f, frame in enumerate(self.frames):
            frame.set_two_sided(True)
            frame.reparent_to(render)
        
        
    def update(self, task):
        for f, frame in enumerate(self.frames):
            frame.hide()
            frame.set_color(choice(self.colors))
            frame.set_h(frame, f+1)
            #frame.set_p(frame, f+1)
            
            for sf, subframe in enumerate(frame.get_children()):
                subframe.set_color(choice(self.colors))
                subframe.set_r(subframe, sf+1)
                subframe.set_h(subframe, sf+1)
                
        if(self.clock >= self.frame_count):
            self.clock = 0
            self.exit(self.data)
            self.transition('room00')
        else:
            self.clock += 0.001
            
        self.frames[round(self.clock)].show()
       

        dt = globalClock.get_dt()
        base.cam.look_at(render)
        base.camera.set_r(base.camera, 0)
        return task.cont
    
    def transition(self, exit_stage):
        if exit_stage == None:
            self.exit_stage = 'main_menu'
        else:
            self.exit_stage = exit_stage    
        base.flow.transition(self.exit_stage)
        
    def exit(self, data):
        for f, frame in enumerate(self.frames):
            frame.detachNode()
        #self.room.detachNode()
        base.bgm.stopMusic()
        base.taskMgr.remove('update')
        return data