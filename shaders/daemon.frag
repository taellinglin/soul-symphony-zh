#version 420

uniform sampler2D p3d_Texture0;
in vec2 resolution;
in float time;
// Input from vertex shader
in vec2 texcoord;
float random (vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}

void main() {
    vec2 st = texcoord.xy/resolution.xy;

    float rnd = random( st );

    gl_FragColor = vec4(1.0,0.0,1.0,rnd);
}