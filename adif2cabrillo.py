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
    match = re.search(r'<' + specifier + r':.*?>(.+?)<', record)
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
    linenumber = 0
    for line in f:
        linenumber = linenumber + 1
        
        # skip header
        if (not eoh_matched):
            eoh_matched = re.match('<EOH>',line)
            continue # fast-forward until <EOH>
        
        # now parse lines for qso records
        qso = {}
        
        # call
        call = get_adif_data(line, r'call')
        if (not call):
            logging.warning(f'call missing for record in line {linenumber}, skipping')
            continue # skip line if no call 
        qso['call'] = call
        
        # band (only needed if freq is missing)
        band = get_adif_data(line, r'band')
        if band:
            qso['band'] = band
        
        # freq
        freq =  get_adif_data(line, r'freq')
        if (freq):
            qso['freq'] = int(float(freq) * 1000.) # MHz to kHz
        else:  # sometimes freq seems to be missing
            qso['freq'] = band
            logging.warning(f'freq missing for record in line {linenumber}, using band instead')
       
        # mode
        mode = get_adif_data(line, r'mode')
        if (mode):
            if (mode == 'SSB'):
                qso['mode'] = 'PH'
            else:
                qso['mode'] = mode
        else:
            logging.warning(f'mode missing for record in line {linenumber}')
        
        # date
        date = get_adif_data(line, r'qso_date')
        if (date):
            qso['date'] = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
        else:
            logging.warning(f'date missing for record in line {linenumber}')

        # time
        time = get_adif_data(line, r'time_on')
        if (time):
            qso['time'] = time[0:4]
        else:
            logging.warning(f'time missing for record in line {linenumber}')

        # rst and exchange sent
        rst_exch_sent = get_adif_data(line, r'rst_sent')
        if (rst_exch_sent):
            (qso['rst_sent'], qso['exch_sent']) = re.split(r'[ ]\s*', rst_exch_sent)
        else:
            logging.warning(f'rst, exch sent missing for record in line {linenumber}')

        # rst and exchange rcvd
        rst_exch_rcvd = get_adif_data(line, r'rst_rcvd')
        if (rst_exch_rcvd):
            (qso['rst_rcvd'], qso['exch_rcvd']) = re.split(r'[ ]\s*', rst_exch_rcvd)
        else:
            logging.warning(f'rst, exch sent missing for record in line {linenumber}')

        print(qso)        
    

#for adif_line in 

# qso_line=qso_line(fake_qso())
# print(qso_line)