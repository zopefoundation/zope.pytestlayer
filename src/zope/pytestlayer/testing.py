def log_to_terminal(request, msg):
    verbose = request.config.option.verbose > 0
    if verbose:
        reporter = request.config.pluginmanager.getplugin('terminalreporter')
        reporter.ensure_newline()
        reporter.write_line(msg)
