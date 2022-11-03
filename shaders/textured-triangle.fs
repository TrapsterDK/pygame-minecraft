#version 330 core
out vec4 f_color;

in vec2 v_tex_coord;

uniform sampler2D tex;
uniform sampler2D tex2;

void main()
{
    if (texture(tex2, v_tex_coord).a == 0.0 ){
        f_color = texture(tex, v_tex_coord);
    }else{
        f_color = mix(texture(tex, v_tex_coord), texture(tex2, v_tex_coord), 0.8);
    }
}