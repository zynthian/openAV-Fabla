#!/bin/python3

# ******************************************************************************
# TTL generator for fabla LV2 plugin
#
# This program generates the fabla plugin's TTL with a
# configurable number of pads, passed as argument.
#
# Copyright (C) 2025 Fernando Moyano <jofemodo@zynthian.org>
#
# ******************************************************************************
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a full copy of the GNU General Public License see the LICENSE.txt file.
#
# ******************************************************************************

import sys

try:
	num_pads = int(sys.argv[1])
except:
	num_pads = 16

plugin_uri = "http://www.openavproductions.com/fabla"

ttl = f"""@prefix atom:  <http://lv2plug.in/ns/ext/atom#> .
@prefix doap:  <http://usefulinc.com/ns/doap#> .
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .
@prefix lv2:   <http://lv2plug.in/ns/lv2core#> .
@prefix state: <http://lv2plug.in/ns/ext/state#> .
@prefix ui:    <http://lv2plug.in/ns/extensions/ui#> .
@prefix urid:  <http://lv2plug.in/ns/ext/urid#> .
@prefix work:  <http://lv2plug.in/ns/ext/worker#> .
@prefix time:  <http://lv2plug.in/ns/ext/time#> .
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rsz:   <http://lv2plug.in/ns/ext/resize-port#> .
@prefix midi:  <http://lv2plug.in/ns/ext/midi#> .
@prefix patch: <http://lv2plug.in/ns/ext/patch#> .
@prefix param: <http://lv2plug.in/ns/ext/parameters#> .
@prefix mod:   <http://moddevices.com/ns/mod#> .
@prefix pg:    <http://lv2plug.in/ns/ext/port-groups#> .
@prefix plug:  <{plugin_uri}#> .

<http://openavproductions.com/about>
  a foaf:Person ;
  foaf:name "Harry van Haaren" ;
  foaf:mbox <mailto:harryhaaren@gmail.com> ;
  foaf:homepage <http://openavproductions.com> .

<{plugin_uri}/gui>
  a ui:X11UI ;
  lv2:requiredFeature urid:map , ui:idleInterface ;
  lv2:optionalFeature ui:noUserResize ;
  lv2:extensionData ui:idleInterface ;
  
  ui:portNotification [
    ui:plugin <{plugin_uri}> ;
    lv2:symbol "notify" ;
    ui:notifyType atom:Blank
  ] .

plug:GROUP_MASTER
  a pg:InputGroup;
  lv2:index 1 ;
  lv2:displayPriority 100 ;
  lv2:name "Master" ;
  lv2:symbol "group_master" .

plug:GROUP_COMPRESSOR
  a pg:InputGroup;
  lv2:index 2 ;
  lv2:displayPriority 99 ;
  lv2:name "Compressor" ;
  lv2:symbol "group_compressor" .
"""

# Generate pad groups:
for i in range(num_pads):
  ttl += f"""
plug:GROUP_PAD{1 + i}_MAIN
  a pg:InputGroup;
  lv2:index {3 + i} ;
  lv2:displayPriority {80 - i} ;
  lv2:name "Pad {1 + i} - Main" ;
  lv2:symbol "group_pad{1 + i}_main" .

plug:GROUP_PAD{1 + i}_ADSR
  a pg:InputGroup;
  lv2:index {4 + i} ;
  lv2:displayPriority {79 - i} ;
  lv2:name "Pad {1 + i} - ADSR" ;
  lv2:symbol "group_pad{1 + i}_adsr" .
"""


# Generate pad fpaths
for i in range(num_pads):
  ttl += f"""
plug:pad_fpath_{1 + i}
  a lv2:Parameter;
  lv2:displayPriority 4 ;
  pg:group plug:GROUP_PAD{1 + i}_MAIN ;
  mod:fileTypes "wav,aiff,flac";
  rdfs:label "Sample {1 + i}";
  rdfs:range atom:Path.
"""

# Plugin header
ttl += f"""
<{plugin_uri}>
  a lv2:InstrumentPlugin ;
  doap:name "Fabla" ;
  doap:license <https://spdx.org/licenses/GPL-2.0.html>;
  doap:description "Performance Sampler" ;
  doap:maintainer <http://openavproductions.com/about>;

  lv2:microVersion 2 ;
  lv2:minorVersion 3 ;
  
  lv2:binary <fabla.so> ;
  lv2:requiredFeature urid:map;
  
  lv2:optionalFeature work:schedule ;
  lv2:optionalFeature lv2:hardRTCapable ;
  
  lv2:extensionData state:interface ;
  
  ui:ui <{plugin_uri}/gui> ;  
"""

# Plugin patch writable
ttl += """
  patch:writable
"""
for i in range(num_pads):
  ttl += f"    plug:pad_fpath_{1 + i},\n"
ttl = ttl[:-2] + ";\n\n"

# Plugin ports (not pad ports)
ttl += """  lv2:port [
    a lv2:InputPort ,
      atom:AtomPort ;
    rsz:minimumSize 13448 ;
    atom:bufferType atom:Sequence ;
    atom:supports time:Position ;
    atom:supports midi:MidiEvent,
      patch:Message;
    lv2:index 0 ;
    lv2:designation lv2:control ;
    lv2:symbol "control" ;
    lv2:name "Control"
  ] , [
    a lv2:OutputPort ,
      atom:AtomPort ;
    atom:bufferType atom:Sequence ;
    atom:supports patch:Message;
    lv2:index 1 ;
    lv2:symbol "notify" ;
    lv2:name "Notify";
  ] , [
    a lv2:AudioPort ,
      lv2:OutputPort ;
    lv2:index 2 ;
    lv2:symbol "left" ;
    lv2:name "Audio Output Left";
  ] , [
    a lv2:AudioPort ,
      lv2:OutputPort ;
    lv2:index 3 ;
    lv2:symbol "right" ;
    lv2:name "Audio Output Right";
  ] , [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index 4 ;
    lv2:symbol "volume" ;
    lv2:name "Master";
    lv2:default 0.75;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:displayPriority 4 ;
    pg:group plug:GROUP_MASTER ;
  ] , [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index 5 ;
    lv2:symbol "base_note" ;
    lv2:name "Base Note";
    lv2:default 36.0;
    lv2:minimum 0.0 ;
    lv2:maximum 63.0 ;
    lv2:displayPriority 3 ;
    pg:group plug:GROUP_MASTER ;
  ] , [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index 6 ;
    lv2:symbol "compressor_attack" ;
    lv2:name "Compressor Attack";
    lv2:default 0.15 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:displayPriority 2 ;
    pg:group plug:GROUP_COMPRESSOR ;
  ] , [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index 7 ;
    lv2:symbol "compressor_decay" ;
    lv2:name "Compressor Decay";
    lv2:default 0.3 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:displayPriority 1 ;
    pg:group plug:GROUP_COMPRESSOR ;
  ] , [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index 8 ;
    lv2:symbol "compressor_threshold" ;
    lv2:name "Compressor Threshold";
    lv2:default 0.5 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:displayPriority 3 ;
    pg:group plug:GROUP_COMPRESSOR ;
  ] , [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index 9 ;
    lv2:symbol "compressor_ratio" ;
    lv2:name "Compressor Ratio";
    lv2:default 0.5 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:displayPriority 4 ;
    pg:group plug:GROUP_COMPRESSOR ;
  ] , [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index 10 ;
    lv2:symbol "compressor_makeup" ;
    lv2:name "Compressor Makeup";
    lv2:default 0.5 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:displayPriority 2 ;
    pg:group plug:GROUP_MASTER ;
  ] , [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index 11 ;
    lv2:symbol "compressor_enable" ;
    lv2:name "Compressor Enable";
    lv2:default 0.0 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:scalePoint [
      rdf:value 0.0 ;
      rdfs:label "OFF" ;
      rdfs:comment "OFF" ;
    ], [
      rdf:value 1.0 ;
      rdfs:label "ON" ;
      rdfs:comment "ON" ;
    ];
    lv2:displayPriority 1 ;
    pg:group plug:GROUP_MASTER ;
  ]
  ,
 """

port_index = 12

# Plugin ports (pad gain ports)
for i in range(num_pads):
  ttl += f""" [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index {port_index};
    lv2:symbol "pad_gain_{1 + i}" ;
    lv2:name "Gain {1 + i}";
    lv2:default 0.5 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:displayPriority 3 ;
    pg:group plug:GROUP_PAD{1 + i}_MAIN ;
  ] ,"""
  port_index += 1

# Plugin ports (pad speed ports)
for i in range(num_pads):
  ttl += f""" [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index {port_index};
    lv2:symbol "pad_speed_{1 + i}" ;
    lv2:name "Speed {1 + i}";
    lv2:default 0.5 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:displayPriority 1 ;
    pg:group plug:GROUP_PAD{1 + i}_MAIN ;
  ] ,"""
  port_index += 1

# Plugin ports (pad pan ports)
for i in range(num_pads):
  ttl += f""" [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index {port_index};
    lv2:symbol "pad_pan_{1 + i}" ;
    lv2:name "Pan {1 + i}";
    lv2:default 0.5 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:displayPriority 2 ;
    pg:group plug:GROUP_PAD{1 + i}_MAIN ;
  ] ,"""
  port_index += 1

# Plugin ports (pad attack ports)
for i in range(num_pads):
  ttl += f""" [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index {port_index};
    lv2:symbol "pad_attack_{1 + i}" ;
    lv2:name "Attack {1 + i}";
    lv2:default 0.0 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:designation param:attack ;
    lv2:displayPriority 4 ;
    pg:group plug:GROUP_PAD{1 + i}_ADSR ;
  ] ,"""
  port_index += 1

# Plugin ports (pad decay ports)
for i in range(num_pads):
  ttl += f""" [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index {port_index};
    lv2:symbol "pad_decay_{1 + i}" ;
    lv2:name "Decay {1 + i}";
    lv2:default 0.5 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:designation param:decay ;
    lv2:displayPriority 3 ;
    pg:group plug:GROUP_PAD{1 + i}_ADSR ;
  ] ,"""
  port_index += 1

# Plugin ports (pad sustain ports)
for i in range(num_pads):
  ttl += f""" [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index {port_index};
    lv2:symbol "pad_sustain_{1 + i}" ;
    lv2:name "Sustain {1 + i}";
    lv2:default 1.0 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:designation param:sustain ;
    lv2:displayPriority 2 ;
    pg:group plug:GROUP_PAD{1 + i}_ADSR ;
  ] ,"""
  port_index += 1

# Plugin ports (pad release ports)
for i in range(num_pads):
  ttl += f""" [
    a lv2:ControlPort ,
      lv2:InputPort ;
    lv2:index {port_index};
    lv2:symbol "pad_release_{1 + i}" ;
    lv2:name "Release {1 + i}";
    lv2:default 0.5 ;
    lv2:minimum 0.0 ;
    lv2:maximum 1.0 ;
    lv2:designation param:release ;
    lv2:displayPriority 1 ;
    pg:group plug:GROUP_PAD{1 + i}_ADSR ;
  ] ,"""
  port_index += 1

# End with dot
ttl = ttl[:-1] + ".\n"

print(ttl)
