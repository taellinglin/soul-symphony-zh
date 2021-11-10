#version 420
in float iTime;
in vec2 iResolution;
uniform mat4 p3d_ModelViewProjectionMatrix;
in vec2 p3d_MultiTexCoord0;
in vec4 p3d_Vertex;
out vec2 texcoord;
out float time;
out vec2 resolution;
void main() {
    time = iTime;
    resolution = iResolution;
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoord = p3d_MultiTexCoord0;
}