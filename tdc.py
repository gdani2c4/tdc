import sys, json, re
msj_uso = (	"Uso: tdc [OPCIÓN] [ARCHIVO]...\n"
			"traducir ARCHIVO(s) mediante la lista de "
			"traducción $PWD/dat/tdc.json.\n"
			"-a	actualizar la lista de traducción\n	"
			"	mediante ARCHIVO(s) de programación actualizados.\n"
			"-t	traducir ARCHIVO(s) y guardar en "
			"camino/de/ARCHIVO/tdc." )
from datetime import datetime
err_ach_de_tdc_predet = (
	"[¡] no se encontró el archivo \"./dat/tdc.json\" "
	"en el directorio actual (el \"$PWD\") [!]" )
# opc_v	vector de opciones existentes del comando
# "modo":	opciones de modo, "t" y "a"
opc = {"modo": ["a", "t"] }

def main():
	ach_prog_nomv = []
	opc_x = {}
	rstdo = {}
	as_argv( sys.argv[1:], rstdo, opc_x )
	ach_prog_nomv = rstdo[ "ach_prog_nomv" ]
	if opc_x["modo"] == "a":
		act_tdc_dat( ach_prog_nomv )
	elif opc_x["modo"] == "t":
		tdc_achos_prog( ach_prog_nomv )

def act_tdc_dat( ach_prog_nomv ):
	ach_prog = {}
	tdcv_nv = { "cda": {} }
	tdcv_ant = {}
	rstdo = {}
	for ach_prog_nom in ach_prog_nomv:
		# ach_cda	el archivo del programa que
		#	está para traducir
		ach_prog = { "ficha_v": [], "ach_cda": "" }
		ach_prog_leer( ach_prog_nom, ach_prog )
		as_ach_prog( ach_prog, tdcv_nv )
	tdcv_ant_leer( rstdo )
	tdcv_ant = rstdo["tdcv_ant"]
	tdcv_unir( tdcv_ant, tdcv_nv )
	json.dumps( tdcv_nv, indent = 4 )
	tdcv_escr( tdcv_nv, tdcv_ant )

def tdc_achos_prog( ach_prog_nomv ):
	pass

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

def ach_prog_leer( ach_nom, rstdo ):
	rstdo["ficha_v"] = ficha_dat["js"]
	with open( ach_nom ) as ach_prog:
		rstdo["ach_cda"] = ach_prog.read()

def as_ach_prog( ach_prog, tdcv_nv ):
	re_rstdo = \
	re.finditer( "".join(
		# dejé un grupo "xx" para "fch + cda + fch" entero
		[	( "(?P<xx%(val)s>%(fa)s" +\
			"(?P<fch%(val)s>%(cnd)s)" + "%(fc)s)|" )\
			% {
				"fa":ii["fa"], "fc":ii["fc"],
				"val": ach_prog["ficha_v"].index(ii),
				"cnd": ".*?" if "sin_esc" in ii else \
					r"(\\\\)*|(.*?[^\\](\\\\)*)"

			}  for ii in ach_prog["ficha_v"]
		]
	)[:-1], ach_prog["ach_cda"], re.DOTALL )
	for ii in re_rstdo:
		for kk in range( len(ach_prog["ficha_v"] ) ):
			if ii.group( "fch%d" % kk ):
				tdcv_nv["cda"][
					ii.group( "fch%d" % kk ) ] = ""

def tdcv_ant_leer( rstdo, tdc_nom_ach = "dat/tdc.json" ):
	with open( tdc_nom_ach ) as ach_tdc:
		try:
			rstdo["tdcv_ant"] = json.load( ach_tdc )
		except FileNotFoundError:
			print( err_ach_de_tdc_predet )
			exit( -1 )

def tdcv_unir( tdcv_ant, tdcv_nv ):
	tdcv_nv["abrv"] = {}
	for ii in tdcv_nv["cda"]:
		if ii in tdcv_ant["cda"]:
			tdcv_nv["cda"][ ii ] = tdcv_ant["cda"][ ii ]
	tdcv_nv["abrv"] = tdcv_ant["abrv"]

def tdcv_escr( tdcv_nv, tdcv_ant,
		tdc_nom_ach = "dat/tdc.json" ):
	with open( tdc_nom_ach + \
		datetime.now().strftime("%d%m%y_%H%M"), "w" )\
		as ach:
		ach.write( json.dumps( tdcv_ant, indent = 4,
			ensure_ascii = 0 ) )
	with open( tdc_nom_ach, "w" ) as ach:
		ach.write( json.dumps( tdcv_nv, indent = 4,
			ensure_ascii = 0, separators = (",\n", ":\n") ) )

def as_argv( argv_n, rstdo, opc_x ):
	# [25-01-20] prueba programarlo con iteradores
	if len( argv_n ) == 0: err( "faltan argumentos" )
	if argv_n[0][0] == "-":
		if argv_n[0][1:] in opc["modo"]:
			opc_x["modo"] = argv_n[0][1:]
			as_argv( argv_n[1:], rstdo, opc_x )
		elif argv_n[0][1:] == "h":
			print(msj_uso)
			exit(0)
		else: err( "opción %s desconocida" % argv_n[0] )
	elif not ( "modo" in opc_x ):
		err( "no se encontró ninguna opción" )
	else:
		rstdo["ach_prog_nomv"] = argv_n
		return 0

def err( cda ):
	print( ("[¡] %s [!]\nprueba tdc -h para las "
		"indicaciones del uso") % cda )
	exit( -1 )

if __name__ == "__main__":
	main()
