


############### A Subset of MSL starts here ##############################
import collections, inspect


Ordered_Dict = collections.OrderedDict;
id_func = lambda x: x;
null_func = lambda: None;
true_func = lambda: True;
false_func = lambda: False;
get_first = lambda x,y: x;
get_second = lambda x,y: y;
get_last = lambda *args: args[-1];
is_list = lambda obj: type(obj) == list;



def none_default(obj, default_value=None, func=None, none=None, none_func=None):
	return (none_func(default_value) if none_func != None else default_value) if(obj == none) else (func(obj) if func != None else obj);


def call_if(obj, is_func):
	return none_default(obj, null_func)() if is_func else obj;


def call_func(operator, *arguments):
	required_args_len = len(inspect.getargspec(operator).args);
	arguments = list(arguments);
	if(len(arguments) < required_args_len):
		arguments += [None]*(required_args_len-len(arguments));
	return operator(*arguments[:required_args_len]);

def has_key(obj, key):
	is_obj_list = is_list(obj);
	return (is_obj_list and (-len(obj) <= key < len(obj))) or (not(is_obj_list) and (key in obj));


def get_keys(obj):
	return list(range(len(obj))) if is_list(obj) else list(obj.keys());

def get_keys_values(obj):
	return list((i, obj[i]) for i in range(len(obj))) if is_list(obj) else list(obj.items());


def map_dict(func, obj, filtering_func=None, key_func=None):
	filtering_func = none_default(filtering_func, true_func);
	key_func = none_default(key_func, id_func);
	func = none_default(func, id_func);
	return obj.__class__((call_func(key_func, i[0], i[1]), call_func(func, i[1], i[0])) for i in get_keys_values(obj) if(call_func(filtering_func, i[1], i[0])));


def values_list(obj):
	if is_list(obj):
		return map(lambda x: x[1], obj);
	else:
		return obj.values();


def map_dict_list(func, obj, filtering_func=None, key_func=None):
	return values_list(map_dict(func, obj, filtering_func, key_func));


def soft_set(obj, key, value, is_force=False):
	if is_list(obj):
		if(key >= len(obj)):
			is_force = True;
			obj += [None]*(key-len(obj)+1);
		if(is_force):
			obj[key] = value;
	elif(not(key in obj) or is_force):
		obj[key] = value;
	return obj;

def get_item(obj, key_sequence, default_value = None):
	if not is_list(key_sequence):
		key_sequence = [key_sequence];
	return left_fold(lambda x,y: (x[0][y], True) if has_key(x[0], y) else (default_value, False) if x[1] else x , key_sequence, (obj, True))[0];


def set_item(obj, key, value):
	return soft_set(obj, key, value, True);


def deep_soft_set(obj, keys, value=None, is_force=False):
	left_fold(lambda x,y,i: ((soft_set(x, y, {})[y]) if (i<len(keys)-1) else soft_set(x, y, value, is_force)), keys, obj);
	return obj;


def deep_set_item(obj, keys, value=None):
	return deep_soft_set(obj, keys, value, True);


def soft_update_once(array, array2, is_force=False):
	return left_fold(lambda x1, yval, y1: soft_set(x1, y1, yval, is_force), array2, array);


def soft_update(obj, *updating_objects):
	return left_fold(lambda x,y: soft_update_once(x,y), list(updating_objects), obj);


def update(obj, *updating_objects):
	return left_fold(lambda x,y: soft_update_once(x,y, True), list(updating_objects), obj);




def left_fold(func, array, identity_element):
	for i in get_keys(array):
		identity_element = call_func(func, identity_element, array[i], i);
	return identity_element;

def mix_list(array):
	return left_fold(lambda x,y: x+y, array, []);

def is_all_true(array):
	return sum(array) == len(list(array));


def is_any_true(array):
	return sum(array) >= 1;


def if_else(a, b=None, c=None, is_func=False):
	return (call_if(b, is_func) if a else call_if(c, is_func));


def if_else_func(a, b=None, c=None):
	return if_else(a, b, c, is_func=True);


def if_else_list(bool_list, value_list, is_func):
	for i,j in get_keys(bool_list):
		if j:
			return call_if(value_list[i], is_func);
	return call_if(value_list[-1], is_func);

def partial_dict(obj, keys, fill_missing_key=False, missing_key_value=None): 
	return obj.__class__(map_dict(lambda x: (obj[x] if has_key(obj, x) else missing_key_value), keys, lambda x: (fill_missing_key or has_key(obj, x)), get_second));


def pop(obj, index):
	return get_last(call_if(lambda: obj.pop(index), has_key(obj, index)) , obj);


########## OS method starts here ####################


import csv


def read_file_pipe(file_pipe, reader=None):
	data=file_pipe.read() if reader == None else reader(file_pipe);
	file_pipe.close();
	return data;

def write_file_pipe(file_pipe, data):
	file_pipe.write(data);
	file_pipe.close();

def read_file(file_name, reader=None):
	return read_file_pipe(open(file_name, encoding="utf-8"), reader);

def write_file(fn, data, mode='w'):
	return write_file_pipe(open(fn, mode), data);

def run_linux_command(command):
	return read_file_pipe(os.popen(command));

def read_csv(file_name):
	return read_file(file_name, lambda csv_file: list(list(row) for row in csv.reader(csv_file)));

def none_default(obj, default_value=None, func=None, none=None, none_func=None):
	return (none_func(default_value) if none_func != None else default_value) if(obj == none) else (func(obj) if func != None else obj);

def run_if_can(operator, exceptions=None, default_value=None, inp=()):
	try:
		return operator(*inp);
	except tuple(none_default(exceptions, (Exception,))):
		return default_value;

def indexify(data, key_list=[], is_unique = False, is_pop = True):
	list_or_row = lambda x: x[0] if is_unique else x;
	def indexify_dict(data, key_list):
		if len(key_list) == 0:
			return list_or_row(data);
		else:
			indexified_dict = Ordered_Dict();
			for row in data:
				index = row[key_list[0]];
				soft_set(indexified_dict, index, []);
				new_row = pop(row, key_list[0]) if is_pop else row;
				indexified_dict[index].append(new_row);
			return map_dict(lambda v: indexify_dict(v, key_list[1:]), indexified_dict);
	return indexify_dict(data, key_list);





##### MSL's Time lib ####



import time, datetime, re


class Time:
	pytz = None;
	formats = {
		"standard": "%d-%m-%Y %I:%M:%S %p", 
		"cool": "%d-%m-%Y %I:%M:%S %p", 
		"time": "%I:%M:%S %p", 
		"date-time": "%d-%m-%Y %I:%M:%S %p", 
		"date": "%d-%m-%Y", 
	};

	@staticmethod
	def now(format=None, show_ms=False):
		if(format == None):
			return Time.get_time_now(show_ms=show_ms);
		else:
			return Time.string(None, format);


	@staticmethod
	def int_to_object(x):
		return datetime.datetime.fromtimestamp(x);


	@staticmethod
	def string(time_at=None, format="date-time"):
		format = Time.formats.get(format, format);
		return Time.int_to_object(none_default(time_at, Time.get_time_now())).strftime(format);


	@staticmethod
	def _int(time_string, format):
		return int(time.mktime(datetime.datetime.strptime(time_string.strip(), format).timetuple()));

	@staticmethod
	def int(time_string, format="data-time"):
		return Time._int(time_string, Time.formats.get(format, format));

	@staticmethod
	def get_time_now(show_ms=False):
		return if_else(show_ms, id_func, int)(time.mktime(datetime.datetime.now(none_default(Time.pytz, func=lambda x: x.timezone("Asia/Calcutta"))).timetuple()));


	@staticmethod
	def str2int(time_string, error_time = 0):
		time_string = re.sub('\s+', ' ', time_string).strip();
		# formates = (['']+['%d-%m-']*['%y', '%Y'])*[' ']*['', '%I:%M:%S %p', '%H:%M:%S', '%I:%M %p', '%H:%M']
		possible_formats = ['', ' %I:%M:%S %p', ' %H:%M:%S', ' %I:%M %p', ' %H:%M', '%d-%m-%y ', '%d-%b-%y', '%d-%b-%Y', '%d-%m-%y %I:%M:%S %p', '%d-%m-%y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%d-%m-%y %I:%M %p', '%d-%m-%y %H:%M', '%d-%m-%Y ', '%d-%m-%Y %I:%M:%S %p', '%d-%m-%Y %H:%M:%S', '%d-%m-%Y %I:%M %p', '%d-%m-%Y %H:%M', '%d/%m/%y ', '%d/%m/%y %I:%M:%S %p', '%d/%m/%y %H:%M:%S', '%d/%m/%y %I:%M %p', '%d/%m/%y %H:%M', '%d/%m/%Y ', '%d/%m/%Y %I:%M:%S %p', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y %I:%M %p', '%d/%m/%Y %H:%M'];
		return none_default(left_fold(lambda x,y: run_if_can(lambda: Time._int(time_string, y.strip()), [Exception]) if x == None else x, possible_formats, None), error_time);

	@staticmethod
	def get_time_at_day_start(time_at=None):
		time_at = none_default(time_at, Time.get_time_now());
		return Time.int(Time.string(time_at, "date"), "date");

	@staticmethod
	def date_to_int(d, m, y):
		return Time.int(str(d)+"-"+str(m)+"-"+str(y), "date");






##### MSL Offered Classes. ###########

class Object(dict):
	def __init__(self, initial_value={}, **kwargs):
		self.__dict__ = self;
		dict.__init__(self, initial_value, **kwargs);





msl = dict(
	__version__ = "1.0.0"
);



