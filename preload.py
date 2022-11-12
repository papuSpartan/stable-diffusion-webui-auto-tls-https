def preload(parser):
	parser.add_argument("--self-sign", action='store_true', help="Trust a provided self-signed certificate passed using --tls-certfile or automatically generate and trust a key/cert pair to enable TLS", default=None)
