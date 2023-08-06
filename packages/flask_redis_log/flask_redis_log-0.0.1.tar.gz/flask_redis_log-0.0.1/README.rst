==========================================================================================
RedisLogs - A simplified version of RedisLog that works with Flask in a more intuitive way
==========================================================================================

A logging handler for Flask that publishes log messages using Redis's pub/sub system. You can use this to store python logs into Redis. Inspired on the package: https://github.com/jedp/python-redis-log by Jed Parsons.

Installation
------------

The current stable release ::

pip install flask_redis_logs


Requirements
------------

- redis

Usage
-----

::

	>>> from redislogs.handlers import RedisHandler
	>>> redis_handler = RedisHandler(
	>>>     host=[ Redis Host ],
	>>>     port=[ Redis Port ],
	>>>     db=[ Redis DB ],
	>>>     log_key=[ Redis Channel ]
	>>> )
	>>> redis_handler.setLevel(logging.INFO)
	>>> app.logger.addHandler(redis_handler)
	>>> app.logger.info("Infor log")