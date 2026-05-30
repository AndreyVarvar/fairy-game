import pygame as pg
import pygame._sdl2.video as sdl2

from .element import Element

# I swear this wasn't stolen
class Renderer(Element):
    def __init__(self) -> None:
        super().__init__(singleton=True)
        self.queue: list = []

        self.order: int = 0

    def clear(self):
        self.order = 0
        self.queue = []

    def queue_draw(
            self,
            texture: sdl2.Texture,
            z: int,
            destination: pg.Rect | pg.FRect,
            source: pg.Rect | None = None,
            flip_x: bool = False,
            flip_y: bool = False,
            angle: float = 0.0,
            pivot: pg.Vector2 | tuple[int, int] | None = None,
            color: pg.Color = pg.Color(255, 255, 255),
            alpha: int = 255,
            blend_mode: int = pg.BLENDMODE_BLEND
    ):
        """
        surface: pygame.Surface. The image to be drawn.
        z: int. z-index of the object. Lower values increase the draw priority
        destination: pygame.Rect. Defines an area where the source image will be drawn into. The image wil be stretched to fit it.
        flip_x: bool. Determines whether the image will be horizontally flipped when drawn.
        flip_y: bool. Duh. You absolute buffoon! You nitwit! You confounded nincompoop! Numskull! Nimrod!
        angle: float. Angle of rotation. Determines by how much the destination rect will be rotated around the `pivot` parameter.
        pivot: pointLike. Determines the pivot for rotation of the destination rect.
        color: ColorLike. Determines how visible is each color channel of the texture. For example, (255, 0, 0) will makes it so that only the red values are visible.
        alpha: int. from 0 to 255. controls transparency. 255 is fully opaque, 0 is fully transparent.
        Used by objects to "queue" themselves into the drawing queue, after which they will be drawn alongside every other element
        """
        self.queue.append([z, self.order, texture, destination, flip_x, flip_y, angle, pivot, source, color, alpha, blend_mode])
        self.order += 1

    def draw(self):
        """
        targets: dict[str, pygame.Surface]. A dictonary with keys being the target name and the surface (target meaning where to draw)
        Draws everything queued so far. Should be called once per frame.
        """
        self.order = 0  # reset it so that it doesn't grow inifinitely
        self.queue.sort(key = lambda x:x[0])
        for sprite in self.queue:
            _, _, texture, dest, flip_x, flip_y, angle, pivot, source, color, alpha, blend_mode = sprite
            texture.color = color
            texture.alpha = alpha
            texture.blend_mode = blend_mode
            texture.draw(srcrect=source, dstrect=dest, angle=angle, origin=pivot, flip_x=flip_x, flip_y=flip_y)
