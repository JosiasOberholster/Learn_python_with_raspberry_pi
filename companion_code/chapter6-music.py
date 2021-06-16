import pygame
from rpigl import glesutils, transforms
from rpigl.gles2 import *
import random
import wave
import time

vertices = [(0.0,0.0,0.0), (0.5,0.0,0.0), (0.5,0.5,0.0), (0.0, 0.5,0.0), 
            (0.0,0.0,-0.5), (0.5,0.0,-0.5), (0.5,0.5,-0.5), (0.0, 0.5,-0.5)]

indices_outer = (0, 1, 2, 3, 0, 4, 5, 1, 5, 6, 2, 6, 7, 3, 7, 4)

vertices_points = []
indices_points = []

for i in range(0,100):
    vertices_points.append(((20 * random.random())-10, (20 * random.random()), (20 * random.random())-10))
    indices_points.append(i)


array_spec = glesutils.ArraySpec("vertex_attrib:3f")

vertex_glsl = array_spec.glsl() + """
uniform mat4 position_matrix;
uniform mat4 eye_matrix;
uniform mat4 scaling_matrix;
uniform mat4 sound_matrix;
uniform float point_size;

varying float red;

void main(void) {
  gl_Position = eye_matrix * position_matrix * scaling_matrix * sound_matrix * vec4(vertex_attrib, 1.0);
  red = (gl_Position[1]+0.9)/2.0;
  gl_PointSize = point_size;
}
"""

fragment_glsl = """
uniform vec4 color;

varying float red;

void main(void) {
  gl_FragColor = vec4(red, 0.0, (1.0-red)/5.0, 1.0);
}
"""



class MyWindow(glesutils.GameWindow):

    def init(self):

        self.angle_x = 5
        self.angle_y = 10
        self.angle_z = 5
        self.framerate = 20
        self.counter = 0

        self.vertex_shader = glesutils.VertexShader(vertex_glsl)
        self.fragment_shader = glesutils.FragmentShader(fragment_glsl)

        self.program1 = glesutils.Program(self.vertex_shader, self.fragment_shader)
        self.program1.use()

        glClearDepthf(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)


        glClearColor(0.0, 0.0, 0.0, 1)

        self.program1.uniform.light_dir.value = ((0, 1, -1))

        self.verteces_buffer = array_spec.create_buffer(vertex_attrib=vertices)
        self.points_buffer = array_spec.create_buffer(vertex_attrib=vertices_points)

        self.elements_outer = glesutils.ElementBuffer(indices_outer)
        self.elements_points = glesutils.ElementBuffer(indices_points)

        self.blank_matrix = transforms.translation(0.0, 0.0, 0.0)

        self.position_matrix = []
        for i in range(0,20):
            self.position_matrix.append(transforms.translation((i/10)-0.95, 0.0, 0.0))

        self.sound_matrix = []
        for i in range(0,20):
            self.sound_matrix.append(transforms.translation(0.0, 0.0, 0.0))

        self.program1.uniform.scaling_matrix.value = transforms.scaling(0.1)

        self.program1.uniform.eye_matrix.value = transforms.compose(transforms.rotation_degrees(self.angle_z, "z"), 
                transforms.rotation_degrees(self.angle_x, "y"), 
                transforms.rotation_degrees(self.angle_x, "x"),
                transforms.translation(0.0, -0.9, 0.0))
        self.counter = 0

    def on_frame(self, ftime):
        global start_time
        global data

        self.angle_y = self.angle_y + .5

        self.program1.uniform.eye_matrix.value = transforms.compose(transforms.rotation_degrees(self.angle_z, "z"), 
                transforms.rotation_degrees(self.angle_y, "y"), 
                transforms.rotation_degrees(self.angle_x, "x"),
                transforms.translation(0.0, -0.9, 0.0))

        frame_position = int((pygame.time.get_ticks() - start_time) * 44.1 * 4)

#        print("haow far through ", frame_position/len(data))
#        print("time: ", pygame.time.get_ticks() - start_time)



        scale_factor = 0
        if frame_position + 1000 < len(data):
            for i in range(1,500):
                scale_factor1 = scale_factor + int.from_bytes(data[frame_position+2*i:frame_position+(2*i)+1], byteorder='little', signed=True)**2

            scale_factor1 = scale_factor1 / 500

            self.sound_matrix[self.counter%20] = transforms.stretching(1.0,scale_factor1,1.0)

            self.program1.uniform.point_size.value = float(scale_factor1/4)

            self.counter = self.counter+1

        self.redraw()
        
    def draw(self):
        self.program1.uniform.color.value = (1, 1, 1, 1)
        for i in range(0,20):
            self.program1.uniform.position_matrix.value = self.position_matrix[i]
            self.program1.uniform.sound_matrix.value = self.sound_matrix[i]
            self.verteces_buffer.draw(elements=self.elements_outer, mode=GL_LINE_STRIP)
            self.counter = self.counter +1

        self.program1.uniform.position_matrix.value = self.blank_matrix
        self.program1.uniform.sound_matrix.value = self.blank_matrix
        self.points_buffer.draw(mode=GL_POINTS)





print("starting pygame mixer")
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
music = pygame.mixer.Sound("tell.wav")

print("opening file")
sound_file = wave.open("test.wav",'rb')

print("getting parameters")
(channels, sample_size, frame_rate, frames, compression_type, compression_name) = sound_file.getparams()

print("Number of channels: ", channels)
print("Sample size: ", sample_size)
print("Frame rate: ", frame_rate)
print("Number of Frames: ", frames)
print("Compression type: ", compression_type)
print("Compression name: ", compression_name)

print("readframes")
data = sound_file.readframes(4*frames)
print(len(data))

print("starting audio")
music.play()
start_time = pygame.time.get_ticks()

print("start time: ", time.clock())

MyWindow(200, 200, pygame.RESIZABLE).run()