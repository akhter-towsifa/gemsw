'''
gets the list of files in the format needed for unpacker
--Towsifa
'''
#run10090a-index000000.raw.zst

f = open("10090_files.list", "r")

a_list = []
b_list = []

def list_by_index_a(read_line):
  if read_line[8]=="a":
    a_list.append(read_line[:29])
  else:
    return
  return a_list
 
def list_by_index_b(read_line):
  if read_line[8]=="b":
    b_list.append(read_line[:29])
  else:
    return
  return b_list

def group_together_ab(a, b):
  if a[15:20]==b[15:20]:
    new_line = '[file:' + a + ', file:' + b + ']\n' 
  return new_line

list_of_original_lines = f.readlines()
for line in list_of_original_lines:
  list_by_index_a(line)
  list_by_index_b(line)

f_new = open("10090.list", "w")

for idx, a_line in enumerate(a_list):
  #print(group_together_ab(a_list[idx], b_list[idx]))
  f_new.writelines(group_together_ab(a_list[idx], b_list[idx]))

f.close()
f_new.close()
