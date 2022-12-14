from gameengine import get_gl_context, load_texture, get_shader 
from array import array

#IGNORE_MODULE = 1

vertices = [ 
    -0.5, -0.5, 0.0, 0.0, # bottom left,  texture coordinate
    0.5, -0.5,  1.0, 0.0, # buttom right, texture coordinate
    0, 0.7,     0.5, 1.0, # top point,    texture coordinate
]

def startup():
    global vao


    ctx  = get_gl_context()

    program = get_shader("textured-triangle")

    program['tex'] = 0
    program['tex2'] = 1

    texture = load_texture("test.png")
    texture_2 = load_texture("test2.png")
    
    texture.filter = (ctx.NEAREST, ctx.NEAREST) # blocky instead of blurry
    texture_2.filter = (ctx.NEAREST, ctx.NEAREST) # blocky instead of blurry
    
    texture.use(location=0)
    texture_2.use(location=1)

    vbo = ctx.buffer(array('f', vertices))
    
    vao = ctx.vertex_array(program, [(vbo, '2f 2f', 'vert', 'tex_coord')])


def draw():
    vao.render()
