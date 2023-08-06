/*
# $BEGIN_SHADY_LICENSE$
# 
# This file is part of the Shady project, a Python framework for
# real-time manipulation of psychophysical stimuli for vision science.
# 
# Copyright (C) 2017-18  Jeremy Hill, Scott Mooney
# 
# Shady is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/ .
# 
# $END_SHADY_LICENSE$
*/
varying vec3      vFragCoordinateInEnvelope;
varying vec2      vTextureCoordinates;

uniform float     uAlpha;
uniform vec3      uBackgroundColor;
uniform float     uBackgroundAlpha;
uniform mat3      uCarrierTransformation;
uniform vec3      uColor;
uniform vec2      uDebugDigitsStartXY;  // the lower-left corner of the first digit starts here relative to the lower-left corner of the texture
uniform vec2      uDebugDigitSize; // each digit spans this many pixels
uniform vec3      uDebugValueIJK;  // row, column and layer of the texture to query and render in the DebugDigits area
uniform vec2      uEnvelopeSize;
uniform int       uFramesCompleted;
uniform vec3      uGamma;
uniform vec3      uNoiseAmplitude;
uniform float     uNormalizedContrast;
uniform vec3      uOffset;
uniform vec2      uPlateauProportion;
uniform int       uSignalFunction;
uniform vec4      uSignalParameters;
uniform int       uModulationFunction;
uniform vec4      uModulationParameters;
uniform vec3      uOutOfRangeColor;
uniform float     uOutOfRangeAlpha;
uniform bool      uShady;
uniform vec2      uTextureSize;
uniform sampler2D uTextureSlotNumber;
uniform bool      uUseTexture;
uniform vec3      uLookupTableTextureSize; // width (number of columns), height (number of rows), length (total number of valid entries)
uniform sampler2D uLookupTableTextureSlotNumber;

//#CUSTOM_UNIFORMS

#define PI                 3.1415926535897932384626433832795
#define TWO_PI             6.283185307179586231995926937088
#define RADIANS_PER_DEGREE 0.017453292519943295474371680598

float InverseLength( vec2 x )
{
	float len = length( x );
	if( len == 0.0 ) return 1.0;
	return 1.0 / len;
}

vec4 Texture_Pixels_XY( sampler2D texture, vec2 textureSize, vec2 coords ) // [0,0] is bottom left;  [1, 0] is next pixel horizontally
{
	coords.y = textureSize.y - coords.y; // no -1 offset: gl_Vertex will have delivered coordinates of gridlines (0 to textureSize.* INCLUSIVE) and texture2D expects these too
	return texture2D( texture, coords / textureSize );
}

vec4 Texture_Pixels_IJ( sampler2D texture, vec2 textureSize, vec2 coords ) // [0,0] is top left; [0, 1] is next pixel horizontally
{
	coords = mod( coords.yx, textureSize ); // mod necessary because of the different coordinate convention
	return texture2D( texture, ( coords + vec2( 0.5, 0.5 ) ) / textureSize ); // offset of 0.5 to reach the pixel center, because texture2D thinks of whole-number coordinates as matching gridlines between pixels
}

float Linearize( float x, float gamma )
{	
	if( gamma == 1.0 ) return x; // linear
	if( x <= 0.0 ) return x;
	if( gamma > 0.0 ) return pow( x, 1.0 / gamma ); // gamma function
	// so now we're left with gamma <= 0.0, which signifies that the nonlinearity is sRGB 
	// (which looks very similar to a gamma of 2.2, even though the exponent it uses is 2.4)
	if( x <= 0.04045 / 12.92 ) return x * 12.92;
	x = pow( x, 1.0 / 2.4 );
	return x * 1.055 - 0.055;
}	

float Digit( float x, int position, float base )
{
	int i;
	float digit;
	
	x = abs( x );
	if( position < 0 )
	{
		x = fract( x );
		for( i = -1; i >= position; i-- )
		{
			if( x <= 0.0 ) { digit = 0.0; break; }
			x *= base;
			digit = floor( x );
			x -= digit;
		}
	}
	else
	{
		x = floor( x );
		float prevx;
		for( i = 0; i <= position; i++ )
		{
			if( x <= 0.0 ) { digit = 0.0; break; }
			prevx = x;
			x = floor( x / base );
			digit = prevx - base * x;
		}
	}
	return digit;
}

float OrderOfMagnitude( float x )
{
	return x == 0.0 ? 0.0 : floor( log( abs( x ) ) / log( 10.0 ) );
}

void RenderDecimal( float value )
{
	// Assume that the texture to which uTextureSlotNumber refers contains
	// a rendering of the digits '0123456789' packed together
	float nSpaces = 10.0;
	const float signSpace = 0.4;
	vec2 pos = vFragCoordinateInEnvelope.xy - uDebugDigitsStartXY;
	if( value < 0.0 ) { pos.x -= uDebugDigitSize.x * signSpace; nSpaces -= signSpace; }
	float dpstart = max( 0.0, OrderOfMagnitude( value ) );
	int decimal_position = int( dpstart - floor( pos.x / uDebugDigitSize.x ) );
	float remainder = mod( pos.x, uDebugDigitSize.x );
	if( pos.x <= uDebugDigitSize.x * nSpaces && pos.y >= 0.0 && pos.y <= uDebugDigitSize.y  )
	{
		if( pos.x >= 0.0 )
		{
			float digit_value = Digit( value, decimal_position, 10.0 );
			vec2 textureSourcePosition = vec2( uDebugDigitsStartXY.x + remainder + digit_value * uDebugDigitSize.x, uDebugDigitsStartXY.y + pos.y );
			gl_FragColor = Texture_Pixels_XY( uTextureSlotNumber, uTextureSize, textureSourcePosition );
		}
		else if( value < 0.0 && pos.x >= -uDebugDigitSize.x * signSpace )
		{
			float x = ( abs( pos.y / uDebugDigitSize.y - 0.5 ) < 0.05 ) ? 1.5 : 0.5;  // middle of a digit 1 (foreground) or middle of a digit 0 (background)
			gl_FragColor = Texture_Pixels_XY( uTextureSlotNumber, uTextureSize, uDebugDigitsStartXY + uDebugDigitSize * vec2( x, 0.5 ) );
		}
	}
	if( ( decimal_position == -1 && remainder / uDebugDigitSize.x <= 0.1 && abs( pos.y ) / uDebugDigitSize.y <= 0.1 ) ||
	    ( decimal_position ==  0 && remainder / uDebugDigitSize.x >= 0.9 && abs( pos.y ) / uDebugDigitSize.y <= 0.1 ) )
	{
		gl_FragColor = Texture_Pixels_XY( uTextureSlotNumber, uTextureSize, uDebugDigitsStartXY + uDebugDigitSize * vec2( 1.5, 0.5 ) );
	}
}

// inverse cumulative Gaussian - converts uniform random variate in interval (0,1) to Gaussian with mean 0 and variance 1
float invcg( float x )
{
	
	x = 2.0 * x - 1.0;
	//x = min( 0.9999, max( -0.9999, x ) ); // seems to be necessary to avoid a few overflows, depending on the RNG
	// Now we will use MBG_erfinv as defined by Mike Giles in https://people.maths.ox.ac.uk/gilesm/files/gems_erfinv.pdf
	// and multiply by sqrt(2) at the end
	float w, p;
	w = -log( ( 1.0 - x ) * ( 1.0 + x ) );
	if ( w < 5.0 )
	{
		w = w - 2.5;
		p =  2.81022636e-08;
		p =  3.43273939e-07 + p * w;
		p = -3.5233877e-06  + p * w;
		p = -4.39150654e-06 + p * w;
		p =  0.00021858087  + p * w;
		p = -0.00125372503  + p * w;
		p = -0.00417768164  + p * w;
		p =  0.246640727    + p * w;
		p =  1.50140941     + p * w;
	}
	else
	{
		w = sqrt( w ) - 3.0;
		p = -0.000200214257;
		p =  0.000100950558 + p * w;
		p =  0.00134934322  + p * w;
		p = -0.00367342844  + p * w;
		p =  0.00573950773  + p * w;
		p = -0.0076224613   + p * w;
		p =  0.00943887047  + p * w;
		p =  1.00167406     + p * w;
		p =  2.83297682     + p * w;
	}
	return 1.4142135623730951 * p * x;
}

float sinusoid( vec2 coord, float cyclesPerPixel, float orientationDegrees, float phaseDegrees )
{
	float orientationRadians = orientationDegrees * RADIANS_PER_DEGREE;
	float x = dot( coord, vec2( cos( orientationRadians ), sin( orientationRadians ) ) );
	return sin( phaseDegrees * RADIANS_PER_DEGREE + TWO_PI * cyclesPerPixel * x );
}

float SinewaveSignal( vec2 coord )
{
	// vec4 uSignalParameters is interpreted as:
	//     amplitude:   signal multiplier. In general, its absolute value should not exceed min( .bg, 1-.bg )
	//                  (although note that the multiplier is also scaled by uColor, if used, and by uNormalizedContrast)
	//     frequency:   spatial frequency in cycles per pixel,
	//     orientation: in degrees (0 is means modulation along the horizontal axis, i.e. vertical stripes)
	//     phase:       in degrees (0 is sine phase at the center of the envelope)
	return uSignalParameters[ 0 ] * sinusoid( coord, uSignalParameters[ 1 ], uSignalParameters[ 2 ], uSignalParameters[ 3 ] );
}

float SinewaveModulation( vec2 coord )
{
	// vec4 uModulationParameters is interpreted as:
	//     depth:       modulation depth from 0 to 1,
	//     frequency:   spatial frequency in cycles per pixel,
	//     orientation: in degrees (0 is means modulation along the horizontal axis, i.e. vertical stripes)
	//     phase:       in degrees (0 is sine phase at the center of the envelope)
	return 1.0 + uModulationParameters[ 0 ] * 0.5 * ( sinusoid( coord, uModulationParameters[ 1 ], uModulationParameters[ 2 ], uModulationParameters[ 3 ] ) - 1.0 );
}

//#CUSTOM_FUNCTIONS

vec3 TintSignal( vec3 signal, vec3 tint )
{
	if( tint.r >= 0.0 ) signal.r *= tint.r;
	if( tint.g >= 0.0 ) signal.g *= tint.g;
	if( tint.b >= 0.0 ) signal.b *= tint.b;
	// NB: could multiply by ( uColor.r - uBackgroundColor.r ) and friends instead of just uColor.r
	//     that would mean that at siga=1, a signal value of 1 arrives at the target uColor
	//     whereas this is more like color addition.  Color addition turns out to be a little more
	//     intuitive when the bg is not 0.5
	return signal;
}
vec3 TintSignal( float signal, vec3 tint )
{
	return TintSignal( vec3( signal, signal, signal ), tint );
}

void main(void)
{
	if( !uShady )
	{
		gl_FragColor = texture2D( uTextureSlotNumber, vTextureCoordinates );
		return;
	}

	vec2 coord2D = ( uCarrierTransformation * vFragCoordinateInEnvelope ).xy;
	
	float debugValue; // if debug-digits have been requested, get the debug value from the texture coordinates requested on the CPU side
	
	
	if( uUseTexture )
	{
		vec2 debugOffset = vec2( -uCarrierTransformation[ 2 ].y, uCarrierTransformation[ 2 ].x );
		// TODO: this is a temporary cop-out: apply all carrier transformations to debug coordinates?
		if( uDebugDigitsStartXY.x >= 0.0 ) debugValue = Texture_Pixels_IJ( uTextureSlotNumber, uTextureSize, uDebugValueIJK.xy + debugOffset )[ int( uDebugValueIJK.z ) ];
		// (for debugging of this shader itself, you can always temporarily override debugValue - the actual rendering happens on the last line of the main(), below)
	
		// Get the base pixel color according to the carrier texture
		gl_FragColor = Texture_Pixels_XY( uTextureSlotNumber, uTextureSize, coord2D );
		if( uColor.r >= 0.0 ) gl_FragColor.r *= uColor.r;
		if( uColor.g >= 0.0 ) gl_FragColor.g *= uColor.g;
		if( uColor.b >= 0.0 ) gl_FragColor.b *= uColor.b;
	}
	else
	{
		gl_FragColor = vec4( uBackgroundColor, 1.0 );
		if( uSignalFunction == 0 ) // only apply fg if not rippling, because signal is additive and assumes bg is the base
		{
			if( uColor.r >= 0.0 ) gl_FragColor.r = uColor.r;
			if( uColor.g >= 0.0 ) gl_FragColor.g = uColor.g;
			if( uColor.b >= 0.0 ) gl_FragColor.b = uColor.b;
		}
	}
	// Add offset to luminance if desired
	gl_FragColor.rgb += uOffset;
	if( uSignalFunction != 0 )
	{
		vec2 xy = coord2D - uEnvelopeSize / 2.0;
		vec3 signal;
		if( uSignalFunction == 1 ) signal = TintSignal( SinewaveSignal( xy ), uColor );
//#SIGNAL_FUNCTION_CALLS
		gl_FragColor.rgb += signal;
	}
	
	// Apply contrast multiplier
	float lambda = uNormalizedContrast;
	
	// ...incorporating the spatial window, if any:
	vec2 v = 2.0 * vFragCoordinateInEnvelope.xy - uEnvelopeSize;
	vec2 pp = uPlateauProportion;
	if( pp.x < 0.0 || pp.x > 1.0 ) { v.x = 0.0; pp.x = 1.0; }
	if( pp.y < 0.0 || pp.y > 1.0 ) { v.y = 0.0; pp.y = 1.0; }
	float vlen = length( v );
	if( vlen != 0.0 )
	{
		vec2 vn = v / vlen;
		vec2 ellipseAxes = uEnvelopeSize * pp;
		float r_inner = ellipseAxes.x * ellipseAxes.y * InverseLength( ellipseAxes.yx * vn ); // inner radius, in same units as v along the direction of v
		float r_outer = uEnvelopeSize.x * uEnvelopeSize.y / length( uEnvelopeSize.yx * vn ); // outer radius, in same units as v along the direction of v - option A
		//float r_outer = r_inner / max( pp.x, pp.y ); // outer radius, in same units as v along the direction of v - option B
		float rlen = vlen - r_inner;
		if( r_outer > r_inner ) rlen /= r_outer - r_inner;
		lambda *= 0.5 + 0.5 * cos( PI * max( 0.0, min( 1.0, rlen ) ) );
	}

	// ...and sinusoidal amplitude modulation, if desired:
	if( uModulationFunction != 0 )
	{
		float f = 1.0;
		vec2 xy = coord2D - uEnvelopeSize / 2.0;
		if( uModulationFunction == 1 ) f = SinewaveModulation( xy );
//#MODULATION_FUNCTION_CALLS
		lambda *= f;
	}
	// Scale according to windowing, amplitude modulation and overall contrast multipliers:
	if( uBackgroundAlpha == 1.0 ) // NB: use this option for linearized stimuli
	{
		gl_FragColor.rgb *= lambda;
		gl_FragColor.rgb += ( 1.0 - lambda ) * uBackgroundColor;
	}
	else // use this for fading stimuli out, but beware that OpenGL's native alpha-blending will happen POST-linearization, making things non-linear
	{
		gl_FragColor.a *= lambda * 1.0 + (1.0 - lambda) * uBackgroundAlpha;
		/*
		
		It's tempting to try and correct alpha here, but 'ere be dragons:
		
		In principle,  if you want foreground luminance f and background luminance b, you can
		achieve a given contrast via alpha manipulation alone if you use an adjustedAlpha such that:
		
		    Luminance = Gamma( adjustedAlpha * InvGamma(f)  +  (1-adjustedAlpha) * InvGamma(b) )
		              = lambda * f + (1-lambda) * b
		
		However, this makes two big assumptions:
		
		(1) the actual background (i.e. the luminance corresponding to the screen glClearColor, or
		    the luminance of whatever other stimulus happens to be showing through in regions where
		    your gl_FragColor.a < 1.0) matches the uBackgroundColor that you have specified for this
		    stimulus - which it might, but it won't be under the control of this stimulus.
		    
		(2) InvGamma(f) is the same for all color channels,  and InvGamma(b) is the same for all color
		    channels.  Both of these terms will be used to compute adjustedAlpha but there's only one
		    slot, gl_FragColor.a,  to store the resulting alpha value.  That had better be right for
		    all channels, which it will only be (except by coincidence) for achromatic stimuli rendered
		    on screens that have achromatic nonlinearities.
		
		Assumption (2) is satisfied, and in fact the correction is unnecessary because adjustedAlpha is
		the same as nominal alpha,  in the special cases of alpha=0 and alpha=1. So if you have full
		contrast and a boxcar window, or full-depth square-wave contrast modulation, then you only have
		to worry about assumption (1). All bets are off at intermediate alpha values, however.  
		*/
	}
	
	// Add noise if desired
	bool useUniformNoise  = uNoiseAmplitude.r < 0.0 || uNoiseAmplitude.g < 0.0 || uNoiseAmplitude.b < 0.0;
	bool useGaussianNoise = uNoiseAmplitude.r > 0.0 || uNoiseAmplitude.g > 0.0 || uNoiseAmplitude.b > 0.0;
	if( useUniformNoise || useGaussianNoise )
	{
		const float nFrames = 60.0 * 15.0;
		float frame = float( uFramesCompleted );
		float n = random( vec3( ( 1.0 + vFragCoordinateInEnvelope.xy ) / ( 2.0 + uTextureSize ), ( 1.0 + mod( frame, nFrames ) ) / ( 2.0 + nFrames ) ) );
		// NB: noise will be the same for all textures: is that a problem?
		float uniformNoise, gaussianNoise;
		if( useUniformNoise  ) uniformNoise  = 2.0 * n - 1.0;
		if( useGaussianNoise ) gaussianNoise = invcg( n );
		gl_FragColor.r += uNoiseAmplitude.r * ( uNoiseAmplitude.r < 0.0 ? uniformNoise : gaussianNoise );
		gl_FragColor.g += uNoiseAmplitude.g * ( uNoiseAmplitude.g < 0.0 ? uniformNoise : gaussianNoise );
		gl_FragColor.b += uNoiseAmplitude.b * ( uNoiseAmplitude.b < 0.0 ? uniformNoise : gaussianNoise );
	}
	
	// Linearize	
	gl_FragColor.r = Linearize( gl_FragColor.r, uGamma.r );
	gl_FragColor.g = Linearize( gl_FragColor.g, uGamma.g );
	gl_FragColor.b = Linearize( gl_FragColor.b, uGamma.b );

	// Apply lookup table, if any
	if( uLookupTableTextureSize.z > 0.0 )
	{
		float maxIndex = uLookupTableTextureSize.z - 1.0;
		float index = floor( 0.5 + max( 0.0, min( 1.0, gl_FragColor.r ) ) * maxIndex );
		vec2 coordsIJ = vec2( mod( index, uLookupTableTextureSize.y ), floor( index / uLookupTableTextureSize.y ) );
		gl_FragColor = Texture_Pixels_IJ( uLookupTableTextureSlotNumber, uLookupTableTextureSize.xy, coordsIJ );
	}

	gl_FragColor.a *= uAlpha;
	
	const float lo = 0.0 - 1.0e-3; // we can afford to be surprisingly lax with the tolerance at this point, because
	const float up = 1.0 + 1.0e-3; // OpenGL is about to round everything to 8-bit RGB anyway, so it makes no difference
	                               // if we're off by anything up to half a grey-level (0.5/255 = 1.96e-3)
	if( gl_FragColor.r < lo || gl_FragColor.r > up || gl_FragColor.g < lo || gl_FragColor.g > up || gl_FragColor.b < lo || gl_FragColor.b > up )
	{
		if( uOutOfRangeColor.r >= 0.0 ) gl_FragColor.r = uOutOfRangeColor.r;
		if( uOutOfRangeColor.g >= 0.0 ) gl_FragColor.g = uOutOfRangeColor.g;
		if( uOutOfRangeColor.b >= 0.0 ) gl_FragColor.b = uOutOfRangeColor.b;
		if( uOutOfRangeAlpha   >= 0.0 ) gl_FragColor.a = uOutOfRangeAlpha;
	}
	
	// Render debugValue if debug-digits are requested
	if( uUseTexture && uDebugDigitsStartXY.x >= 0.0 ) RenderDecimal( debugValue );
}
