from operator import itemgetter
import datetime, sys, logging
from .LogGen import set_up_logging

logger = logging.getLogger(__name__)

def GetDate():
    logger.debug("Setting the date.")
    return datetime.date.today().strftime("%d%b%Y") # i.e. 15Feb2018

# split words from file extension and number, sort by index (numerically or alphabetically), 
# then rejoin words in list
def NumberMe(List):
    NumList = []
    WordList = []
    for item in List:
        String = item.split('.')[0]# get value to the left of ".jpg" (or whichever)
        ext = item.split('.')[1]
        Num = String[len(String.rstrip('0123456789')):]
        
        if Num.isdigit():
            NumList.append(SplitList(String, Num, ext)) # create numbered list
        else:
            WordList.append(SplitList(String,Num, ext)) # create ordered strings

    # Sort by alphabetically or numerically
    NumList.sort(key=itemgetter(1)) 
    WordList.sort(key=itemgetter(0))

    # Join list of list into just a list of word
    NumberedList = joinList(NumList)
    AlphaList = joinList(WordList)

    # final list placing numbers first
    return NumberedList + AlphaList

def SplitList(String, Num, Ext):
    SubList = []
    SubList.append(String)
    if Num.isdigit():
        try:
            SubList.append(int(float(Num)))
        except:
            SubList.append(Num)
    SubList.append(Ext)
    # Add SubList to Main List
    return SubList

def joinList(List):
    JoinedList = []
    for item in List:
        # Delete the number index so we have a clean list
        if len(item) == 3:
            del item[1]
        JoinedList.append('.'.join(item)) #word = '.'.join(word) 
    return JoinedList

def cli_progress_test(cur_val, end_val, bar_length=40, suffix=''):
    
    filled_len = int(round(bar_length * cur_val / float(end_val)))

    percents = round(100.0 * cur_val / float(end_val), 1)
    bar = '=' * filled_len + '-' * (bar_length - filled_len)

    print('[%s] %s%s ...%s\r\n' % (bar, percents, '%', suffix), flush=True)