#define PI 3.1415926535
uniform vec2 resolution;
uniform float u_time;
float random2d(vec2 n) { 
    return fract(sin(dot(n, vec2(129.9898, 4.1414))) * 2398.5453);
}

vec2 getCellIJ(vec2 uv, float gridDims){
    return floor(uv * gridDims)/ gridDims;
}

vec2 rotate2D(vec2 position, float theta)
{
    mat2 m = mat2( cos(theta), -sin(theta), sin(theta), cos(theta) );
    return m * position;
}

//from https://github.com/keijiro/ShaderSketches/blob/master/Text.glsl
float letter(vec2 coord, float size)
{
    vec2 gp = floor(coord / size * 7.); // global
    vec2 rp = floor(fract(coord / size) * 7.); // repeated
    vec2 odd = fract(rp * 0.5) * 2.;
    float rnd = random2d(gp);
    float c = max(odd.x, odd.y) * step(0.5, rnd); // random lines
    c += min(odd.x, odd.y); // fill corner and center points
    c *= rp.x * (6. - rp.x); // cropping
    c *= rp.y * (6. - rp.y);
    return clamp(c, 0., 1.);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{

    vec2 uv = fragCoord.xy / resolution.xy;    
    //correct aspect ratio
    uv.x *= resolution.x/resolution.y;
    float t = u_time;
    float scrollSpeed = 0.3;
    float dims = 2.0;
    int maxSubdivisions = 3;
    
    //uv = rotate2D(uv,PI/12.0);
    uv.y -= u_time * scrollSpeed;
    
    float cellRand;
    vec2 ij;
    
   	for(int i = 0; i <= maxSubdivisions; i++) { 
        ij = getCellIJ(uv, dims);
        cellRand = random2d(ij);
        dims *= 2.0;
        //decide whether to subdivide cells again
        float cellRand2 = random2d(ij + 454.4543);
        if (cellRand2 > 0.3){
        	break; 
        }
    }
   
    //draw letters    
    float b = letter(uv, 1.0 / (dims));
	
    //fade in
    float scrollPos = u_time*scrollSpeed + 0.5;
    float showPos = -ij.y + cellRand;
    float fade = smoothstep(showPos ,showPos + 0.05, scrollPos );
    b *= fade;
    
    //hide some
    if (cellRand < 0.1) b = 0.0;
    
    fragColor = vec4(vec3(b), 1.0);
    
}