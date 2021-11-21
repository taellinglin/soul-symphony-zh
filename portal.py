from direct.showbase.Loader import Loader


from audio3d import audio3d

class Portal():
    
    def __init__(self):
        self.model = base.loader.loadModel('components/portal.bam')
        self.audio3d = audio3d()
        self.portal_loops = self.audio3d.sfx3d.get('portal_loop')
        
    def warp(self):
        
        
    def update(self, task):
        