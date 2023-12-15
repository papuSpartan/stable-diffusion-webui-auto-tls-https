import launch

if not launch.is_installed("certipie"):
    launch.run_pip("install certipie==0.2.0", "requirements for auto-tls")
if not launch.is_installed("certifi"):
    launch.run_pip("install certifi", "requirements for auto-tls")
