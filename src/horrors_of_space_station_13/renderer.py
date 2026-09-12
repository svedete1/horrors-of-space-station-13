import ctypes

import numpy as np
import pygame
from OpenGL import GL
from OpenGL.GL import shaders as gl_shaders

from .settings import BLACK, TILE

_SPRITE_VERT = """#version 330 core
layout(location = 0) in vec2 aPos;
layout(location = 1) in vec2 aTexCoord;
uniform mat4 uProjection;
out vec2 vTexCoord;
void main() {
    gl_Position = uProjection * vec4(aPos, 0.0, 1.0);
    vTexCoord = aTexCoord;
}
"""

_SPRITE_FRAG = """#version 330 core
in vec2 vTexCoord;
uniform sampler2D uTexture;
out vec4 fragColor;
void main() {
    fragColor = texture(uTexture, vTexCoord);
}
"""

_COLOR_VERT = """#version 330 core
layout(location = 0) in vec2 aPos;
uniform mat4 uProjection;
void main() {
    gl_Position = uProjection * vec4(aPos, 0.0, 1.0);
}
"""

_COLOR_FRAG = """#version 330 core
uniform vec4 uColor;
out vec4 fragColor;
void main() {
    fragColor = uColor;
}
"""

# Bytes per sprite vertex: vec2 position + vec2 texcoord.
_SPRITE_VERTEX_SIZE = 4 * 4
_POS_OFFSET = 0
_TEX_OFFSET = 2 * 4


class ShaderProgram:

    def __init__(self, vertex_src, fragment_src):
        vertex = gl_shaders.compileShader(vertex_src, GL.GL_VERTEX_SHADER)
        fragment = gl_shaders.compileShader(fragment_src, GL.GL_FRAGMENT_SHADER)
        self.program = gl_shaders.compileProgram(vertex, fragment)

    def use(self):
        GL.glUseProgram(self.program)

    def uniform(self, name):
        return GL.glGetUniformLocation(self.program, name)


class Texture:

    __slots__ = ("id", "width", "height", "surface")

    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()
        # Upload top-to-bottom (flipped=False): texture row 0 (v=0) is the top
        # image row, matching the v mapping used by draw_tile/draw_region.
        data = pygame.image.tobytes(surface, "RGBA")

        self.id = int(GL.glGenTextures(1))
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.id)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGBA,
            self.width,
            self.height,
            0,
            GL.GL_RGBA,
            GL.GL_UNSIGNED_BYTE,
            data,
        )
        # Nearest filtering keeps pixel art crisp; clamp avoids edge bleeding.
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def bind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.id)


class TextureManager:

    _cache = {}

    @classmethod
    def get(cls, path):
        texture = cls._cache.get(path)
        if texture is None:
            surface = pygame.image.load(path).convert_alpha()
            texture = Texture(surface)
            cls._cache[path] = texture
        return texture

    @classmethod
    def clear(cls):
        cls._cache.clear()


class Renderer:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.sprite_program = ShaderProgram(_SPRITE_VERT, _SPRITE_FRAG)
        self.color_program = ShaderProgram(_COLOR_VERT, _COLOR_FRAG)
        self.projection = self._make_projection(width, height)

        self.sprite_vao, self.sprite_vbo = self._make_sprite_geometry()
        self.line_vao, self.line_vbo = self._make_line_geometry()

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glDisable(GL.GL_DEPTH_TEST)

        # Quads: (texture_id, dst_x, dst_y, dst_w, dst_h, u0, v0, u1, v1)
        self.sprite_quads = []
        # Lines: (x1, y1, x2, y2, (r, g, b))
        self.lines = []

    @staticmethod
    def _make_projection(width, height):
        # Row-major ortho matrix mapping pixel (x, y) -> NDC, y flipped so that
        # (0, 0) is the top-left corner (pygame convention).
        return np.array(
            [
                [2.0 / width, 0.0, 0.0, -1.0],
                [0.0, -2.0 / height, 0.0, 1.0],
                [0.0, 0.0, -1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        )

    def _make_sprite_geometry(self):
        vao = int(GL.glGenVertexArrays(1))
        vbo = int(GL.glGenBuffers(1))
        GL.glBindVertexArray(vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(
            0, 2, GL.GL_FLOAT, GL.GL_FALSE, _SPRITE_VERTEX_SIZE, ctypes.c_void_p(_POS_OFFSET)
        )
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(
            1, 2, GL.GL_FLOAT, GL.GL_FALSE, _SPRITE_VERTEX_SIZE, ctypes.c_void_p(_TEX_OFFSET)
        )
        GL.glBindVertexArray(0)
        return vao, vbo

    def _make_line_geometry(self):
        vao = int(GL.glGenVertexArrays(1))
        vbo = int(GL.glGenBuffers(1))
        GL.glBindVertexArray(vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, ctypes.c_void_p(0))
        GL.glBindVertexArray(0)
        return vao, vbo

    def begin(self, clear_color=BLACK):
        GL.glClearColor(*(c / 255.0 for c in clear_color), 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        self.sprite_quads.clear()
        self.lines.clear()

    def end(self):
        # Sprites first, then the aim line on top, then present the frame.
        if self.sprite_quads:
            self._flush_sprites()
        if self.lines:
            self._flush_lines()
        pygame.display.flip()

    def draw_tile(self, texture, dst_x, dst_y, col, row, tile_size=TILE):
        u0 = (col * tile_size) / texture.width
        v0 = (row * tile_size) / texture.height
        u1 = ((col + 1) * tile_size) / texture.width
        v1 = ((row + 1) * tile_size) / texture.height
        self.sprite_quads.append(
            (texture.id, dst_x, dst_y, tile_size, tile_size, u0, v0, u1, v1)
        )

    def draw_region(self, texture, dst_x, dst_y, dst_w, dst_h, src_rect):
        u0 = src_rect[0] / texture.width
        v0 = src_rect[1] / texture.height
        u1 = (src_rect[0] + src_rect[2]) / texture.width
        v1 = (src_rect[1] + src_rect[3]) / texture.height
        self.sprite_quads.append(
            (texture.id, dst_x, dst_y, dst_w, dst_h, u0, v0, u1, v1)
        )

    def draw_line(self, x1, y1, x2, y2, color):
        self.lines.append((x1, y1, x2, y2, color))

    def _flush_sprites(self):
        # Group by texture so we only rebind textures, not per quad.
        groups = {}
        for quad in self.sprite_quads:
            groups.setdefault(quad[0], []).append(quad)

        self.sprite_program.use()
        GL.glUniformMatrix4fv(
            self.sprite_program.uniform("uProjection"), 1, GL.GL_TRUE, self.projection
        )
        GL.glUniform1i(self.sprite_program.uniform("uTexture"), 0)
        GL.glActiveTexture(GL.GL_TEXTURE0)

        GL.glBindVertexArray(self.sprite_vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.sprite_vbo)

        for texture_id, quads in groups.items():
            vertices = np.empty((len(quads) * 6, 4), dtype=np.float32)
            i = 0
            for _, x, y, w, h, u0, v0, u1, v1 in quads:
                x0, y0 = x, y
                x1, y1 = x + w, y + h
                vertices[i : i + 6] = (
                    (x0, y0, u0, v0),
                    (x1, y0, u1, v0),
                    (x1, y1, u1, v1),
                    (x0, y0, u0, v0),
                    (x1, y1, u1, v1),
                    (x0, y1, u0, v1),
                )
                i += 6

            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_DYNAMIC_DRAW)
            GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, i)

        GL.glBindVertexArray(0)

    def _flush_lines(self):
        self.color_program.use()
        GL.glUniformMatrix4fv(
            self.color_program.uniform("uProjection"), 1, GL.GL_TRUE, self.projection
        )
        color_loc = self.color_program.uniform("uColor")

        GL.glBindVertexArray(self.line_vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.line_vbo)

        for x1, y1, x2, y2, color in self.lines:
            vertices = np.array((x1, y1, x2, y2), dtype=np.float32)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_DYNAMIC_DRAW)
            GL.glUniform4f(
                color_loc, color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, 1.0
            )
            GL.glDrawArrays(GL.GL_LINES, 0, 2)

        GL.glBindVertexArray(0)
