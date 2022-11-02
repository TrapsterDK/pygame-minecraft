from gameengine import get_gl_context
from array import array

IGNORE_MODULE = 1

vertices = [ 
    -0.5, -0.5, # bottom left
    0.5, -0.5,  # buttom right 
    0, 0.7,     # top point 
]

def startup():
    global ctx, program, vbo, vao

    ctx  = get_gl_context()

    program = ctx.program(
        vertex_shader = '''
            #version 330 core
            in vec2 vert;

            void main()
            {
                gl_Position = vec4(vert, 0.0, 1.0);
            }
        ''',

        fragment_shader = '''
            #version 330 core
            out vec4 color;

            void main()
            {
                color = vec4(1.0, 0.5, 0.5, 1.0);
            }
        '''
    )

    vbo = ctx.buffer(array('f', vertices))
    
    vao = ctx.vertex_array(program, [(vbo, '2f', 'vert')])

def draw():
    vao.render()
