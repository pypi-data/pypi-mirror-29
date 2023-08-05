@echo off
python -c "import sys; import quantgo_api.cli as cli; args = sys.argv[1:]; sys.exit(cli.main(args));" %*