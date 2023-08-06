#!/usr/bin/python
import numpy

triangle = numpy.array([
    5.0,  5.0, 0.0,
    -5.0,  5.0, 0.0,
    0.0, -5.0, 0.0],
    dtype=numpy.float32)

triangle_uv = numpy.array([
    5.0,  5.0, 0.0, 0.0, 1.0,
    -5.0,  5.0, 0.0, 1.0, 0.0,
    0.0, -5.0, 0.0, 0.0, 0.0],
    dtype=numpy.float32)

square = numpy.array([
    -5.0,  5.0, 0.0,
    -5.0, -5.0, 0.0,
    5.0,  5.0, 0.0,
    5.0, -5.0, 0.0],
    dtype=numpy.float32)

square_uv = numpy.array([
    -5.0,  5.0, 0.0, 0.0, 1.0,
    -5.0, -5.0, 0.0, 0.0, 0.0,
     5.0,  5.0, 0.0, 1.0, 0.0,
     5.0, -5.0, 0.0, 1.0, 1.0],
    dtype=numpy.float32)

simple_vertex_shader = [b"""
    #version 330
    uniform mat4 modelview_mat;
    uniform mat4 projection_mat;
    in vec3 vertex_pos;
    void main()
    {
        vec4 pos = vec4(vertex_pos, 1.0);
        gl_Position = projection_mat * modelview_mat * pos;
        //gl_Position = vec4(vertex_pos, 1.0);
    }"""]

simple_fragment_shader = [b"""
    #version 330
    out vec4 fragColor;
    void main()
    {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }"""]


simple_texture_vs = [b"""
    #version 330

    in vec3 vertex_pos;
    in vec2 texture_pos;

    uniform mat4 modelview_mat;
    uniform mat4 projection_mat;

    out vec2 tex_coords;

    void main(){
        vec4 pos = vec4(vertex_pos, 1.0);
        gl_Position = projection_mat * modelview_mat * pos;
        tex_coords = texture_pos;
    }"""]


simple_texture_fs = [b"""
    #version 330

    in vec2 tex_coords;
    uniform sampler2D quad_texture;

    out vec4 fragColor;
    void main(){
        fragColor = texture2D(quad_texture, tex_coords);
    }"""]

point_texture_vs = [b"""
    #version 330

    in vec3 vertex_pos;
    in vec2 texture_pos;

    uniform mat4 modelview_mat;
    uniform mat4 projection_mat;

    out vec2 tex_coords;

    void main(){

        vec4 pos = vec4(vertex_pos, 1.0);
        gl_Position = projection_mat * modelview_mat * pos;
        tex_coords = texture_pos;
    }"""]


point_texture_fs = [b"""
    #version 330

    in vec2 tex_coords;
    uniform sampler2D quad_texture;

    out vec4 fragColor;
    void main(){
        fragColor = vec4(tex_coords, 0.5 ,1);
    }"""]
