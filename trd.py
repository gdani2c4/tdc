import sys, json, re

def main():
	achvo_prog_nom = sys.argv[1]
	trdv_ant_nom = sys.argv[2]
	trdv_nv = []
	rstdo = {}
	print( sys.argv[2] )
	achvo_prog = { "ficha_v": [], "achvo_cda": "" }
	# achvo_cda	el archivo del programa que está
	#	para traducir
	achvo_prog_leer( achvo_prog_nom, achvo_prog )
	as_achvo_prog( achvo_prog, trdv_nv )
	print( trdv_nv )
#	# depuración: imprimir las cadenas encontradas
#	for ii in rstdo["trdv_nv"]:
#		for kk in range(len(achvo_prog["ficha_v"])):
#			if ii.group("fch%d" % kk):
#				print( ii.group("fch%d" % kk))
	rstdo = {"trdv_ant": []}
	trdv_ant_leer( trdv_ant_nom, rstdo )
#	trdv_unir( rstdo["trdv_ant"], trdv_nv )

ficha_dat = {
"js": [
	{ "fa": '"',	"fc": '"' },
	{ "fa": '\'',	"fc": '\'' },
	{ "fa": '`',	"fc": '`' },
	{ "fa": "/\*",	"fc": "\*/" , "sin_esc": 1 },
	{ "fa": "//",	"fc": '\n' , "sin_esc": 1 } ],
"py": [
	{ "fa": '"',	"fc": '"' },
	{ "fa": '\'',	"fc": '\'' },
	{ "fa": '#',	"fc": '\n', "sin_esc": 1 } ]
}

def achvo_prog_leer( achvo_nom, rstdo ):
	rstdo["ficha_v"] = ficha_dat["js"]
	rstdo["achvo_cda"] = "".join(
		[ii for ii in open( achvo_nom )] )

def as_achvo_prog( achvo_prog, rstdo ):
#	rstdo["trdv_nv"] = \
	re_rstdo = \
	re.finditer( "".join(
		# dejé un grupo "xx" para "fch + cda + fch" entero
		[	( "(?P<xx%(val)s>%(fa)s" +\
			"(?P<fch%(val)s>%(cnd)s)" + "%(fc)s)|" )\
			% {
				"fa":ii["fa"], "fc":ii["fc"],
				"val": achvo_prog["ficha_v"].index(ii),
				"cnd": ".*?" if "sin_esc" in ii else \
					r"(.*?[^\\](\\\\)*)|(\\\\)*"
			}  for ii in achvo_prog["ficha_v"]
		]
	)[:-1], achvo_prog["achvo_cda"], re.DOTALL )
	for ii in re_rstdo:
		for kk in range( len(achvo_prog["ficha_v"] ) ):
			if ii.group( "fch%d" % kk ):
				rstdo.append(
					ii.group( "fch%d" % kk ) )

def trdv_ant_leer( trdv_ant_nom, rstdo ):
	rstdo[ "trdv_ant" ] = json.load( open(
		trdv_ant_nom ) )

#dev trdv_unir( trdv_ant, trdv_nv )
#	for ii in trdv_ant:

if __name__ == "__main__":
	main()
