import sys
import os
import re
import pprint

dot = '(?=\.|\sdot\s)'

at = '(?:\s?@\s?|\sat\s|\&#x40;)'
tld_list = ['AC' , 'AD' , 'AE' , 'AERO' , 'AF' , 'AG' , 'AI' , 'AL' , 'AM' , 'AN' , 'AO' , 'AQ' , 'AR' , 'ARPA' , 'AS' , 'ASIA' , 'AT' , 'AU' , 'AW' , 'AX' , 'AZ' , 'BA' , 'BB' , 'BD' , 'BE' , 'BF' , 'BG' , 'BH' , 'BI' , 'BIZ' , 'BJ' , 'BM' , 'BN' , 'BO' , 'BR' , 'BS' , 'BT' , 'BV' , 'BW' , 'BY' , 'BZ' , 'CA' , 'CAT' , 'CC' , 'CD' , 'CF' , 'CG' , 'CH' , 'CI' , 'CK' , 'CL' , 'CM' , 'CN' , 'CO' , 'COM' , 'COOP' , 'CR' , 'CU' , 'CV' , 'CW' , 'CX' , 'CY' , 'CZ' , 'DE' , 'DJ' , 'DK' , 'DM' , 'DO' , 'DZ' , 'EC' , 'EDU' , 'EE' , 'EG' , 'ER' , 'ES' , 'ET' , 'EU' , 'FI' , 'FJ' , 'FK' , 'FM' , 'FO' , 'FR' , 'GA' , 'GB' , 'GD' , 'GE' , 'GF' , 'GG' , 'GH' , 'GI' , 'GL' , 'GM' , 'GN' , 'GOV' , 'GP' , 'GQ' , 'GR' , 'GS' , 'GT' , 'GU' , 'GW' , 'GY' , 'HK' , 'HM' , 'HN' , 'HR' , 'HT' , 'HU' , 'ID' , 'IE' , 'IL' , 'IM' , 'IN' , 'INFO' , 'INT' , 'IO' , 'IQ' , 'IR' , 'IS' , 'IT' , 'JE' , 'JM' , 'JO' , 'JOBS' , 'JP' , 'KE' , 'KG' , 'KH' , 'KI' , 'KM' , 'KN' , 'KP' , 'KR' , 'KW' , 'KY' , 'KZ' , 'LA' , 'LB' , 'LC' , 'LI' , 'LK' , 'LR' , 'LS' , 'LT' , 'LU' , 'LV' , 'LY' , 'MA' , 'MC' , 'MD' , 'ME' , 'MG' , 'MH' , 'MIL' , 'MK' , 'ML' , 'MM' , 'MN' , 'MO' , 'MOBI' , 'MP' , 'MQ' , 'MR' , 'MS' , 'MT' , 'MU' , 'MUSEUM' , 'MV' , 'MW' , 'MX' , 'MY' , 'MZ' , 'NA' , 'NAME' , 'NC' , 'NE' , 'NET' , 'NF' , 'NG' , 'NI' , 'NL' , 'NO' , 'NP' , 'NR' , 'NU' , 'NZ' , 'OM' , 'ORG' , 'PA' , 'PE' , 'PF' , 'PG' , 'PH' , 'PK' , 'PL' , 'PM' , 'PN' , 'PR' , 'PRO' , 'PS' , 'PT' , 'PW' , 'PY' , 'QA' , 'RE' , 'RO' , 'RS' , 'RU' , 'RW' , 'SA' , 'SB' , 'SC' , 'SD' , 'SE' , 'SG' , 'SH' , 'SI' , 'SJ' , 'SK' , 'SL' , 'SM' , 'SN' , 'SO' , 'SR' , 'ST' , 'SU' , 'SV' , 'SX' , 'SY' , 'SZ' , 'TC' , 'TD' , 'TEL' , 'TF' , 'TG' , 'TH' , 'TJ' , 'TK' , 'TL' , 'TM' , 'TN' , 'TO' , 'TP' , 'TR' , 'TRAVEL' , 'TT' , 'TV' , 'TW' , 'TZ' , 'UA' , 'UG' , 'UK' , 'US' , 'UY' , 'UZ' , 'VA' , 'VC' , 'VE' , 'VG' , 'VI' , 'VN' , 'VU' , 'WF' , 'WS' , 'XXX' , 'YE' , 'YT' , 'ZA' , 'ZM' , 'ZW']
tld_list.sort(key=lambda x: len(x), reverse=True)
tld_group = r'(%s)' % '|'.join(tld_list)

pat = '([\w\+\.\-]+)' + at + \
                '([\w\.\-]+)' + \
                '(?<=\.)' +  tld_group
                
pat2 = '([\w\.\+\-]+)' + at + \
                '([\w\.\-]+\sdot\s)+' + \
                '(?<=\sdot\s)' +  tld_group
                

tld_list_slashes = []
for tld in tld_list:
    slashed_tld =''
    for char in tld:
        slashed_tld += '-' + char
    tld_list_slashes.append(slashed_tld)

tld_group_slashes =  r'(%s)' % '|'.join(tld_list_slashes)    
    
pat3 = '(\w\-)+(@\-)(\w\-)+(\.)' + tld_group_slashes

pat4 = '([\w\.\+\-]+)' + '\swhere\s' + \
                '([\w\.\-]+)' + \
                '(\sdom\s)' +  tld_group
                
pat5 = '([\w\.\+\-]+)' + at + \
                '([\w\.\-;,]+)' + \
                '(?<=;)' +  tld_group
                
pat6 = '([\w\.\+\-]+)' + at + \
                '([\w\.\-;,]+)' + \
                '(?<=,)' +  tld_group
                
pat7 = "obfuscate\('([\w\.\-]+)','([\w\.-]+)'\)"

pat8 = '([\w\.\+\-]+)' + '\s\(followed by\s(?:"|&ldquo;)' + at + '([\w\.\-]+)'+ '(?:"|&rdquo;)\)'

pat9 = '([\w\.\+\-]+)' + at + \
                '([\w\.\-]+\s){1}' + \
                '(?<=\s)' +  tld_group
                
pat10 = '([\w\.\+\-]+)' + at + \
                '([\w\.\-]+\sdo*t\s)+' + \
                '(?<=\sdt\s)' +  tld_group
                
phone1 = '(\d{3})(?:\s|-|\)\s|\))(\d{3})(?:\s|-)(\d{4})'

#sys.stderr.write(pat+'\n')
#sys.stderr.write(pat2+'\n')
#sys.stderr.write(pat3+'\n')
#sys.stderr.write(phone1+'\n')

sys.stderr.write(pat9+'\n')

""" 
TODO
This function takes in a filename along with the file object (actually
a StringIO object at submission time) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***, as it will be called directly by
the submit script

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO at submission time. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    
    for line in f:
        matches = re.findall(pat,line, re.IGNORECASE)
        for m in matches:
            email = '%s@%s%s' % m
            res.append((name,'e',email))
                
            
        matches = re.findall(pat2,line, re.IGNORECASE)
        if matches:
            line = re.sub(' dot ','.',line.lower())
            
            matches = re.findall(pat,line, re.IGNORECASE)
            for m in matches:
                email = '%s@%s%s' % m
                res.append((name,'e',email))
            
        matches = re.findall(pat3,line, re.IGNORECASE)
        if matches:
            line = re.sub('-','',line)
            
            
            matches = re.findall(pat,line, re.IGNORECASE)
            for m in matches:
                email = '%s@%s%s' % m
                res.append((name,'e',email))
                
        matches = re.findall(pat4,line, re.IGNORECASE)
        for m in matches:
            
            email = '%s@%s%s%s' % m
            
            email = re.sub(' where ','.',email.lower())
            email = re.sub(' dom ','.',email.lower())
            res.append((name,'e',email))
        
        matches = re.findall(pat5,line, re.IGNORECASE)
        if matches:
            
            line = re.sub(';','.',line.lower())
            
            matches = re.findall(pat,line, re.IGNORECASE)
            for m in matches:
                email = '%s@%s%s' % m
                
                res.append((name,'e',email))
                
        matches = re.findall(pat6,line, re.IGNORECASE)
        if matches:
            line = re.sub(',','.',line.lower())
            
            matches = re.findall(pat,line, re.IGNORECASE)
            for m in matches:
                email = '%s@%s%s' % m
                res.append((name,'e',email))
            
        matches = re.findall(pat7,line, re.IGNORECASE)
        for m in matches:
            email = '%s@%s' % (m[1],m[0])
            
            res.append((name,'e',email))
            
    
        matches = re.findall(pat8,line, re.IGNORECASE)
        for m in matches:
            email = '%s@%s' % (m[0],m[1])
            
            res.append((name,'e',email))
            
#        matches = re.findall(pat9,line, re.IGNORECASE)
#        for m in matches:
#            email = '%s@%s.%s' % m
#            email = re.sub(' ','.',email.lower())
#            sys.stderr.write(email)
#            res.append((name,'e',email))

        matches = re.findall(pat10,line, re.IGNORECASE)
        if matches:
            line = re.sub(' dt ','.',line.lower())
            line = re.sub(' dot ','.',line.lower())
            
            
            matches = re.findall(pat,line, re.IGNORECASE)
            for m in matches:
                email = '%s@%s%s' % m
             
                res.append((name,'e',email))
        
        matches = re.findall(phone1,line, re.IGNORECASE)
        for m in matches:
            phone = '%s-%s-%s' % m
            res.append((name,'p',phone))
    
    for result in res:
       
        if result[2].startswith('Server@'):
            res.remove(result)
        
    return res

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    pp.pprint(fn)
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'usage:\tSpamLord.py <data_dir> <gold_file>'
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])
