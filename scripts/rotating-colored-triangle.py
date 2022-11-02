
from gameengine import get_gl_context
from array import array

IGNORE_MODULE = 1

vertices = [ 
    -0.5, -0.5, # bottom left
    0.5, -0.5,  # buttom right 
    0, 0.7,     # top point 
]

def startup():
    global ctx, program, vbo, vao, rotation

    ctx  = get_gl_context()

    program = ctx.program(
        vertex_shader = '''
            #version 330 core
            in vec2 vert;
            out vec4 color;

            uniform float rotation;

            void main()
            {
                mat2 rot = mat2(cos(rotation), sin(rotation), -sin(rotation), cos(rotation));
                gl_Position = vec4(vert*rot, 0.0, 1.0);
                color = vec4(abs(sin(gl_Position.x)), abs(sin(gl_Position.y)), gl_Position.x, 1.0);
            }
        ''',

        fragment_shader = '''
            #version 330 core
            in vec4 color;
            out vec4 f_color;

            void main()
            {
                f_color = color;
            }
        '''
    )
    
    # Uniforms
    rotation = program['rotation']

    vbo = ctx.buffer(array('f', vertices))
    
    vao = ctx.vertex_array(program, [(vbo, '2f', 'vert')])

def draw():
    global rotation
    rotation.value += 0.01
    vao.render()
