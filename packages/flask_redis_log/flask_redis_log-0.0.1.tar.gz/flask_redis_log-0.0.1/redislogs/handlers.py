import redis
import logging
from redislogs.formatters import RedisFormatter

class RedisHandler:
	def __init__(self, host=None, port=None, db=0, log_key='logs'):
		self._redis = redis.Redis(host=host, port=port, db=db)
		self._redis_list_key = log_key
		self._level = logging.DEBUG
		self._formatter = RedisFormatter()

	def handle(self, record):
		try:
			self._redis.publish(self._redis_list_key, self._formatter.format(record))
		except Exception as e:
			pass

	def setFormatter(self, formatter):
		self._formatter = formatter

	@property
	def level(self):
		return self._level

	def setLevel(self, val):
		self._level = val