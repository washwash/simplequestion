from copy import copy
import random
import svgwrite
from datetime import datetime


class Painter:
    CELL_SIZE = (150, 50)
    ROW_CELL_COUNT = 7

    def __init__(self):
        self.drw = svgwrite.Drawing(
            'test.svg', profile='tiny'
        )

    def draw_canvas(self, data, point):
        canvas = self.drw.rect(
            insert=point,
            size=(
                len(data) * self.CELL_SIZE[0],
                max([len(d) for d in data]) * self.CELL_SIZE[1] + self.CELL_SIZE[1]
            ),
            fill='white'
        )
        self.drw.add(canvas)
        return canvas

    def draw_block(self, point, text, color, text_color='black'):
        self.drw.add(self.drw.rect(
            insert=point,
            size=self.CELL_SIZE,
            fill=color
        ))
        self.drw.add(self.drw.text(
            text,
            insert=(
                point[0] + 10,
                point[1] + 15
            ),
            fill=text_color
        ))


    def draw_day(self, day, point):
        next_place = copy(point)
        self.draw_block(
            next_place,
            day[0][1].strftime('%d-%m-%Y'),
            'grey'
        )
        colors = ('blue', 'red', 'green', 'yellow', 'purple')
        for record in day:
            next_place[1] += self.CELL_SIZE[1]
            self.draw_block(
                next_place,
                f'{record[1].strftime("%H:%M")} {record[2]}',
                random.choice(colors)
            )

    def draw(self, data):
        start_point = [0, 0]
        chunk = self.ROW_CELL_COUNT
        for part in [data[i:i+chunk] for i in range(0, len(data), chunk)]:
            canvas = self.draw_canvas(part, start_point)
            for day in part:
                self.draw_day(day, start_point)
                start_point[0] += self.CELL_SIZE[0]
            start_point[0] = 0
            start_point[1] += canvas.attribs['height']

        self.drw.save()

