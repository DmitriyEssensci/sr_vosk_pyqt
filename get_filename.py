import sys
def get_filename(dir_to_file):
    filename = ''
    s = dir_to_file
    subs = '/'
    ls = []
    ind = -1
    while True:
        ind = s.find(subs, ind + 1)
        if ind == -1:
            break
        ls.append(ind)
        last_id = ls[-1]
        filename = s[last_id:].replace('/', '')
    return filename