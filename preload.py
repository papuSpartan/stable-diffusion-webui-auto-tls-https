def preload(parser):
	parser.add_argument("--self-sign", action='store_true', help="Trust a provided key/certificate pair passed using --tls-certfile and --tls-keyfile", default=None)
