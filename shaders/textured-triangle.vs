#version 330 core
in vec2 vert;
in vec2 tex_coord;

out vec2 v_tex_coord;

void main()
{
    gl_Position = vec4(vert, 0.0, 1.0);
    v_tex_coord = tex_coord;
}