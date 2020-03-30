CQ WPX contest expects "Cabrillo" logs, so...

adif2cabrillo
=============

This amateur radio utility converts ADIF log files (as exported by Cloudlog)
to Cabrillo log files (as expected by the CQ WPX contest).
It only writes the QSO lines, not the header.

From <https://www.cqwpx.com/cabrillo.htm> :

```
QSO: qso-data
The qso-data format is shown below.

                              --------info sent------- -------info rcvd--------
QSO: freq  mo date       time call          rst exch   call          rst exch   t
QSO: ***** ** yyyy-mm-dd nnnn ************* nnn ****** ************* nnn ****** n
QSO:  3799 PH 1999-03-06 0711 HC8N          59  001    W1AW          59  001    0
000000000111111111122222222223333333333444444444455555555556666666666777777777788
123456789012345678901234567890123456789012345678901234567890123456789012345678901

Note for Column 81 (transmitter number): For the MULTI-TWO category, the last column in the log indicates which transmitter made the QSO. It must be a 0 or a 1. This column is not required for other categories.
```
