import os
import certifi

def setup_tls():
	from modules.shared import cmd_opts

	if cmd_opts.tls_keyfile is not None and cmd_opts.tls_keyfile is not None:

		try:
			if not os.path.exists(cmd_opts.tls_keyfile):
				print("Invalid path to TLS keyfile given")
			if not os.path.exists(cmd_opts.tls_certfile):
				print(f"Invalid path to TLS certfile: '{cmd_opts.tls_certfile}'")
		except TypeError:
			cmd_opts.tls_keyfile = cmd_opts.tls_certfile = None
			print("TLS setup invalid, running webui without TLS")
		else:
			print("Running with TLS")

	if cmd_opts.self_sign:
		# if no cert or key then provide a default for the user in order to provide aio functionality
		if not cmd_opts.tls_certfile and not cmd_opts.tls_keyfile:
			import certipie
			cmd_opts.tls_keyfile = "./webui.key"
			cmd_opts.tls_certfile = "./webui.cert"

			if not os.path.exists(cmd_opts.tls_certfile) and not os.path.exists(cmd_opts.tls_keyfile):
				privkey = certipie.create_private_key(filename=cmd_opts.tls_keyfile)
				certipie.create_auto_certificate(
					filename=cmd_opts.tls_certfile,
					private_key=privkey,
					alternative_names=["localhost", "0.0.0.0", "::1"],
					organization="AUTOMATIC1111 Web-UI",
					country='TD',
					state_or_province="fake state",
					city="fake city"
				)
				print("Generated new key/cert pair")
			else:
				print("Default key/cert pair was already generated by webui")

		trusted = trust_cert(cmd_opts.tls_certfile)
		if trusted == 1:
			print('Given certificate has already been added to trust store')
		else:
			print('Certificate trust store updated')

		print("Running with TLS")


def trust_cert(cert):
	"""given path to a certificate, add it to the trust store. Return 1 on success, -1 if already added"""
	with open(cert, 'r') as infile:
		local_cert = infile.read()

	# print('Adding local certificate to Certifi trust store...')
	with open(certifi.where(), 'r+') as ca_bundle:
		# check that we have not already appended the certificate to the certifi trust store/CA bundle
		if ca_bundle.read().find(local_cert) == -1:
			# if you don't write this header, appending any more certs to the bundle after the first one breaks things
			ca_bundle.write("\n#\n#\n#\n# ADDED BY AUTOMATIC1111 WEBUI\n#\n#\n#\n")
			ca_bundle.write(local_cert)

			return -1
		else:
			return 1
	ca_bundle.close()
	infile.close()