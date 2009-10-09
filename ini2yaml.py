#!/usr/bin/python -tt
# vim: ai ts=4 sts=4 et sw=4

#    Copyright (c) 2009 Intel Corporation
#
#    This program is free software; you can redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by the Free
#    Software Foundation; version 2 of the License
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#    for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc., 59
#    Temple Place - Suite 330, Boston, MA 02111-1307, USA.


import os
import sys


"""Overview of ini2yaml
    (1) ini2yaml reads the ini file and divides it into segments.    
    (2) Parses the 'header' segment. Write out the key,value pairs 
    (3) Expand the 'Files' if found
    (4) Parse the sub-packages segments if found
"""

def segmentize(iniFile):
    """Divide the ini file into segments. The segments are then organized into a dictionary with header name as the key"""
    #Initialize the dictionary
    segments = dict()
    for line in iniFile:
        #Search every line for segment header
        if line.find('[') != -1:
            #Line is a segment header. Initialize a new segment
            name = line.strip().strip('[]')
            segments[name] = ""
        else:
            #Lne is not a segment header. Add the line to the current segment
            segmentContent = segments[name]
            segments[name] = segmentContent + line
    #Return the dictionary of segments
    return segments

def parse_segment(segments, segment_name, iniDir = None):
    """Function to parse a segment and convert it into key value pairs"""
    #Initialize a dictionary
    segment_dict = dict()
    key = ""
    segment_content = segments[segment_name].splitlines() 
    for line in segment_content:
        #Check if the line has a '=' char
        if line.find('=') != -1:
            key = line.split('=', 1)[0].strip() 
            #Rename Summary to Description
            if key == 'Summary':
                key = 'Description'
            segment_dict[key] = line.split('=', 1)[1].strip()
        #If a line does not have a '=' char, either include it with the previous key if it exists        
        else:
            if key:
                segment_dict[key] = segment_dict[key] + '\n' + line.strip()
            #Ignore as comment if no previous key exists
            else:
                pass

    #If the key happens to be 'Files' then we need to find the corresponding *.files and expand it 
    #The first line of *.files might contain %doc, this needs to be handled separatly
    doc = ""
    for key, content in segment_dict.iteritems():
        if key == 'Files':                    
            doc, files = expand_file(os.path.join(iniDir, content), None)
            segment_dict['Files'] = files
    if doc:
        segment_dict['Documents'] = doc

    return segment_dict


def read_file():
    """Read the input file"""
    #Check if the input file exists
    if os.path.exists(sys.argv[1]):
        iniFilePath = sys.argv[1]
        iniDir = os.path.dirname(iniFilePath)
        yamlFilePath = iniFilePath.rstrip('.ini') + ".yaml"
        print "ini File: %s" % iniFilePath
        print "yaml File: %s" % yamlFilePath
        iniFile = open(sys.argv[1], "r")
        yamlFile = open(yamlFilePath, "w")
        segments = segmentize(iniFile)
        #print segments
        for name, value in segments.iteritems():
            print "--------------- %s ------------" % name
            parsed_segment = parse_segment(segments, name, iniDir)
            segments[name] = parsed_segment 
            #for key, content in parsed_segment.iteritems():
            #    print "%s:    %s" % (key, content)
            #print value.splitlines() 
        #Write all the parsed information to the yaml file
        #Start with the header
        header_segment = segments['header'] 
    
        #Lets write the Name, Version, Release first

        write_to_yaml(yamlFile, "Name", header_segment['Name'])
        del header_segment['Name'] 

        write_to_yaml(yamlFile, "Version", header_segment['Version'])
        del header_segment['Version'] 

        write_to_yaml(yamlFile, "Release", header_segment['Release'])
        del header_segment['Release'] 

        for key, value in header_segment.iteritems():
            #Saving SubPackages and Files for last
            if key != 'SubPackages'  and key != 'Files':
                write_to_yaml(yamlFile, key, value)
       
        for key, value in segments['configuration'].iteritems():
            if key == 'PkgConfig':
                write_to_yaml(yamlFile, "BuildRequires", "")
                write_to_yaml(yamlFile, key, value, 1)
            else:
                write_to_yaml(yamlFile, key, value)

        write_to_yaml(yamlFile, "Files", header_segment['Files'])
        
        #Write out all the subpackages  
        sub_package_list = header_segment['SubPackages'].split() 
        print sub_package_list
        write_to_yaml(yamlFile, "SubPackages", "")
        for subPackage in sub_package_list:
            write_to_yaml(yamlFile, subPackage, "", 1)
            for key, value in segments[subPackage].iteritems():
                if key != 'Files':
                    write_to_yaml(yamlFile, key, value, 2)
            write_to_yaml(yamlFile, 'Files', segments[subPackage]['Files'], 2)
	#If input file does not exist, print an error message and exit         
    else:
        print "%s: File does not exist" % sys.argv[1]

def expand_file(fileName, yamlFile):
    """This Function expands *.files"""
    #print "Expanding file: %s..." % fileName
    doc = ""
    files = ""
    if os.path.exists(fileName):
        fileObj = open(fileName)
        for line in fileObj:
            #Check if any line has %doc mentioned. It needs to be handled seperatly
            if line.find("%doc") != -1:
                doc = line[4:].strip() 
            else:
                files = files + line
    else:
        print "Missing file: %s" % fileName
    return doc, files

def write_to_yaml(yamlFile, key, value, ts = 0):
    """Function to write the key value pair to yaml file.
    It checkes if a value has multiple lines and handles them."""
    tab = ""
    for i in range(ts):
        tab = tab + '\t'
    lines_to_write = value.splitlines()
    if len(lines_to_write) == 1:
        yamlFile.write(tab + "%s: %s\n" % (key, value))
    elif len(lines_to_write) == 0:
        yamlFile.write(tab + "%s:\n" % (key))
    else:
        yamlFile.write(tab + "%s: |\n" % key)
        tab = tab + '\t'
        for line in lines_to_write:
            yamlFile.write(tab + "%s\n" % line)

if __name__ == '__main__':
    """Main Function"""
    print "ini2yaml"
    #Check to see if an argument was passed. If no arguments were passed, print the usage and exit.
    if len(sys.argv) == 1:
        print "Usage: ini2yaml inifile_path"
    else:
        read_file()


