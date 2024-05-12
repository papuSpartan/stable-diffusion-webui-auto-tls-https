import os
import certifi
from modules.shared import cmd_opts

wui_keyfile = "./webui.key"
wui_certfile = "./webui.cert"
wui_bundle_name = "./webui.bundle"

def setup_bundle(cert):
	"""given path to a certificate, pass it to requests as being trusted along with the certifi bundle"""

	cert = open(cert)
	certifi_bundle = open(certifi.where())
	wui_bundle = open(wui_bundle_name, "w")

	# merge user cert(s) with certifi bundle into an intermediary webui bundle
	wui_bundle.write(certifi_bundle.read())
	wui_bundle.write(cert.read())
	if cmd_opts.autotls_certs is not None:
		for c in cmd_opts.autotls_certs:
			c = open(c)
			wui_bundle.write(c.read())
			c.close()

	# cleanup
	cert.close()
	certifi_bundle.close()
	wui_bundle.close()

	os.environ['REQUESTS_CA_BUNDLE'] = wui_bundle_name


if not cmd_opts.self_sign:
	import certipie
	cmd_opts.tls_keyfile = wui_keyfile
	cmd_opts.tls_certfile = wui_certfile

	if not os.path.exists(cmd_opts.tls_certfile) and not os.path.exists(cmd_opts.tls_keyfile):
		privkey = certipie.create_private_key(filename=cmd_opts.tls_keyfile)
		certipie.create_auto_certificate(
			filename=cmd_opts.tls_certfile,
			private_key=privkey,
			# it seems like requests prioritizes CN despite CN being deprecated by SAN's?
			# localhost is already picked as the cert common name by default through constructor
			common_name=cmd_opts.server_name if cmd_opts.server_name else "localhost",
			alternative_names=None,
			organization="AUTOMATIC1111 Web-UI",
			country='TD',
			state_or_province="fake state",
			city="fake city",
		)
		print("Generated new key/cert pair")
	else:
		print("Default key/cert pair was already generated by webui")
else:
	try:
		if not os.path.exists(cmd_opts.tls_keyfile):
			print(f"Invalid path to TLS keyfile: '{cmd_opts.tls_keyfile}'")
		if not os.path.exists(cmd_opts.tls_certfile):
			print(f"Invalid path to TLS certfile: '{cmd_opts.tls_certfile}'")
	except TypeError as e:
		cmd_opts.tls_keyfile = cmd_opts.tls_certfile = None
		print("TLS components missing or invalid.")
		raise e

success_msg = 'Certificate trust store ready'
if cmd_opts.autotls_bundle is not None:
	if not os.path.exists(cmd_opts.autotls_bundle):
		print(f"could not open bundle file '{cmd_opts.autotls_bundle}'")
	else:
		os.environ['REQUESTS_CA_BUNDLE'] = cmd_opts.autotls_bundle
		print(success_msg)
else:
	setup_bundle(cmd_opts.tls_certfile)
	print(success_msg)
