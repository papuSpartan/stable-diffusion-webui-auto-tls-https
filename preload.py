def preload(parser):
	parser.add_argument("--self-sign", action='store_true', help="Trust a provided key/certificate pair passed using --tls-certfile and --tls-keyfile", default=None)
	parser.add_argument("--autotls-certs", nargs='+', help="Trust one or more given certificates Ex. --certs cert1.cert cert2.cert", default=None)
	parser.add_argument("--autotls-bundle", help="Pass an entire trust store/bundle to python", default=None)
