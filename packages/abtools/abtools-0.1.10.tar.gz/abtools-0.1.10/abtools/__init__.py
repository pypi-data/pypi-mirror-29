import os

if not os.environ.get('READTHEDOCS', None):

    from ._compare import run as compare
    from ._correct import run as correct
    from ._finder import run as finder
    from ._phylogeny import run as phylogeny
    # import _stats as stats

    from pkg_resources import get_distribution, DistributionNotFound
    import os.path

    try:
        _dist = get_distribution('abtools')
        # Normalize case for Windows systems
        dist_loc = os.path.normcase(_dist.location)
        here = os.path.normcase(__file__)
        if not here.startswith(os.path.join(dist_loc, 'abtools')):
            # not installed, but there is another version that *is*
            raise DistributionNotFound
    except DistributionNotFound:
        __version__ = 'Please install AbTools before checking the version'
    else:
        __version__ = _dist.version
