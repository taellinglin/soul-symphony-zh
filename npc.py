from panda3d.core import TextNode
from panda3d.core import NodePath
from panda3d.core import TextFont
from panda3d.core import Texture
from panda3d.core import TextureStage
from panda3d.core import CardMaker

from bgm import BGM
from random import choice, shuffle
from dialog import dialog
import glob

names = ["迪米特里",
         "蒙杜",
         "洛基",
         "黄道",
         "普瑞姆",
         "星",
         "沃克",
         "托玛",
         "巴拉科",
         "莫塔利亚",
         "何新",
         "皮克苏",
         "泰",
         "海洋",
         "薇薇安",
         "学者",
         "暴风雨",
         "梦想家",
         "天空",
         "锂",
         "拳击手",
         "布鲁克",
         "法尔戈",
         "士兵",
         "海王星",
         "艾丽塔",
         "泰利",
         "本田",
         "土星",
         "托尔图加"]
used_names = []

class npc():
    
    def __init__(self):
        self.names = names
        self.faces = [
                        base.loader.loadTexture("NPCs/faces/face00.png"),
                        base.loader.loadTexture("NPCs/faces/face01.png"),
                        base.loader.loadTexture("NPCs/faces/face02.png"),
                        base.loader.loadTexture("NPCs/faces/face03.png"),
                        base.loader.loadTexture("NPCs/faces/face04.png"),
                        base.loader.loadTexture("NPCs/faces/face05.png"),
                        base.loader.loadTexture("NPCs/faces/face06.png"),
                        base.loader.loadTexture("NPCs/faces/face07.png"),
                        base.loader.loadTexture("NPCs/faces/face08.png"),
                        base.loader.loadTexture("NPCs/faces/face09.png"),
        ]
        self.emblems = [
                        base.loader.loadTexture("NPCs/emblems/emblem00.png"),
                        base.loader.loadTexture("NPCs/emblems/emblem01.png"),
                        base.loader.loadTexture("NPCs/emblems/emblem02.png"),
        ]
        base.task_mgr.add(self.update, "npc_update")
        self.npc_dialog = dialog()
        self.dialogs = self.npc_dialog.get_dialogs()
        self.id = 0
        
    def load_npc(self):
        
        npcModel = base.loader.loadModel("NPCs/npc01.bam")
        list_copy = self.names.copy()
        shuffle(list_copy)
        if len(list_copy):
            next_random = list_copy.pop()
        else:
            self.dialogs = self.npc_dialog.get_dialogs()
            list_copy = self.dialogs
            next_random = list_copy.pop()
            
        npc = { "name" : next_random,
                "face" : choice(self.faces),
                "emblem" : choice(self.emblems),
        }
        self.nametag = npcModel.find("**/npcNametag")
        self.face = npcModel.find("**/npcFace")
        self.face.set_two_sided(True)
        self.nametag.hide()
        
        self.emblem = npcModel.find("**/npcEmblem")
        self.emblem.set_two_sided(True)
        ts1 = TextureStage('ts1')
        ts2 = TextureStage('ts2')
        for stage in self.face.find_all_texture_stages():
            self.face.set_texture(stage, npc.get("face"), 1)
        for stage in self.emblem.find_all_texture_stages():
            self.emblem.set_texture(stage, npc.get("emblem"), 1)
        self.cm = CardMaker('card')
        self.card = render.attachNewNode(self.cm.generate())
        npc_dialog_text = self.dialogs[self.id]

        # Load a random font
        font_paths = glob.glob("fonts/text/*.ttf")
        font_path = choice(font_paths)
        font = loader.load_font(font_path)

        # Create a TextNode object
        text_node = TextNode("my_text_node")
        text_node.set_font(font)

        # Set the text content
        text_node.set_text(npc_dialog_text)

        new_npc = { "id" : self.id,
                    "name" : npc.get("name"),
                    "nametag" : self.nametag,
                    "face": self.face,
                    "emblem": self.emblem,
                    "model": npcModel,
                    "dialog": npc_dialog_text,
                    "text_node": text_node,
        }
        self.id += 1
        return new_npc
    
    def update(self, task):
        self.face.set_h(self.face, 1)
        self.emblem.set_h(self.emblem, -1)
            
        return task.cont
