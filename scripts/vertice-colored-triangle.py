from gameengine import get_gl_context
from array import array

vertices = [ 
    -0.5, -0.5,   1.0, 0.0, 0.0, # bottom left, s red
     0.5, -0.5,   0.0, 1.0, 0.0, # buttom right, blue
     0.0,  0.7,   0.0, 0.0, 1.0, # top point,    green
]

def startup():
    global ctx, program, vbo, vao

    ctx  = get_gl_context()

    program = ctx.program(
        vertex_shader = '''
            #version 330 core
            in vec2 vert;
            in vec3 in_color;
            out vec3 color;

            void main()
            {
                color = in_color;
                gl_Position = vec4(vert, 0.0, 1.0);
            }
        ''',

        fragment_shader = '''
            #version 330 core
            in vec3 color;
            out vec4 f_color;

            void main()
            {
                f_color = vec4(color, 1.0);
            }
        '''
    )

    vbo = ctx.buffer(array('f', vertices))
    
    vao = ctx.vertex_array(program, [(vbo, '2f 3f', 'vert', 'in_color')])

def draw():
    vao.render()
