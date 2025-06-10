// Define precision based on the shader type and version
#if defined(VERTEX) || __VERSION__ > 100 || defined(GL_FRAGMENT_PRECISION_HIGH)
	#define MY_HIGHP_OR_MEDIUMP highp
#else
	#define MY_HIGHP_OR_MEDIUMP mediump
#endif

// External variables passed from the application
extern MY_HIGHP_OR_MEDIUMP vec2 enchanted; // Custom effect parameters
extern MY_HIGHP_OR_MEDIUMP number dissolve; // Dissolve effect intensity
extern MY_HIGHP_OR_MEDIUMP number time; // Time variable for animations
extern MY_HIGHP_OR_MEDIUMP vec4 texture_details; // Texture scaling and offset details
extern MY_HIGHP_OR_MEDIUMP vec2 image_details; // Image dimensions
extern bool shadow; // Whether to apply shadow effects
extern MY_HIGHP_OR_MEDIUMP vec4 burn_colour_1; // First burn color
extern MY_HIGHP_OR_MEDIUMP vec4 burn_colour_2; // Second burn color

// Function to apply a dissolve mask effect
vec4 dissolve_mask(vec4 tex, vec2 texture_coords, vec2 uv)
{
	// If dissolve is very low, return the original texture with optional shadow
	if (dissolve < 0.001) {
		return vec4(shadow ? vec3(0.,0.,0.) : tex.xyz, shadow ? tex.a*0.3 : tex.a);
	}

	// Adjust dissolve value for smoother transitions
	float adjusted_dissolve = (dissolve * dissolve * (3. - 2. * dissolve)) * 1.02 - 0.01;

	// Time-based animation variable
	float t = time * 10.0 + 2003.;

	// Scale and center UV coordinates
	vec2 floored_uv = (floor((uv * texture_details.ba))) / max(texture_details.b, texture_details.a);
	vec2 uv_scaled_centered = (floored_uv - 0.5) * 2.3 * max(texture_details.b, texture_details.a);

	// Generate animated fields using trigonometric functions
	vec2 field_part1 = uv_scaled_centered + 50. * vec2(sin(-t / 143.6340), cos(-t / 99.4324));
	vec2 field_part2 = uv_scaled_centered + 50. * vec2(cos(t / 53.1532), cos(t / 61.4532));
	vec2 field_part3 = uv_scaled_centered + 50. * vec2(sin(-t / 87.53218), sin(-t / 49.0000));

	// Combine fields into a single value
	float field = (1. + (
		cos(length(field_part1) / 19.483) + sin(length(field_part2) / 33.155) * cos(field_part2.y / 15.73) +
		cos(length(field_part3) / 27.193) * sin(field_part3.x / 21.92))) / 2.;

	// Define borders for the dissolve effect
	vec2 borders = vec2(0.2, 0.8);

	// Calculate the dissolve mask value
	float res = (.5 + .5 * cos((adjusted_dissolve) / 82.612 + (field + -.5) * 3.14))
		- (floored_uv.x > borders.y ? (floored_uv.x - borders.y) * (5. + 5. * dissolve) : 0.) * dissolve
		- (floored_uv.y > borders.y ? (floored_uv.y - borders.y) * (5. + 5. * dissolve) : 0.) * dissolve
		- (floored_uv.x < borders.x ? (borders.x - floored_uv.x) * (5. + 5. * dissolve) : 0.) * dissolve
		- (floored_uv.y < borders.x ? (borders.x - floored_uv.y) * (5. + 5. * dissolve) : 0.) * dissolve;

	// Apply burn colors based on dissolve mask conditions
	if (tex.a > 0.01 && burn_colour_1.a > 0.01 && !shadow && res < adjusted_dissolve + 0.8 * (0.5 - abs(adjusted_dissolve - 0.5)) && res > adjusted_dissolve) {
		if (!shadow && res < adjusted_dissolve + 0.5 * (0.5 - abs(adjusted_dissolve - 0.5)) && res > adjusted_dissolve) {
			tex.rgba = burn_colour_1.rgba;
		} else if (burn_colour_2.a > 0.01) {
			tex.rgba = burn_colour_2.rgba;
		}
	}

	// Return the final texture with dissolve mask applied
	return vec4(shadow ? vec3(0.,0.,0.) : tex.xyz, res > adjusted_dissolve ? (shadow ? tex.a * 0.3 : tex.a) : .0);
}

// Helper function to calculate hue for RGB conversion
number hue(number s, number t, number h)
{
	number hs = mod(h, 1.) * 6.;
	if (hs < 1.) return (t - s) * hs + s;
	if (hs < 3.) return t;
	if (hs < 4.) return (t - s) * (4. - hs) + s;
	return s;
}

// Convert HSL to RGB
vec4 RGB(vec4 c)
{
	if (c.y < 0.0001)
		return vec4(vec3(c.z), c.a);

	number t = (c.z < .5) ? c.y * c.z + c.z : -c.y * c.z + (c.y + c.z);
	number s = 2.0 * c.z - t;
	return vec4(hue(s, t, c.x + 1. / 3.), hue(s, t, c.x), hue(s, t, c.x - 1. / 3.), c.w);
}

// Convert RGB to HSL
vec4 HSL(vec4 c)
{
	number low = min(c.r, min(c.g, c.b));
	number high = max(c.r, max(c.g, c.b));
	number delta = high - low;
	number sum = high + low;

	vec4 hsl = vec4(.0, .0, .5 * sum, c.a);
	if (delta == .0)
		return hsl;

	hsl.y = (hsl.z < .5) ? delta / sum : delta / (2.0 - sum);

	if (high == c.r)
		hsl.x = (c.g - c.b) / delta;
	else if (high == c.g)
		hsl.x = (c.b - c.r) / delta + 2.0;
	else
		hsl.x = (c.r - c.g) / delta + 4.0;

	hsl.x = mod(hsl.x / 6., 1.);
	return hsl;
}

// Main fragment shader effect function
vec4 effect(vec4 colour, Image texture, vec2 texture_coords, vec2 screen_coords)
{
	// Sample the texture at the given coordinates
	vec4 tex = Texel(texture, texture_coords);

	// Adjust UV coordinates based on texture details
	vec2 uv = (((texture_coords) * (image_details)) - texture_details.xy * texture_details.ba) / texture_details.ba;

	// Rotate UV coordinates 45 degrees counterclockwise
	float angle = radians(-45.0);
	mat2 rotation = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
	vec2 rotated_uv = rotation * uv;

	// Calculate saturation factor based on color delta
	number low = min(tex.r, min(tex.g, tex.b));
	number high = max(tex.r, max(tex.g, tex.b));
	number delta = high - low;
	number saturation_fac = 1. - max(0., 0.05 * (1.1 - delta));

	// Convert texture color to HSL and adjust hue and saturation
	vec4 hsl = HSL(vec4(tex.r * saturation_fac, tex.g * saturation_fac, tex.b, tex.a));
	float t = enchanted.y * 2.221 + time;

	// Generate a linear gradient field based on rotated UV coordinates
	float field = rotated_uv.x * 10.0 + enchanted.y * 0.1; // Increase the multiplier for faster gradient changes

	// Adjust HSL values based on the field
	float res = (.5 + .5 * cos((enchanted.x) * 2.612 + (field + -.5) * 3.14));
	hsl.x = mod(hsl.x + res * 0.1, 1.0); // Keep original hue range
	hsl.y = min(0.6, hsl.y + 0.5);

	// Convert HSL back to RGB
	tex.rgb = RGB(hsl).rgb;

	// Adjust alpha for transparency effects
	if (tex[3] < 0.7)
		tex[3] = tex[3] / 3.;

	// Apply dissolve mask and return the final color
	return dissolve_mask(tex * colour, texture_coords, uv);
}

// External variables for vertex shader
extern MY_HIGHP_OR_MEDIUMP vec2 mouse_screen_pos; // Mouse position on screen
extern MY_HIGHP_OR_MEDIUMP float hovering; // Whether the mouse is hovering
extern MY_HIGHP_OR_MEDIUMP float screen_scale; // Screen scaling factor

#ifdef VERTEX
// Vertex shader function to adjust position based on mouse interaction
vec4 position(mat4 transform_projection, vec4 vertex_position)
{
	// If not hovering, return the default position
	if (hovering <= 0.) {
		return transform_projection * vertex_position;
	}

	// Calculate distance from the center of the screen
	float mid_dist = length(vertex_position.xy - 0.5 * love_ScreenSize.xy) / length(love_ScreenSize.xy);

	// Calculate offset based on mouse position
	vec2 mouse_offset = (vertex_position.xy - mouse_screen_pos.xy) / screen_scale;

	// Scale the position based on hovering and distance
	float scale = 0.2 * (-0.03 - 0.3 * max(0., 0.3 - mid_dist))
				* hovering * (length(mouse_offset) * length(mouse_offset)) / (2. - mid_dist);

	// Return the transformed position
	return transform_projection * vertex_position + vec4(0, 0, 0, scale);
}
#endif