"""
Path utilities for Om Sans font generation.
Provides quadratic bezier paths for TrueType and exact degree-elevated cubic paths for OpenType CFF.
"""

import math

class Path:
    def __init__(self):
        self.commands = []
        self.current_point = (0.0, 0.0)
        self.start_point = (0.0, 0.0)

    def move_to(self, x, y):
        p = (float(round(x, 2)), float(round(y, 2)))
        self.commands.append(('move', p))
        self.current_point = p
        self.start_point = p
        return self

    def line_to(self, x, y):
        p = (float(round(x, 2)), float(round(y, 2)))
        self.commands.append(('line', p))
        self.current_point = p
        return self

    def quad_to(self, cx, cy, x, y):
        ctrl = (float(round(cx, 2)), float(round(cy, 2)))
        p = (float(round(x, 2)), float(round(y, 2)))
        self.commands.append(('quad', ctrl, p))
        self.current_point = p
        return self

    def close(self):
        self.commands.append(('close',))
        self.current_point = self.start_point
        return self

    def arc_to(self, cx, cy, rx, ry, a_start, a_end, clockwise=True, steps=None):
        """
        Draw an arc along an ellipse centered at (cx, cy) with radii (rx, ry).
        Using fixed steps ensures strictly identical point counts across masters.
        """
        if clockwise:
            sweep = (a_start - a_end) % 360.0
            if sweep == 0:
                sweep = 360.0
        else:
            sweep = (a_end - a_start) % 360.0
            if sweep == 0:
                sweep = 360.0

        if steps is None:
            steps = max(1, int(math.ceil(sweep / 45.0)))

        step_angle = sweep / steps
        for i in range(steps):
            if clockwise:
                a0 = math.radians(a_start - i * step_angle)
                a1 = math.radians(a_start - (i + 1) * step_angle)
            else:
                a0 = math.radians(a_start + i * step_angle)
                a1 = math.radians(a_start + (i + 1) * step_angle)
            amid = (a0 + a1) / 2.0
            delta = abs(a1 - a0) / 2.0
            rx_c = rx / math.cos(delta)
            ry_c = ry / math.cos(delta)
            ctrl = (cx + rx_c * math.cos(amid), cy + ry_c * math.sin(amid))
            end = (cx + rx * math.cos(a1), cy + ry * math.sin(a1))
            self.quad_to(ctrl[0], ctrl[1], end[0], end[1])
        return self

    def circle(self, cx, cy, r, clockwise=True):
        """Draw an 8-segment quadratic circle with guaranteed constant point count."""
        self.move_to(cx + r, cy)
        self.arc_to(cx, cy, r, r, 0, 360, clockwise=clockwise, steps=8)
        self.close()
        return self

    def ellipse(self, cx, cy, rx, ry, clockwise=True):
        """Draw an 8-segment quadratic ellipse with guaranteed constant point count."""
        self.move_to(cx + rx, cy)
        self.arc_to(cx, cy, rx, ry, 0, 360, clockwise=clockwise, steps=8)
        self.close()
        return self

    def donut(self, cx, cy, rx_out, ry_out, rx_in, ry_in):
        """Draw an outer clockwise ellipse and an inner counter-clockwise ellipse."""
        # Outer
        self.move_to(cx + rx_out, cy)
        self.arc_to(cx, cy, rx_out, ry_out, 0, 360, clockwise=True, steps=8)
        self.close()
        # Inner
        self.move_to(cx + rx_in, cy)
        self.arc_to(cx, cy, rx_in, ry_in, 0, 360, clockwise=False, steps=8)
        self.close()
        return self

    def rect(self, x, y, w, h):
        """Draw a rectangular contour clockwise."""
        self.move_to(x, y)
        self.line_to(x, y + h)
        self.line_to(x + w, y + h)
        self.line_to(x + w, y)
        self.close()
        return self

    def draw_to_tt_pen(self, pen):
        """Send quadratic commands to a TrueType GlyphPen."""
        for cmd in self.commands:
            op = cmd[0]
            if op == 'move':
                pen.moveTo(cmd[1])
            elif op == 'line':
                pen.lineTo(cmd[1])
            elif op == 'quad':
                pen.qCurveTo(cmd[1], cmd[2])
            elif op == 'close':
                pen.closePath()

    def draw_to_t2_pen(self, pen):
        """Send exact degree-elevated cubic commands to an OpenType CFF T2CharStringPen."""
        curr = (0.0, 0.0)
        for cmd in self.commands:
            op = cmd[0]
            if op == 'move':
                pen.moveTo(cmd[1])
                curr = cmd[1]
            elif op == 'line':
                pen.lineTo(cmd[1])
                curr = cmd[1]
            elif op == 'quad':
                ctrl = cmd[1]
                p2 = cmd[2]
                c1 = (curr[0] + 2.0 / 3.0 * (ctrl[0] - curr[0]), curr[1] + 2.0 / 3.0 * (ctrl[1] - curr[1]))
                c2 = (p2[0] + 2.0 / 3.0 * (ctrl[0] - p2[0]), p2[1] + 2.0 / 3.0 * (ctrl[1] - p2[1]))
                pen.curveTo(c1, c2, p2)
                curr = p2
            elif op == 'close':
                pen.closePath()


class GlyphSpec:
    def __init__(self, name, unicode_val, advance_width, lsb, paths=None):
        self.name = name
        self.unicode_val = unicode_val
        self.advance_width = int(round(advance_width))
        self.lsb = int(round(lsb))
        self.paths = paths or []

    def add_path(self, path):
        self.paths.append(path)
        return self
