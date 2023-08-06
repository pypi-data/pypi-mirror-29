from argparse import ArgumentParser
from qlib.log import log
import logging
import chardet, os, sys



parser = ArgumentParser()

parser.add_argument("file_or_obj", help=" file or some object to handle")
parser.add_argument("-e","--encoding"  , default=None, help="change encoding: utf , gbk, ...")


@log(logging.INFO)
def main():
    
    args = parser.parse_args()
    e = None
    if os.path.exists(args.file_or_obj):
        os.system("file " + args.file_or_obj)
        with open(args.file_or_obj, "rb") as fp:
            ws = fp.read(2000)
            e = chardet.detect(ws)
            logging.info(str(e))
            # logging.info("wbt")
    if args.encoding:
                        
                
        if not ws or not e:
            logging.error("not load success")
            return 

        with open(args.file_or_obj + ".bak", 'wb') as fp2:
            fp2.write(ws.decode(e['encoding']).encode(args.encoding))
            
        logging.info(e['encoding'] + ' -> ' + args.encoding )

