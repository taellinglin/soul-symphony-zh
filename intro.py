import sys
from stageflow.core import Stage
from random import randint, choice
from stageflow import Stage

class Intro(Stage):
    def __init__(self, exit_stage = "main_menu"):
        self.exit_stage = exit_stage
        self.colors = [(1,0,0,1), (0,1,1,1), (1,1,0,1), (1,0,1,1)]
        self.clock = 0
        self.frame_count = 7

    def enter(self, data):
        self.data = data
        print("intro Enter")
        base.cam.set_hpr(render, (0,0,0))
        base.cam.set_y(0.5)
        base.cam.set_z(3)
        base.cam.set_p(180)
        base.cam.look_at(render)
        #self.load_room()
        self.text_begin()
        base.camera.set_hpr(0,0,0)
        base.bgm.playMusic('TheSpiritsTwo', True)
        base.task_mgr.add(self.update, 'update')
        base.accept('escape', sys.exit)
        
        
    def load_room(self):
        self.room = base.loader.loadModel("rooms/room00.bam")
        self.room.set_p(90)
        self.room_texture = base.loader.loadTexture("graphics/mandala00.png")
        self.room.setTexture(self.room_texture, 1)
        self.room.reparent_to(render)
        
    def text_begin(self):
        self.caption = base.loader.loadModel("text_chapters/chapter00/frame00.bam")
        self.caption1 = base.loader.loadModel("text_chapters/chapter00/frame01.bam")
        self.caption2 = base.loader.loadModel("text_chapters/chapter00/frame02.bam")
        self.caption3 = base.loader.loadModel("text_chapters/chapter00/frame03.bam")
        self.caption4 = base.loader.loadModel("text_chapters/chapter00/frame04.bam")
        self.caption5 = base.loader.loadModel("text_chapters/chapter00/frame05.bam")
        self.caption6 = base.loader.loadModel("text_chapters/chapter00/frame06.bam")
        self.caption7 = base.loader.loadModel("text_chapters/chapter00/frame07.bam")
        
        self.caption.set_h(180)
        self.caption1.set_h(180)
        self.caption2.set_h(180)
        self.caption3.set_h(180)
        self.caption4.set_h(180)
        self.caption5.set_h(180)
        self.caption6.set_h(180)
        self.caption7.set_h(180)
        
        self.caption.set_r(0)
        self.caption1.set_r(0)
        self.caption2.set_r(0)
        self.caption3.set_r(0)
        self.caption4.set_r(0)
        self.caption5.set_r(0)
        self.caption6.set_r(0)
        self.caption7.set_r(0)
        
        self.caption.set_p(0)
        self.caption1.set_p(0)
        self.caption2.set_p(0)
        self.caption3.set_p(0)
        self.caption4.set_p(0)
        self.caption5.set_p(0)
        self.caption6.set_p(0)
        self.caption7.set_p(0)
        
        self.caption.set_z(0)
        self.caption1.set_z(0)
        self.caption2.set_z(0)
        self.caption3.set_z(0)
        self.caption4.set_z(0)
        self.caption5.set_z(0)
        self.caption6.set_z(0)
        self.caption7.set_z(0)
        
        self.caption.set_y(-0.1)
        self.caption1.set_y(-0.1)
        self.caption2.set_y(-0.1)
        self.caption3.set_y(-0.1)
        self.caption4.set_y(-0.1)
        self.caption5.set_y(-0.1)
        self.caption6.set_y(-0.1)
        self.caption7.set_y(-0.1)
                           
        self.caption.set_scale(0.18,0.18,0.18)
        self.caption1.set_scale(0.18,0.18,0.18)
        self.caption2.set_scale(0.18,0.18,0.18)
        self.caption3.set_scale(0.18,0.18,0.18)
        self.caption4.set_scale(0.18,0.18,0.18)
        self.caption5.set_scale(0.18,0.18,0.18)
        self.caption6.set_scale(0.18,0.18,0.18)
        self.caption7.set_scale(0.18,0.18,0.18)
        
        self.caption.reparent_to(render)
        self.caption1.reparent_to(render)
        self.caption2.reparent_to(render)
        self.caption3.reparent_to(render)
        self.caption4.reparent_to(render)
        self.caption5.reparent_to(render)
        self.caption6.reparent_to(render)
        self.caption7.reparent_to(render)
        
        self.caption.set_two_sided(True)
        self.caption1.set_two_sided(True)
        self.caption2.set_two_sided(True)
        self.caption3.set_two_sided(True)
        self.caption4.set_two_sided(True)
        self.caption5.set_two_sided(True)
        self.caption6.set_two_sided(True)
        self.caption7.set_two_sided(True)
        
        self.frames = [self.caption,self.caption1,self.caption2,self.caption3,self.caption4,self.caption5,self.caption6, self.caption7]
        
    def update(self, task):
        for f, frame in enumerate(self.frames):
            frame.hide()
        if(self.clock >= self.frame_count):
            self.clock = 0
            self.exit(self.data)
            self.transition('intro2')
        else:
            self.clock += 0.005
            
        self.frames[round(self.clock)].show()
       
        for c, caption in enumerate(self.caption4.get_children()):
            caption.set_color(choice(self.colors))
            caption.set_r(caption, 0.5*c)
            
        for c, caption in enumerate(self.caption3.get_children()):
            caption.set_color(choice(self.colors))
            #caption.set_r(caption, 0.5*c)
            
        for c, caption in enumerate(self.caption2.get_children()):
            caption.set_color(choice(self.colors))
            caption.set_r(caption, 0.5)
        for c, caption in enumerate(self.caption5.get_children()):
            caption.set_color(choice(self.colors))
            caption.set_r(caption, 0.5*c)
        for c, caption in enumerate(self.caption6.get_children()):
            caption.set_color(choice(self.colors))
            caption.set_r(caption, 0.5)
        for c, caption in enumerate(self.caption7.get_children()):
            caption.set_color(choice(self.colors))
            caption.set_p(caption, -3)
            caption.show()
            
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
        self.caption.detachNode()
        self.caption1.detachNode()
        self.caption2.detachNode()
        self.caption3.detachNode()
        self.caption4.detachNode()
        self.caption5.detachNode()
        self.caption6.detachNode()
        self.caption7.detachNode()

        #self.room.detachNode()
        base.bgm.stopMusic()
        base.taskMgr.remove('update')
        return data