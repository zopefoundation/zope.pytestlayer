"""
Coverage sitecustomize - enable coverage for subprocess started via
subprocess.Popen
"""
import atexit
import os


# Check if coverage subprocess tracking is enabled
if 'COVERAGE_PROCESS_START' in os.environ:
    import coverage

    # Start coverage in this subprocess
    cov = coverage.Coverage(
        config_file=os.environ['COVERAGE_PROCESS_START'])
    cov.start()
    atexit.register(cov.save)
