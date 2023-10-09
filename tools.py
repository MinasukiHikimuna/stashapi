import base64, hashlib, math, re
from collections import defaultdict

def defaultify(d:dict, default=None):
	"""Return default dict for given nested dictionaries with provided default value"""
	if not isinstance(d, dict):
		return d
	return defaultdict(lambda: default, {k: defaultify(v) for k, v in d.items()})

def clean_dict(to_clean):
# returns dictionary where values are not None
	return {k:v for k,v in to_clean.items() if v and "__" not in k}

def str_compare(s1, s2, ignore_case=True):
	import string
	# remove punctuation
	punctuation = re.compile(f'[{string.punctuation}]')
	s1 = re.sub(punctuation, ' ', s1)
	s2 = re.sub(punctuation, ' ', s2)
	
	# normalize whitespace
	whitespace = re.compile(f'[{string.whitespace}]+')
	s1 = re.sub(whitespace, ' ', s1)
	s2 = re.sub(whitespace, ' ', s2)

	# remove leading and trailing whitespace
	s1 = s1.strip(string.whitespace)
	s2 = s2.strip(string.whitespace)

	# force lowercase
	if ignore_case:
		s1 = s1.lower()
		s2 = s2.lower()

	return s1 == s2

def sha256(pth, return_object=False, buffer=65536):
	sha256_value = hashlib.sha256()
	with open(pth, 'rb') as f:
		while True:
			data = f.read(buffer)
			if not data:
				break
			sha256_value.update(data)
	if return_object:
		return sha256_value
	return sha256_value.hexdigest()

def get_base64(pth):
	"""deprecated use file_to_base64() instead"""
	return file_to_base64(pth)

def url_to_base64(url):
	import requests
	return base64.b64encode(requests.get(url).content)

def file_to_base64(image_path):

	from pathlib import Path
	import mimetypes
	"""get base64 encoded image from local image path

	Args:
		 image_path (str): path to image file

	Returns:
		 str: base64 encoded string of image
	"""
	mime =  mimetypes.types_map.get(Path(image_path).suffix, 'image/jpeg')
	with open(image_path, "rb") as img:
		b64img_bytes = base64.b64encode(img.read())
	if not b64img_bytes:
		return None
	return f"data:{mime};base64,{b64img_bytes.decode('utf-8')}"

def si_prefix(value, round):
	SI_PREFIX_UNITS = u"yzafpnµm kMGTPEZY"

	tens_exponent = int(math.log(value,10))
	units_mid = (len(SI_PREFIX_UNITS)-1) // 2
	si_level = tens_exponent // 3
	try:
		prefix =  SI_PREFIX_UNITS[si_level+units_mid]
	except:
		prefix = f"e{tens_exponent}"

	value /= 10 ** tens_exponent
	return f"{value:.{round}f}{prefix}"

def human_bytes(value, round=1):
	try:
		return f"{si_prefix(value, round)}B"
	except:
		return f"{value:.{round}f}B"
	
def human_bits(value, round=1):
	try:
		return f"{si_prefix(value, round)}b"
	except:
		return f"{value:.{round}f}b"
	
def phash_distance(lhash, rhash):
	assert len(lhash) == len(rhash)
	hamming = int(lhash,16) ^ int(rhash,16)
	return bin(hamming).count("1")

def similarity_score(lhash, rhash):
	return 1-(phash_distance(lhash, rhash)/64.0)