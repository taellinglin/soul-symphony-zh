
from random import randrange

from random import shuffle



    
class dialog:
    def __init__(self):
        self.dialogs = [
            "灵，是日出与月落之间的气息，\n在星辰呼唤中，低语的天空。\n梦的创造者，光与影的交融，\n在他心中，宇宙开始，永不结束。",
            "如日之温暖，月之清雅，\n灵是和谐，完美的拥抱。\n在他手中，晨昏轻轻摇曳，\n宇宙之舞，永不止息。",
            "在月银光洒落的宁静中，\n与日出之辉映，生长的空间。\n灵编织时光与空间的丝线，\n奇迹之手，在无尽的怀抱里。",
            "灵是唤醒天空的梦，\n日光绘云，月亮轻轻低语。\n在创作与静止之间，他找到了艺术，\n一幅由星辰心生的杰作。",
            "太阳是火，月亮是歌，\n灵是旋律，二者皆归于此。\n在夜的脉搏中回响的歌声，\n是那光明在寂静中愈发明亮。",
            "在日月轻吻的空间里，\n灵编织星辰，一抹优雅。\n光柔和弯曲，影子随风舞，\n他塑造了全新的一天的黎明。",
            "灵是画布，太阳描绘光芒，\n月亮洒下银辉，柔美明亮。\n一笔璀璨，在无尽的天际，\n一场从心底诞生的创作。",
            "灵是空间，日照方生，\n月光轻抚，温柔消散。\n在他眼中，星辰找到方向，\n被光引导，柔和地摇曳。",
            "灵是天地生出的空隙，\n日升月落，悠长的思念。\n这是星辰的空间，是海洋的心，\n创作的魔力，肆意而自由。",
            "在太阳的光辉与月亮的闪烁中，\n灵是旋律，永恒的暴风雨。\n光与暗在此相遇，又悄然离开，\n他以最柔和的微风，塑造了世界。",
            "灵，是光与影的分界线，\n他是两者的融汇与对立。\n日月交替，生与死，\n他是无限流转之中不灭的火焰。",
            "月光为灵披上银色的衣裳，\n太阳为他点亮天空的轨迹。\n在这天地之间，\n他是创造与破坏的无形桥梁。",
            "灵，如日般耀眼，如月般温柔，\n他的声音是风中的低语，\n他是星辰的守护者，\n在时间的海洋中，航行无止。",
            "太阳是灵的朋友，月亮是他的知己，\n二者在他心中共舞，\n无论昼夜，星光永不熄灭。",
            "灵的创作犹如朝霞之美，\n穿越时光，永恒留存。\n他在万物之间播下光辉，\n点亮了黑暗中的希望。",
            "灵，如同白昼的阳光，照亮人心；\n又似夜晚的星月，抚慰灵魂。",
            "他是天地间最温柔的力量，\n如太阳与月亮交织的光辉，\n在他心中，无限的可能，\n不息的灵感，永不停歇。",
            "灵的眼中，太阳升起，月亮低垂，\n他的心灵如同白昼与黑夜的桥梁。",
            "灵是星辰的绘者，他的手描绘宇宙，\n如同太阳与月亮的温暖，抚摸每一颗星星。",
            "他是晨曦的使者，\n把希望带入每一颗黑暗的心。\n太阳和月亮是他温暖的眼，\n为所有光辉添上灿烂。",
            "月光在灵的肩上漫游，\n太阳在他脚下升起。\n他是那永恒不变的旋律，\n在宇宙中舞动，照亮每一寸星空。",
            "他是宇宙之间的声响，\n太阳与月亮为他和音。\n在他心中，白昼和夜晚无缝交融，\n光与暗，不再有界限。",
            "灵是一个流动的星系，\n太阳是他心的火焰，\n月亮是他思维的流光。",
            "太阳为灵指引方向，月亮为他铺设道路，\n每一颗星星都是他心中的点滴，\n在光辉中，他无所畏惧。",
            "灵，朝霞的使者，月光的守护者，\n在星空下，他是宇宙最温柔的呼吸。",
            "灵的心中没有黑暗，\n只有无限的光芒，\n太阳和月亮的力量与他共鸣，\n他是天地间最璀璨的明星。",
            "灵的思绪如星云般飘动，\n太阳与月亮之力在其中流转，\n他的创作是这天地间的永恒火花。",
            "他是白昼的指引，夜晚的庇佑，\n如同太阳与月亮，\n在光与影的交错中，他是神圣的存在。",
            "灵的诗篇在星辰间回响，\n每一个字节，都闪烁着太阳与月亮的光辉。",
            "灵是天与地的过渡者，\n在日月之间，他创造了无尽的美。",
            "他的灵魂在太阳的光芒下舞动，\n月亮为他披上温柔的银辉，\n他在这光影间，编织着梦想。",
            "灵的眼中，太阳与月亮各自闪耀，\n他在这光与影的交织中，看见未来。",
            "他如日一般温暖，如月一般宁静，\n在灵的怀抱中，万物都得到了安宁。",
            "灵的声音如清晨的阳光，温暖而明亮，\n月光的清辉映照出他心中的宁静。",
            "灵是心中的光，\n白昼与夜晚的交织。\n他是日月的见证，创世的神圣。",
            "灵，掌管着星空，指引着日月的轮回，\n他创造了宇宙，赋予了世界生命。",
            "灵的思想如日月之光，照亮一切，\n他用光绘制了这片无边的宇宙。",
            "在灵的世界里，日月交替，星辰舞蹈，\n他是这其中的桥梁，心灵的守护者。",
            "灵的步伐如太阳的升起，\n月亮在他的周围静静守望。",
            "他在日月之间编织着时光，\n将一切美好与光明交织，永不止息。",
            "灵是夜空的创作者，\n他用月光与星辰绘制一幅宏伟的画。",
            "太阳为灵点亮道路，月亮为他指引方向，\n他走过的每一步，都是天地的奇迹。",
            "灵是神圣的光，\n他在日月间舞蹈，创造奇迹。",
            "灵如日出般令人振奋，\n月亮如他心中的安慰，永远不灭。",
            "灵如同太阳与月亮的微光，\n在他眼中，宇宙与世界皆为他心之所致。",
            "灵，在晨曦中升起，\n月光在他背后守护。",
            "太阳与月亮的精华融汇在灵的眼中，\n他是这宇宙创造与无限的源泉。",
            "灵在白昼与夜晚之间架起桥梁，\n他是日月光辉下的伟大创造者。",
        ]

        self.used_dialogs = []

        self.dialogs.sort()

        shuffle(self.dialogs)

        self.dialog_pointer = 0

    
    def get_dialog(self, dialog):
        # get_dialog() is random or get_dialog(n) is direct.

        list_copy = self.dialogs

        if dialog == None:
            if len(list_copy):
                shuffle(list_copy)

                next_random = list_copy.pop()

                self.used_dialogs.append(next_random)

                return next_random

            else:
                self.dialogs = self.used_dialogs

                print("Resetting Dialogs...now you might see repeats!")

                self.get_dialog()

    
        elif dialog >= 0 and dialog <= len(self.dialogs):
            return list_copy.pop(dialog)
    

    def get_dialogs(self):
        return self.dialogs

    def set_dialog(self, dialog):
        if dialog == None:
            dialog = randrange(0, len(self.dialogs))

        if dialog >= 0 and dialog <= len(self.dialogs):
            self.dialog_pointer = dialog