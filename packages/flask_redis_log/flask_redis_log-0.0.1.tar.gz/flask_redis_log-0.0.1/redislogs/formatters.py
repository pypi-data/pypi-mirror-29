import logging
import json

class RedisFormatter(logging.Formatter):
	def format(self, record):
		data = vars(record)
		return json.dumps(data)