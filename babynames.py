#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Lab 6: Regular Expressions

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # +++your code here+++
  f = open(filename, 'r')
  f1 = f.read()
  strings = re.findall(r'<td>\w+', f1)
  strings1 = [s.replace('<td>', '') for s in strings]
  #print(strings1)
  rank = []
  boys = []
  girls = []
  for x in range(len(strings1)):
      if (((x + 1)/1)%3) == 1:
          rank.append(strings1[x])
      elif (((x + 1)/1)%3) == 2:
          boys.append(strings1[x])
      elif (((x + 1)/1)%3) == 0:
          girls.append(strings1[x])
          
  boys_dict = {boys[i]: rank[i] for i in range(len(rank))}
  girls_dict = {girls[i]: rank[i] for i in range(len(rank))}
  
  boys_final = []
  girls_final = []
 # print(len(strings))
 # print(rank)
  #print(boys_dict)
  for k, v in boys_dict.items():
      n1 = k + " " + v
      boys_final.append(n1)
      
  for k, v in girls_dict.items():
      n1 = k + " " + v
      girls_final.append(n1)
      
  boys_final.sort()
  final_names = boys_final + girls_final
  final_names.sort()
  year = re.findall(r'Popularity in \d+', f1)
  year1 = year[0].replace('Popularity in ', '')
  #print(final_names)
  #print(year1)
  
  final_names.insert(0, year1)
  #print(final_names)
  return final_names


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  new = extract_names(args[0])
  for e in new:
      print(e)

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  
if __name__ == '__main__':
  main()

