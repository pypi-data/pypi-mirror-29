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

// Uniform (0, 1) random noise solution by SO user Spatial:  https://stackoverflow.com/a/17479300/
// NB:  uintBitsToFloat and floatBitsToUint require GLSL 3.3+
// A single iteration of Bob Jenkins' One-At-A-Time hashing algorithm.
uint hash( uint x )
{
	x += ( x << 10u );
	x ^= ( x >>  6u );
	x += ( x <<  3u );
	x ^= ( x >> 11u );
	x += ( x << 15u );
	return x;
}
// Compound versions of the hashing algorithm whipped together by Spatial.
uint hash( uvec2 v ) { return hash( v.x ^ hash( v.y )                             ); }
uint hash( uvec3 v ) { return hash( v.x ^ hash( v.y ) ^ hash( v.z )               ); }
uint hash( uvec4 v ) { return hash( v.x ^ hash( v.y ) ^ hash( v.z ) ^ hash( v.w ) ); }
// Construct a float with half-open range [0:1] using low 23 bits.
// All zeroes yields 0.0, all ones yields the next smallest representable value below 1.0.
float floatConstruct( uint m )
{
	const uint ieeeMantissa = 0x007FFFFFu; // binary32 mantissa bitmask
	const uint ieeeOne      = 0x3F800000u; // 1.0 in IEEE binary32

	m &= ieeeMantissa;                     // Keep only mantissa bits (fractional part)
	m |= ieeeOne;                          // Add fractional part to 1.0

	float  f = uintBitsToFloat( m );       // Range [1:2]
	return f - 1.0;                        // Range [0:1]
}
// Pseudo-random value in half-open range [0:1]
float random( float x ) { return floatConstruct( hash( floatBitsToUint( x ) ) ); }
float random( vec2  v ) { return floatConstruct( hash( floatBitsToUint( v ) ) ); }
float random( vec3  v ) { return floatConstruct( hash( floatBitsToUint( v ) ) ); }
float random( vec4  v ) { return floatConstruct( hash( floatBitsToUint( v ) ) ); }
