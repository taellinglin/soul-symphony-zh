import sys
from stageflow.core import Stage
from random import randint, choice
from stageflow import Stage

class Intro2(Stage):
    def __init__(self, exit_stage = "main_menu"):
        self.exit_stage = exit_stage
        self.colors = [(1,0,0,1), (0,1,1,1), (1,1,0,1), (1,0,1,1)]
        self.clock = 0
        self.frame_count = 16

    def enter(self, data):
        self.data = data
        print("intro2 Enter")
        base.cam.set_hpr(render, (0,0,0))
        base.cam.set_y(0.5)
        base.cam.set_z(3)
        base.cam.set_h(180)
        base.cam.look_at(render)
        #self.load_room()
        self.text_begin()
        base.camera.set_hpr(0,0,0)
        base.bgm.playMusic('SpiritsMarch', True)
        base.task_mgr.add(self.update, 'update')
        base.accept('escape', sys.exit)
        
        
    def load_room(self):
        self.room = base.loader.loadModel("rooms/room00.bam")
        self.room.set_p(90)
        self.room_texture = base.loader.loadTexture("graphics/mandala00.png")
        self.room.setTexture(self.room_texture, 1)
        self.room.reparent_to(render)
        
    def text_begin(self):
        self.caption = base.loader.loadModel("text_chapters/intro2/frame00.bam")
        self.caption1 = base.loader.loadModel("text_chapters/intro2/frame01.bam")
        self.caption2 = base.loader.loadModel("text_chapters/intro2/frame02.bam")
        self.caption3 = base.loader.loadModel("text_chapters/intro2/frame03.bam")
        self.caption4 = base.loader.loadModel("text_chapters/intro2/frame04.bam")
        self.caption5 = base.loader.loadModel("text_chapters/intro2/frame05.bam")
        self.caption6 = base.loader.loadModel("text_chapters/intro2/frame06.bam")
        self.caption7 = base.loader.loadModel("text_chapters/intro2/frame07.bam")
        self.caption8 = base.loader.loadModel("text_chapters/intro2/frame08.bam")
        self.caption9 = base.loader.loadModel("text_chapters/intro2/frame09.bam")
        self.caption10 = base.loader.loadModel("text_chapters/intro2/frame10.bam")
        self.caption11 = base.loader.loadModel("text_chapters/intro2/frame11.bam")
        self.caption12 = base.loader.loadModel("text_chapters/intro2/frame12.bam")
        self.caption13 = base.loader.loadModel("text_chapters/intro2/frame13.bam")
        self.caption14 = base.loader.loadModel("text_chapters/intro2/frame14.bam")
        self.caption15 = base.loader.loadModel("text_chapters/intro2/frame15.bam")
        self.caption16 = base.loader.loadModel("text_chapters/intro2/frame16.bam")
        
        
        
                
        
        self.frames = [self.caption, 
                       self.caption1,
                       self.caption2,
                       self.caption3,
                       self.caption4,
                       self.caption5,
                       self.caption6, 
                       self.caption7,
                       self.caption8, 
                       self.caption9, 
                       self.caption10, 
                       self.caption11,
                       self.caption12,
                       self.caption13,
                       self.caption14,
                       self.caption15,
                       self.caption16]
        
        for f, frame in enumerate(self.frames):
            frame.set_h(180)
            frame.set_r(0)
            frame.set_p(0)
            frame.set_z(0)
            frame.set_y(-0.1)
            frame.set_scale(0.18,0.18,0.18)
            frame.reparent_to(render)
            frame.set_two_sided(True)
    def update(self, task):
        self.frames[0].set_r(self.frames[0], 0.75)
        for f, frame in enumerate(self.frames):
            frame.hide()
        if(self.clock >= self.frame_count):
            self.clock = 0
            self.exit(self.data)
            self.transition('intro3')
        else:
            self.clock += 0.003
            
        
       
        for f, frame in enumerate(self.frames):
            frame.hide()
            frame.set_color(choice(self.colors))
            #frame.set_h(frame, f+1)
            #frame.set_p(frame, f+1)
            
            for sf, subframe in enumerate(frame.get_children()):
                subframe.set_color(choice(self.colors))
                #subframe.set_r(subframe, sf+1)
                #subframe.set_h(subframe, sf+1)
        self.frames[round(self.clock)].show()
            
        dt = globalClock.get_dt()
        base.cam.look_at(render)
        base.camera.set_r(base.camera, 0)
        for l, line in enumerate(self.caption.get_children()):
            line.set_color(choice(self.colors))
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