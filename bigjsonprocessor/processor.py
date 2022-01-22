import sys
import json
from collections import namedtuple, defaultdict

OutRecord = namedtuple('OutRecord', ['Gender', 'HeightCm', 'WeightKg', 'BMI', 'BMICategory', 'HealthRisk'])

def compute_BMI(height_cms, weight_kg):
	"""Formua to compute BMI, given height in cms and weight in Kg"""
	try:
		height_ms = height_cms/100
		bmi = weight_kg / ((height_ms)**2)
	except ZeroDivisionError:
		print('Height cannot be zero')
		raise
	return round(bmi, 2)


def process_record():
	"""Compute the required fields and created an updated object with BMI category and health risk"""

	bmi, bmi_category, health_risk = None, None, None
	rec = None
	stats = defaultdict(int)
	while True:
		gender, height_cms, weight_kg = yield rec, stats
		try:
			bmi = compute_BMI(height_cms, weight_kg)
		except Exception:
			rec = OutRecord(gender, height_cms, weight_kg, float('NaN'), 'N/A', 'N/A')._asdict()
			continue
		if bmi < 18.5:
			bmi_category = 'Underweight'
			health_risk = 'Malnutrition risk'
			stats['under_weight'] += 1
		elif bmi >= 18.5 and  bmi <25:
			bmi_category = 'Normal Weight'
			health_risk = 'Low risk'
			stats['normal_weight'] += 1
		elif bmi >= 25 and bmi < 30:
			bmi_category = 'Overweight'
			health_risk = 'Enhanced risk'
			stats['over_weight'] += 1
		elif bmi >= 30 and bmi < 35:
			bmi_category = 'Moderately obese'
			health_risk = 'Medium risk'
			stats['moderately_obese'] += 1
		elif bmi >= 35 and bmi < 40:
			bmi_category = 'Severely obese'
			health_risk = 'High risk'
			stats['severely_obese'] += 1
		else:
			bmi_category = 'Very severely obese'
			health_risk = 'Very high risk'
			stats['very_severely_obese'] += 1
		stats['_num_records'] += 1
		rec = OutRecord(gender, height_cms, weight_kg, bmi, bmi_category, health_risk)._asdict()


def iter_json(json_file_name):
	"""Read the records from the JSON file line by line and decode"""
	decoder = json.JSONDecoder()
	with open(json_file_name, 'rt') as fp:
		for idx, line in enumerate(fp):
			if idx == 0:
				continue
			buf = line.strip()
			try:
				result = decoder.raw_decode(buf)
			except json.JSONDecodeError:
				break
			else:
				yield result[0]


def write_json(input_gen, process_gen, json_file_name):
	"""Consume the records after they are processed

	Output all the processed BMI records line by line in a
	JSON file.
	Also, once complete print out the final statistics of all
	the records.
	"""
	fp = open(json_file_name, 'wt')
	for idx, in_rec in enumerate(input_gen):
		if idx == 0:
			fp.write('[\n')
		out_rec, stats = process_gen.send((in_rec.get('Gender'), in_rec.get('HeightCm'), in_rec.get('WeightKg')))
		fp.write(json.dumps(out_rec))
		fp.write(',\n')
	fp.write(']\n')
	fp.close()
	for k, v in sorted(stats.items()):
		print(k,v, sep=' ==> ')


def big_json_transformer(input_file, output_file):
	""" Read a JSON file, extract records and create output JSON

	Input JSON can be as big as you want, we are going to stream it.
	We would decode individual JSON objects, calculate some fields
	and then write those back to Output JSON in streaming manner.

	"""
	input_gen = iter_json(input_file)
	process_gen = process_record()
	next(process_gen)
	write_json(input_gen, process_gen, output_file)

def usage():
	print('program needs 2 arguments')
	print('processor.py <input.json> <output.json>')
	sys.exit(1)

if __name__ == '__main__':
	if (len(sys.argv) - 1) < 2:
		usage()
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	big_json_transformer(input_file, output_file)
