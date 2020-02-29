
import sys
import socket

def load_dict(filename):
    table = {}
    with open(filename, 'r') as file:
        for line in file:
            stripped_line = line.strip()

            # Split the line into an array
            table_entry = stripped_line.split(' ')

            # Use a lowercase domain name for case-insensitive lookup
            table[table_entry[0].lower()] = table_entry
    return table


dns_table = load_dict('PROJ1_DNSTS.txt')
print dns_table
print sys.argv