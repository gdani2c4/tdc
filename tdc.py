import sys, json, re
from datetime import datetime
err_ach_de_tdc_predet = \
	"[¡] no se encontró el archivo \"./dat/tdc.json\" " +\
	"en el directorio actual (el \"pwd\") [!]"

def main():
	ach_prog_nom = sys.argv[1]
	tdcv_nv = {}
	tdcv_ant = {}
	rstdo = {}
	# ach_cda	el archivo del programa que está
	#	para traducir
	ach_prog = { "ficha_v": [], "ach_cda": "" }
	ach_prog_leer( ach_prog_nom, ach_prog )
	as_ach_prog( ach_prog, tdcv_nv )
	tdcv_ant_leer( rstdo )
	tdcv_ant = rstdo["tdcv_ant"]
	tdcv_unir( tdcv_ant, tdcv_nv )
#	print( json.dumps( tdcv_nv, indent = 4 ) )
	tdcv_escr( tdcv_nv, tdcv_ant )

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

def as_ach_prog( ach_prog, rstdo ):
	re_rstdo = \
	re.finditer( "".join(
		# dejé un grupo "xx" para "fch + cda + fch" entero
		[	( "(?P<xx%(val)s>%(fa)s" +\
			"(?P<fch%(val)s>%(cnd)s)" + "%(fc)s)|" )\
			% {
				"fa":ii["fa"], "fc":ii["fc"],
				"val": ach_prog["ficha_v"].index(ii),
				"cnd": ".*?" if "sin_esc" in ii else \
					r"(.*?[^\\](\\\\)*)|(\\\\)*"
			}  for ii in ach_prog["ficha_v"]
		]
	)[:-1], ach_prog["ach_cda"], re.DOTALL )
	for ii in re_rstdo:
		for kk in range( len(ach_prog["ficha_v"] ) ):
			if ii.group( "fch%d" % kk ):
				rstdo[ ii.group( "fch%d" % kk ) ] = ""

def tdcv_ant_leer( rstdo, tdc_nom_ach = "dat/tdc.json" ):
	with open( tdc_nom_ach ) as ach_tdc:
		try:
			rstdo["tdcv_ant"] = json.load( ach_tdc )
		except FileNotFoundError:
			print( err_ach_de_tdc_predet )
			exit( -1 )

def tdcv_unir( tdcv_ant, tdcv_nv ):
	for ii in tdcv_nv:
		if ii in tdcv_ant:
			tdcv_nv[ ii ] = tdcv_ant[ ii ]

def tdcv_escr( tdcv_nv, tdcv_ant,
		tdc_nom_ach = "dat/tdc.json" ):
	with open( tdc_nom_ach + \
		datetime.now().strftime("%d%m%y_%H%M"), "w" )\
		as ach:
		ach.write( json.dumps( tdcv_ant, indent = 4 ) )
	with open( tdc_nom_ach, "w" ) as ach:
		ach.write( json.dumps( tdcv_nv, indent = 4 ) )

if __name__ == "__main__":
	main()
