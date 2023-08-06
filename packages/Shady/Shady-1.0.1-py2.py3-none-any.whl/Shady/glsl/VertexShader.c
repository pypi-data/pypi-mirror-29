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
varying vec3 vFragCoordinateInEnvelope;
varying vec2 vTextureCoordinates;

void main(void)
{
	vFragCoordinateInEnvelope = vec3( gl_Vertex.xy, 1.0 );
	vTextureCoordinates = gl_MultiTexCoord0.st; // TODO: 0 is hardcoded here - how do we know which texture unit to use?
	
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex; // TODO: is there a way of shortcutting this matrix multiplication...?
}
