Much of the detail of the file format remains unknown. Contributions
and corrections are very welcome. Thanks are due to Sooty,
who provided example files for dissection.

The files begin with a 640-byte header, which begins with the magic number
``SGCAT32``. Nothing is known about header fields at present.

One or more records follow the header. Each record gives a
single translation from steno to text.

The record header is 21 bytes. header[18] contains the number
of strokes, and header[19] gives the number of letters in
the text. Each is an unsigned byte. The purpose of all other
fields in the record header is unknown at present.

The stroke follows, as a sequence of four-byte unsigned integers.
Each integer is a bitmap of keys in the standard steno order,
with the first "S" as the most significant bit.

Then the text follows, as ordinary ASCII text. Nothing is
currently known about coding of text outside the ASCII range.
Various non-ASCII characters crop up, apparently as
control codes.

Finally, there are zero to three padding bytes, in order
to bring us up to a four-byte boundary.
