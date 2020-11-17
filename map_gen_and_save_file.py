#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import os

def map_gen(x, y, density):
    print('{}.ox'.format(y))
    #first line
    output = str(y) + '.ox\n'
    
    for i in range(int(y)):
        result = str()
        for j in range(int(x)):
            if (random.randint(0, int(y)) * 2) < int(density):
                print('o', end='')
                result += 'o'
            else:
                print('.', end='')
                result += '.'
        print('', end='\n')        
        output += result + '\n'


    fileName = str(x) + '_' + str(y) + '_' + str(density)
    
    #write into file
    if not os.path.isfile(fileName):
        file = open(fileName, "w")
        file.write(output)
        file.close()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Missing parameters.')
        exit()
    map_gen(*sys.argv[1:4])
