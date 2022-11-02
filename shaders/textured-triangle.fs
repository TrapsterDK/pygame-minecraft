#version 330 core
out vec4 f_color;

in vec2 v_tex_coord;

uniform sampler2D tex;

void main()
{
    f_color = texture(tex, v_tex_coord);
}