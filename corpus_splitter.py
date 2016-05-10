__author__ = 'Tiffany Chen'

import json
import sys

with open(sys.argv[1],'r') as infile:
    o = json.load(infile)
    with open(sys.argv[1][:-5] + '_' + '1' + '.json', 'w') as outfile:
        for i in xrange(1, 2):
            try:
                json.dump(o[str(i)], outfile, sort_keys=True, indent=4, separators=(',', ': '))
            except KeyError:
                pass