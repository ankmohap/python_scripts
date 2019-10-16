import os

#Path where we have to browse files
path=r'D:\test_file'

#Dictionaries created with intent of keeping file names as keys
dict_header = {}
dict_footer = {}

array2=[]

#function to link pairs to the list or array

def link_pairs(p1,p2):
    array1=[]
    array1=[p1,p2]
    found = ''
    for i in range(len(array2)):
        if array1[0] == array2[i]:
            array2.insert(i+1,array1[1])
            found = 'y'
    if found == '':
        array2.append(array1[0])
        array2.append(array1[1])
    print ("List After linking--")
    print (array2)
        
count_header= {};

#Remove duplicates while re-arranging
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

files=[]
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
            files.append(os.path.join(r, file))
            
print("File List --")            
for f in files:
    print(f)
    file_handle = open(f,"r")
    line_list = file_handle.readlines()
    footer=line_list[-1]
    header=line_list[0]
    dict_header.update({f:header})
    dict_footer.update({f:footer})

for key in dict_footer.keys():
    for key1 in dict_header.keys():
        if (dict_footer[key] == dict_header[key1].splitlines()[0]):
            print ('LINK'+':'+key.split('\\')[2]+':'+key1.split('\\')[2])
            pair1=key.split('\\')[2]
            pair2=key1.split('\\')[2]
            count_header.update({key1:1})
            link_pairs(pair1,pair2)

#Below block will give which file has no matching header with any footer that can be treated as start of sequence 
diff = str(set(dict_header) - set(count_header))
seq_start=diff
start_point=seq_start.split('\\')[4]

#Identify point to break the list as per start of sequence 
mid_index = 0 
for i in range(len(array2)):
    if array2[i] == str(start_point.split('\'')[0]):
        mid_index = i

print ('List can be broken from -'+str(mid_index))

final_Array = array2[mid_index:]

for i in range(0,mid_index):
    final_Array.append(array2[i])
print('list after re-arrage-')
final_list =Remove (final_Array)

print ('>'.join(final_list))

    
