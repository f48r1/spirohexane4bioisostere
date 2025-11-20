DIR_DATA = 'data'

DIR_CORES = 'cores'
DIR_REACTIONS = 'reactions'

DIR_MM = 'MM'
DIR_RAW = 'raw'
DIR_OPT = 'opt_mol'
DIR_COMP = 'computed'
DIR_DFT = 'DFT'

SEP='|'

def parse_params(path):
    import re
    import os
    relevant_path, ext = os.path.splitext(path)
    
    exclusion = rf'[^{SEP}{os.path.sep}]'

    compiler_kwargs = re.compile(r'(?P<key>'+exclusion+r'+)=(?P<value>'+exclusion+r'+)')
    kwargs = compiler_kwargs.findall(relevant_path)
    return dict(kwargs)

def smi2safepath(smi):
    bytes = smi.encode("utf-8")
    numb = int.from_bytes(bytes, byteorder="big")
    path = str(numb)
    return path

def safepath2smi(path):
    path = int(path)
    bytes = path.to_bytes(((path.bit_length() + 7) // 8), byteorder="big")
    string = bytes.decode("utf-8")
    smi = str(string)
    return smi