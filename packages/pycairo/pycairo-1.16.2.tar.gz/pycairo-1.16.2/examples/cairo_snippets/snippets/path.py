
def draw(cr, width, height):
    cr.scale(width, height)
    cr.set_line_width(0.04)

    cr.move_to(0.5, 0.1)
    cr.line_to(0.9, 0.9)
    cr.rel_line_to(-0.4, 0.0)
    cr.curve_to(0.2, 0.9, 0.2, 0.5, 0.5, 0.5)

    cr.stroke()
