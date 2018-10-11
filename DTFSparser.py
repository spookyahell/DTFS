import re


lang = {'de' : 
	{'tags':
		{'dtfs':'html','körper':'body','kopf':'head', 'stil': 'style','ü':'h'},
	'num_tags': ['ü'],
	'value_pairs': {'ja':'true',
							'nein':'false',
							'wahr':'true',
							'falsch':'false',
							'ein':'true',
							'aus':'false'},
	'property_name_pairs': {'wert':'value'},
	}
}


sel_lang = 'de'

use_lang = lang[sel_lang]
lang_tags = use_lang['tags']
lang_num_tags = use_lang['num_tags']
lang_prop_names = use_lang['property_name_pairs']

#~ JS/CSS etc. muss wie sonst auch implementiert we:rden (da es hierfür keine Übersetzung gibt und auch keine geplant ist)

#~ Method to read CR+LF or CR
f = open('example.dtfs', 'rb')
d = f.read().decode('utf-8-sig')
lines = [f.rstrip() for f in d.split('\n')]
if len(lines) == 1:
	if '\r' in lines[0]:
		lines = [f.rstrip() for f in d.split('\r')]
		
#~ for line in lines:
	
	#~ x = re.fullmatch('(\s+)?(<([a-zöäüA-ZÖÜÖ]+)(\d)?([^>]+)?>)?([^<]+)?(</([a-zöäüA-ZÖÜÖ]+)(\d)?>)?(\s+)?', line)
	#~ if x:
		#~ print(x.groups())
		
class DTFSError(Exception):
	pass
	
	
def getRealTag(tag_name, tag_num):
	tag_name_l = tag_name.lower()
	if tag_name_l in lang_tags:
		thetagname = lang_tags[tag_name_l]
		if tag_name_l in lang_num_tags:
			if tag_num:
				thetagname += tag_num
			else:
				raise DTFSError(f'Das Tag {open_name} erwartet eine Nummer, es wurde aber keine zugewiesen...')
	else:
		thetagname = tag_name
	return thetagname
	
def removeHighestItem(a_list, item):
	a_list.reverse()
	a_list.remove(item)
	a_list.reverse()
	return a_list
		
html_out = ''
open_tags = []
for line in lines:
	
	x = re.fullmatch('(\s+)?(<([a-zöäüA-ZÖÜÖ]+)(\d)?([^>]+)?>)?([^<]+)?(</([a-zöäüA-ZÖÜÖ]+)(\d)?>)?(\s+)?', line)
	if x:
		pre_space, tag_open, open_name, open_num, tag_vals, tag_text, tag_close, close_name, close_num, after_space = x.groups()
		if pre_space:
			html_out += pre_space
		if open_name:
			thetag = getRealTag(open_name, open_num)
			html_out += f'<{thetag}'
			if not tag_vals:
				html_out += '>'
		if tag_vals:
			tag_vals_list = tag_vals.split(' ')
			real_vals = {}
			for idx,item in enumerate(tag_vals_list):
				if item != '':
					x = re.fullmatch('(\w+)="([^"]+)"', item)
					if not x:
						raise DTFSError('HTML param seems falsely formed')
					else:
						property_name_l = x.group(1).lower()
						if property_name_l in lang_prop_names:
							property_name_l = lang_prop_names[property_name_l]
						html_out += f' {property_name_l}="{x.group(2)}"'
						if idx == len(tag_vals_list) -1:
							html_out += '>'
		if tag_text:
			html_out += tag_text
			
		if close_name:
			thetag = getRealTag(close_name, close_num)
			html_out += f'</{thetag}>'
							
		if after_space:
			html_out += after_space
		html_out += '\n'
	else:
		if line.upper() == '<!DOKUMENT-FORMAT DTFS>':
			html_out += '<!DOCTYPE HTML>\n'
						
print(html_out)
