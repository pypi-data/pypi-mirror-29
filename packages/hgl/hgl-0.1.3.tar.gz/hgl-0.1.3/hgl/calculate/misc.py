#!/usr/bin/python
# -*- coding: utf-8 -*-

#camera class
#~ class calculate:
    #~ def dot_product(self, v1, v2, dimensions=3):
        #~ """ args, first vector, second vector, number of dimensions 3 for x,y,z 2 for x,y"""
        #~ result=0
        #~ for i in range(0,dimensions):
            #~ result+=v1[i]*v2[i]
        #~ return result
#~ 
    #~ def direction_vector(self,p1,p2):
        #~ """ args = first point, second point"""
        #~ return createpoint((p2.x-p1.x,p2.y-p1.y,p2.z-p1.z))


def generate_indices(self, size):
    """ Given two points return a box parallel to the line
    Args:
      p1 (point): line start
      p2 (point): line end

    Returns:
      points: four points for the box edges

    Links:
    Images:
    """ 
    indices = []
    pos = 0
    for line in range(0, (size / 4) + 1):
        pos = line * 4
        for i in range(pos, pos + 3):
            indices.append(i)
        pos += 1
        for i in range(pos, pos + 3):
            indices.append(i)
    return indices


def interleave(list1, list2, list1_start=0, list2_start=0, step=1):
    """ Given 2 lists interleave between each list every n steps 
       optionally offset the start of either list but loop round so all results are returned.
    Args:
      list1: line start
      list2: line end
      list1_start: optionally offset start position of first list zero by default
      list2_start: optionally offset start position of second list zero by default
      step: number of items to return before switching lists

    Returns:
      list item: current item in list

    Links:"""
    if len(list1) != len(list2):
        raise StopIteration

    length1 = len(list1)
    length2 = len(list2)
    length = min(length1, length2) 
    list1_pos = list1_start
    list2_pos = list2_start
    for pos in range(0, length, step):
        for i in range(0, step):
            if list1_pos >= length1:
                list1_pos = 0
            yield list1[list1_pos]
            list1_pos += 1

        for i in range(0, step):
            if list2_pos >= length2:
                list2_pos = 0
            yield list2[list2_pos]
            list2_pos += 1

def interleave_uneven(list1, list2, list1_start=0, list2_start=0, list1_step=1, list2_step=1):
    """ Given 2 lists interleave between each list every n steps 
       optionally offset the start of either list but loop round so all results are returned.
    Args:
      list1: line start
      list2: line end
      list1_start: optionally offset start position of first list zero by default
      list2_start: optionally offset start position of second list zero by default
      list1_step: number of items to return before switching lists
      list2_step: number of items to return before switching lists

    Returns:
      list item: current item in list

    Links:"""

    length1 = len(list1) - 1
    length2 = len(list2) - 1
    length = (length1 + length2) 
    list1_pos = list1_start
    list2_pos = list2_start
    pos = 0
    while pos < length:
        for i in range(0, list1_step):
            yield list1[list1_pos]
            list1_pos += 1
            if list1_pos > length1:
                list1_pos = 0
            pos += 1

        for i in range(0, list2_step):
            yield list2[list2_pos]
            list2_pos += 1
            if list2_pos > length2:
                list2_pos = 0
            pos += 1
