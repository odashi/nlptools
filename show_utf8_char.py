#!/usr/bin/python3
import sys
import unicodedata

def main():
  try:
    v = bytes(int(x, 16) for x in sys.argv[1:])
    c = v.decode('utf8')
    print('gryph:            %s' % c)
    print('codepoint:        U+%x' % ord(c))
    print('name:             %s' % unicodedata.name(c, 'Unknown'))
    print('decimal:          %s' % unicodedata.decimal(c, 'Unknown'))
    print('digit:            %s' % unicodedata.digit(c, 'Unknown'))
    print('numeric:          %s' % unicodedata.numeric(c, 'Unknown'))
    print('category:         %s' % unicodedata.category(c))
    print('bidirectional:    %s' % unicodedata.bidirectional(c))
    print('combining:        %s' % unicodedata.combining(c))
    print('east_asian_width: %s' % unicodedata.east_asian_width(c))
    print('mirrored:         %s' % unicodedata.mirrored(c))
    print('decomposition:    %s' % unicodedata.decomposition(c))
  except Exception as ex:
    print('ERROR: %s' % ex)

if __name__ == '__main__':
  main()

