#version 420
#define PI 3.141592
#define TAU 2.0*PI
in vec2 resolution;
in float time;
in vec2 texcoord;
out vec4 fragColor;
precision mediump float;

void amod(inout vec2 p, float c) {
    float m = TAU / c;
    float a = mod(atan(p.x, p.y)-m*.5, m) - m*.5;
    p = vec2(cos(a), sin(a)) * length(p);
}

void mo(inout vec2 p, vec2 d) {
    p = abs(p) - d;
    if(p.y>p.x)p=p.yx;
}

mat2 r2d(float a) {
    float c = cos(a), s = sin(a);
    return mat2(c, s, -s, c);
}

float smooth_stairs(float x) {
    return tanh(5.*(x-floor(x)-0.5))/tanh(2.5)*0.5+floor(x)+0.5;
}

void main()
{
    vec2 uv = ( texcoord - .5*resolution.xy ) / resolution.y;
    //vec2 mouse = iMouse.xy / resolution.xy;
    uv.y = abs(uv.y);
    
    uv *= 3.0;
    //amod(uv, 5.5+sin(time*0.2)*2.5);
    float nrays = abs(mod(time*0.3, 10.)-5.);
    amod(uv, 8.-smooth_stairs(nrays));
    
    mo(uv, vec2(1.2+sin(time*0.3), 0.6+sin(time*0.5)*0.3));
    uv *= r2d(PI/12.-PI/8.*mod(time*0.2, 16.));
    mo(uv, vec2(1.1+sin(time*0.5)*0.7, 0.4+0.5*1.5));
    uv *= r2d(PI/6.-mod(time*0.25, 12.0)*PI/6.0);
    mo(uv, vec2(.7+sin(time*0.45)*0.2, .2));
    
    //uv *= 10.;
    uv *= 30.;
    //float l = min(abs(uv.x), abs(uv.y));
    //float l = max(abs(uv.x), abs(uv.y));
    float l = abs(uv.x) + abs(uv.y);
    float d = sin(l) - .3;
    
    d = smoothstep(0., fwidth(d), d);
    gl_FragColor = vec4(sqrt(d),sqrt(d),sqrt(d),sqrt(d));
}