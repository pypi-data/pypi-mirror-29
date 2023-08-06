# -*- coding: utf-8 -*-

from kongalib import JSONEncoder, JSONDecoder, Decimal



class Encoder(JSONEncoder):
	def write(self, obj):
		if isinstance(obj, Decimal):
			obj = str(obj)
		return JSONEncoder.write(self, obj)

	def encode(self, obj):
		self.reset()
		self.write(obj)
		return bytes(self.generate())


class Decoder(JSONDecoder):
	def save_object(self, obj):
		if len(self.containter) > 0:
			if isinstance(self.containter[-1], list):
				self.containter[-1].append(obj)
			elif isinstance(self.containter[-1], dict):
				self.containter[-1][self.key[-1]] = obj

	def start_map(self):
		obj = {}
		self.save_object(obj)
		self.containter.append(obj)
		self.key.append(None)

	def end_map(self):
		if len(self.containter) > 1:
			self.containter.pop()
		self.key.pop()

	def read_key(self, key):
		self.key[-1] = key

	def start_array(self):
		obj = []
		self.save_object(obj)
		self.containter.append(obj)

	def end_array(self):
		if len(self.containter) > 1:
			self.containter.pop()

	def read(self, obj):
		if len(self.containter) == 0:
			self.containter.append(obj)
		else:
			self.save_object(obj)

	def decode(self, text):
		self.containter = []
		self.key = []

		if isinstance(text, basestring):
			self.parse(text)
		else:
			while True:
				data = text.read(65536)
				if not data:
					break
				self.parse(data)
		self.complete_parse()

		obj = self.containter[0]
		del self.containter
		del self.key
		return obj


def dumps(obj, encoding='utf-8'):
	return Encoder(encoding).encode(obj)


def dump(obj, fp, encoding='utf-8'):
	fp.write(dumps(obj, encoding))


def loads(text, encoding='utf-8'):
	return Decoder(encoding).decode(text)


load = loads



if __name__ == '__main__':
	from pprint import pprint
	data = { 'a': 1, 'b': [ 1,2,3, { 'c': { 'd': [4,5,6]}} ], 'e': {'f': None}, 'g': Decimal("12.345678") }

	saved = dumps(data)
	print "SAVED:"
	print saved

	loaded = loads(saved)
	print "LOADED:"
	pprint(loaded)




