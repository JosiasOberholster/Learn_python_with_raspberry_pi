import pygame
from rpigl import glesutils, transforms
from rpigl.gles2 import *

vertices = [(0.0,0.0,0.0), (0.5,0.0,0.0), (0.5,0.5,0.0), (0.0, 0.5,0.0), 
            (0.0,0.0,-0.5), (0.5,0.0,-0.5), (0.5,0.5,-0.5), (0.0, 0.5,-0.5)]

faces = [{"vertex_index":(0, 1, 2, 0, 3), "normal":(0,0,1), "colour":(1, 0, 0, 1)},
         {"vertex_index":(4, 5, 6, 4, 7), "normal":(0,0,-1), "colour":(0, 1, 0, 1)},
         {"vertex_index":(1, 5, 6, 1, 2), "normal":(1,0,0), "colour":(0, 0, 1, 1)},
         {"vertex_index":(0, 4, 7, 0 ,3), "normal":(-1,0,0), "colour":(1, 0, 1, 1)},
         {"vertex_index":(3, 2, 6, 3, 7), "normal":(0,1,0), "colour":(1, 1, 0, 1)},
         {"vertex_index":(0, 1, 5, 0, 4), "normal":(0,-1,0), "colour":(0, 1, 1, 1)}]

array_spec = glesutils.ArraySpec("vertex_attrib:3f")

vertex_glsl = array_spec.glsl() + """
uniform mat4 transform_matrix;
uniform vec3 light_position;
uniform float ambient_light;
uniform vec3 face_normal;

varying float brightness;

void main(void) {
  gl_Position = transform_matrix * vec4(vertex_attrib, 1.0);
  vec4 spun_face_normal = normalize(transform_matrix * vec4(face_normal, 1.0));
  float distance = length(vec4(light_position, 1.0) - gl_Position);
  vec4 light_direction = normalize(vec4(light_position, 1.0) - gl_Position);
  float light_amount_angle = max(dot(spun_face_normal, light_direction), ambient_light);
  float light_distance_drop = 1.0/(distance * distance);
  brightness = light_amount_angle * light_distance_drop;
  gl_PointSize = 2.0;
}
"""

fragment_glsl = """
uniform vec4 color;

varying float brightness;

void main(void) {
  gl_FragColor = brightness*color;
}
"""



class MyWindow(glesutils.GameWindow):

    def init(self):

        self.angle = 10
        self.framerate = 20

        self.vertex_shader = glesutils.VertexShader(vertex_glsl)
        self.fragment_shader = glesutils.FragmentShader(fragment_glsl)

        self.program1 = glesutils.Program(self.vertex_shader, self.fragment_shader)
        self.program1.use()

        glClearDepthf(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glFrontFace(GL_CW)

        glClearColor(0.5, 0.5, 0.5, 1)

        self.program1.uniform.light_dir.value = ((0, 1, -1))

        self.verteces_buffer = array_spec.create_buffer(vertex_attrib=vertices)
        for face in faces:
            face["element_buffer"] = glesutils.ElementBuffer(face["vertex_index"])

        self.outer_matrix = transforms.compose(transforms.rotation_degrees(20, "z"), 
                transforms.rotation_degrees(20, "y"), 
                transforms.rotation_degrees(20, "x"),
                transforms.scaling(1.2))

        self.points_matrix = transforms.compose(transforms.stretching(0.1, 1, 1.5),
                             transforms.translation(-0.5, -0.5, -0.5))

    def on_frame(self, time):
        self.angle = self.angle + time*0.02
        self.redraw()

    def draw(self):
        self.program1.uniform.light_position.value = (0,0,-1)
        self.program1.uniform.ambient_light.value = 0.3
   
        rotation_matrix = transforms.compose(transforms.rotation_degrees(self.angle, "z"), 
                transforms.rotation_degrees(self.angle, "y"),
                transforms.compose(transforms.rotation_degrees(self.angle, "x")))
        self.program1.uniform.transform_matrix.value = rotation_matrix

        for face in faces:
            self.program1.uniform.color.value = face["colour"]
            self.program1.uniform.face_normal.value = face["normal"]
            self.verteces_buffer.draw(elements=face["element_buffer"], mode=GL_TRIANGLE_STRIP)

MyWindow(200, 200, pygame.RESIZABLE).run()