import logging


class IdentityTransformer(object):
    """Minimal tornado transform implementation."""

    def __init__(self, request, *args, **kwargs):
        pass

    def transform_first_chunk(self, status_code, headers, chunk,
                              include_footers):
        return status_code, headers, chunk

    def transform_chunk(self, chunk, include_footers):
        return chunk


class EnsureRequestIdTransformer(IdentityTransformer):
    """
    Transformer that creates the ``divak_request_id`` property on requests.

    This simple Tornado transformer uses :func:`setattr` to ensure that
    every request has a ``divak_request_id`` property.

    """

    def __init__(self, request, *args, **kwargs):
        if not hasattr(request, 'divak_request_id'):
            setattr(request, 'divak_request_id', None)
        super(EnsureRequestIdTransformer, self).__init__(
            request, *args, **kwargs)


class DivakRequestIdFilter(logging.Filter):
    """
    Logging filter that sets the `divak_request_id` attribute on records.

    This makes it possible to use ``divak_request_id`` in log formats
    without having to do additional work.  You shouldn't need to tinker
    with this yourself since :class:`divak.api.Recorder` does it for you
    when a instance is created.

    """

    def filter(self, record):
        if not hasattr(record, 'divak_request_id'):
            setattr(record, 'divak_request_id', '')
        return 1


class DivakLogger(logging.Logger):
    """
    Extends class:`logging.Logger` to ensure that divak_request_id is set.

    This class is installed via :func:`logging.setLoggerClass` to ensure
    that the ``divak_request_id`` attribute is set on all records.

    """

    def makeRecord(self, *args, **kwargs):
        # Using args & kwargs to work around signature differences
        # between python versions
        record = super(DivakLogger, self).makeRecord(*args, **kwargs)
        if not hasattr(record, 'divak_request_id'):
            setattr(record, 'divak_request_id', '')
        return record


def initialize_logging():
    """
    Ensure that LogRecords have a divak_request_id defined.

    This is called during initialization to ensure that
    :class:`logging.LogRecord` instances will *always* have a
    ``divak_request_id`` property.  This makes it possible to refer to
    the request id in your log formats.

    Firstly, it installs a new :class:`logging.Logger` class by calling
    :func:`logging.setLoggerClass` that sets the attribute in it's
    :meth:`logging.Logger.makeRecord` method if it not already present.
    Then it spins through the existing loggers and adds
    :class:`.DivakRequestIdFilter` to any handler that doesn't already have
    one.  This process ensures that new and existing loggers can refer to
    the request id in log formats.

    """
    # First we need to insert our own logger class.  That is the
    # easy part.
    logging.setLoggerClass(DivakLogger)

    # ... and then insert filters on all active logging.Handler
    # instances that already exist... so much work!
    log_filter = DivakRequestIdFilter()
    known_handlers = set()
    for logger in logging.Logger.manager.loggerDict.values():
        if isinstance(logger, logging.Logger):
            for handler in logger.handlers:
                if handler not in known_handlers:
                    if not _has_divak_filter(handler.filters):
                        handler.addFilter(log_filter)
                    known_handlers.add(handler)
    for handler in logging.getLogger().handlers:
        if handler not in known_handlers:
            if not _has_divak_filter(handler.filters):
                handler.addFilter(log_filter)
            known_handlers.add(filter)


def _has_divak_filter(filters):
    """
    Check if `filters` contains a DivakRequestIdFilter instance.

    :param filters: sequence of ``logging.Filter`` instances
    :returns: :data:`True` if a :class:`DivakRequestIdFilter` instance
        is in `filters`; :data:`False` otherwise
    :rtype: bool

    """
    for filter in filters:
        if isinstance(filter, DivakRequestIdFilter):
            return True
    return False
