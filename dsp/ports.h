/*
 * Author: Harry van Haaren 2013
 *         harryhaaren@gmail.com
 * Modified: Fernando Moyano 2024-2025
 *         fernando@zynthian.org
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 */

#ifndef FABLA_PORTS_H
#define FABLA_PORTS_H

// Plugin's URI
#define FABLA_URI    "http://www.openavproductions.com/fabla"
#define FABLA_UI_URI "http://www.openavproductions.com/fabla/gui"

#define NPADS 64

typedef enum {
  ATOM_IN= 0,
  ATOM_OUT= 1,
  
  AUDIO_OUT_L= 2,
  AUDIO_OUT_R= 3,
  
  MASTER_VOL= 4,
  BASE_NOTE= 5,
  
  COMP_ATTACK= 6,
  COMP_DECAY= 7,
  COMP_THRES= 8,
  COMP_RATIO= 9,
  COMP_MAKEUP= 10,
  COMP_ENABLE= 11,
  
  // p*2... is to place hold that index for the functionality before.
  // Actual interaction with the value is by comparison of "port" variable
  // reading:
  //    if ( port > PAD_GAIN && port < PAD_GAIN + NPADS )
  // writing:
  //    write( int(PAD_GAIN) + padNumber, &value );
  
  PAD_GAIN= 12,  
  PAD_SPEED= 12 + NPADS,  
  PAD_PAN= 12 + 2 * NPADS,
  PAD_ATTACK= 12 + 3 * NPADS,  
  PAD_DECAY= 12 + 4 * NPADS,  
  PAD_SUSTAIN= 12 + 5 * NPADS,  
  PAD_RELEASE= 12 + 6 * NPADS
} PortIndex;

#define NUM_PORTS 12 + 7 * NPADS

#endif // FABLA_PORTS_H

