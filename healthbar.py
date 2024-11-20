from panda3d.core import NodePath, CardMaker, Vec4
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

class HealthBar(DirectObject):
    def __init__(self, parent=None, max_health=100, height=0.025, position=(-2, 0, 1 - 0.025)):  # Positioned at the top
        self.max_health = max_health
        self.current_health = max_health
        self.height = height
        self.position = position
        self.colors = [
            Vec4(1, 0, 0, 0.5),
            Vec4(1, 0.5, 0, 0.5),
            Vec4(1, 1, 0, 0.5),
            Vec4(0, 1, 0, 0.5),
            Vec4(0, 0, 1, 0.5),
            Vec4(0.3, 0, 0.5, 0.5),
            Vec4(0.5, 0, 1, 0.5)
        ]
        self.current_color_index = 0

        self.root = NodePath("HealthBar")
        self.root.reparent_to(parent if parent else base.aspect2d)

        # Background bar (oversized full width for dynamic stretch)
        self.bg_bar = self.create_bar(Vec4(0.2, 0.2, 0.2, 1), 4, height)
        self.bg_bar.reparent_to(self.root)
        self.bg_bar.set_pos(*position)

        # Foreground bar (health-based width)
        self.fg_bar = self.create_bar(Vec4(0, 1, 0, 1), 4, height)
        self.fg_bar.reparent_to(self.root)
        self.fg_bar.set_pos(*position)

        # Update the health bar color based on the current health
        self.update_health(self.current_health)

        # Start cycling colors periodically based on task or health change
        taskMgr.add(self.cycle_colors, "CycleColors")

    def create_bar(self, color, width, height):
        cm = CardMaker("Bar")
        cm.set_frame(0, width, 0, height)
        bar = NodePath(cm.generate())
        bar.set_color(color)
        bar.set_scale(1, 1, 1)
        return bar

    def update_health(self, new_health):
        """Update the health and adjust bar size and color accordingly."""
        self.current_health = max(0, min(self.max_health, new_health))
        health_ratio = self.current_health / self.max_health

        # Update foreground bar scale (width)
        new_width = 4 * health_ratio  # Shrink the foreground bar horizontally
        self.fg_bar.set_scale(new_width, 1, 1)

        # Change color based on health ratio (red for low health, green for full)
        if health_ratio <= 0.2:
            self.fg_bar.set_color(Vec4(1, 0, 0, 0.5))  # Red for low health
        elif health_ratio <= 0.5:
            self.fg_bar.set_color(Vec4(1, 1, 0, 0.5))  # Yellow for mid-health
        else:
            self.fg_bar.set_color(Vec4(0, 1, 0, 0.5))  # Green for high health

        # Adjust position (optional, based on your UI layout)
        self.fg_bar.set_pos(self.position[0] + (4 - new_width), self.position[1], self.position[2])  # Align left

    def cycle_colors(self, task):
        """Optional color cycling effect (periodic updates)."""
        if task.time % 1.0 < 0.1:  # Update color every second (or adjust for faster/slower cycling)
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.fg_bar.set_color(self.colors[self.current_color_index])
        return Task.cont
