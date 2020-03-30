import sys
import os
import argparse
import logging
import re

#                               --------info sent------- -------info rcvd--------
# QSO: freq  mo date       time call          rst exch   call          rst exch   t
# QSO: ***** ** yyyy-mm-dd nnnn ************* nnn ****** ************* nnn ****** n
# QSO:  3799 PH 1999-03-06 0711 HC8N          59  001    W1AW          59  001    0
# 000000000111111111122222222223333333333444444444455555555556666666666777777777788
# 123456789012345678901234567890123456789012345678901234567890123456789012345678901

def fake_qso():
    qso = {
        'freq' : 7100, # kHz integer
        'mo' : 'ph', # cw or ph, not ssb!
        'date' : '2000-01-01',
        'time' : '2359',
        'call_sent' : 'DL0XXX',
        'rst_sent' : '59',
        'exch_sent' : '12', 
        'call_rcvd' : 'TA0XXX',
        'rst_rcvd' : '59',
        'exch_rcvd' : '1234',
    }
    return qso


def cabrillo_qso_line(qso):
    qso_line = ('QSO: '
            f'{qso["freq"]:5} '
            f'{qso["mo"][0:2]:2} '
            f'{qso["date"]:10} '
            f'{qso["time"]:4} '
            f'{qso["call_sent"]:13} '
            f'{qso["rst_sent"]:3} '
            f'{qso["exch_sent"]:6} '
            f'{qso["call_rcvd"]:13} '
            f'{qso["rst_rcvd"]:3} '
            f'{qso["exch_rcvd"]:6} ' )
    return cabrillo_qso_line

def get_adif_data(record, specifier):
    pattern = re.compile(r'<call:.*?>(\w+)<')
    match = pattern.match(line)
    if (match):
        return(match.group(1))
    else:
        return None

parser = argparse.ArgumentParser()
parser.add_argument("adif_file")
args = parser.parse_args()

if (not os.path.exists(args.adif_file)):
    logging.error(f'ADIF file {args.adif_file} does not exist.')
    exit(-1)

with open(args.adif_file, 'r') as f:
    eoh_matched = False # we haven't seen <EOH> yet
    for line in f:
        # skip header
        if (not eoh_matched):
            eoh_matched = re.match('<EOH>',line)
            continue # fast-forward until <EOH>
        # now parse lines for qso records
        qso = {}
        call = get_adif_data(line, 'XXX')
        if (not call):
            continue # skip line if it does not contain a call 
        print(call)        

    # now parse QSO lines
    

#for adif_line in 

# qso_line=qso_line(fake_qso())
# print(qso_line)