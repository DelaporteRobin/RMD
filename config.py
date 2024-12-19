# -*- coding: utf-8 -*-
#CONFIG FILE CONTAINING ALL MAIN VARIABLES ANND SETTINGS FOR THE RMD APP
import Imath
import os


#GLOBAL INFORMATIONS
VERSION = 0.2
AUTHOR = "DelaporteRobin"
REPO = "https://github.com/DelaporteRobin/RMD"

ASCII_FONT_LOBBY = "ansi_shadow"
ASCII_FONT_TERMINAL = "ansi_shadow"


#WELCOME TEXT
WELCOME = """
Welcome in RMD - Renderman Denoiser
Version --> %s
Writen by --> %s

Go star the Repo to support my work
%s

"""%(VERSION, AUTHOR, REPO)


PIXAR_PATH = "C:/Program Files/Pixar/RenderManProServer-26.2"


AOV_REQUIRED = [
	"Ci",
	"a", 
	"mse",
	"sampleCount",
	"albedo",
	"albedo_mse",
	"diffuse",
	"diffuse_mse",
	"specular",
	"specular_mse",
	"normal",
	"normal_mse"
	]

AOV_KEYWORD = {
	"a": ["a"],
	"albedo":["albedo", "albedo_var", "albedo_mse"],
	"diffuse": ["diffuse","Diffuse","diffuse_mse","normal","forward","backward"],
	"specular": ["specular","Specular", "specular_mse"],
	"color": ["beauty","Ci","subsurface","glass","Glass","transmissive"],
	"sampleCount":["sampleCount"],
	"mse": ["mse"],
	"zfiltered": ["zfiltered"],
	"zfiltered_var": ["zfiltered_var"],
	"normal_var":["normal_var"],
	"normal_mse":["normal_mse"],
}

COMPRESSION_ALGORYTHM = {
	"DWAB_COMPRESSION" : Imath.Compression.DWAB_COMPRESSION,
	"RLE_COMPRESSION": Imath.Compression.RLE_COMPRESSION,
	"ZIP_COMPRESSION": Imath.Compression.ZIP_COMPRESSION,
	"ZIPS_COMPRESSION": Imath.Compression.ZIPS_COMPRESSION,
	"PIZ_COMPRESSION": Imath.Compression.PIZ_COMPRESSION,
	"PXR24_COMPRESSION":Imath.Compression.PXR24_COMPRESSION,
	"B44_COMPRESSION":Imath.Compression.B44_COMPRESSION,
	"B44A_COMPRESSION":Imath.Compression.B44A_COMPRESSION,
	"DWAA_COMPRESSION":Imath.Compression.DWAA_COMPRESSION,
	"DWAB_COMPRESSION": Imath.Compression.DWAB_COMPRESSION,	
	}


DENOISE_SETTINGS = {
	"DENOISE_INPUT": True,
	"CROSSFRAME": True,
	"COMBINE": True,
	"COMPRESS": True,
}