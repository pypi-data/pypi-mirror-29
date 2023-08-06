from operator import itemgetter
import datetime, sys, logging
from .LogGen import set_up_logging

logger = logging.getLogger(__name__)

def GetDate():
        logger.debug("Setting the date.")
        return datetime.date.today().strftime("%d%b%Y") # i.e. 15Feb2018

def NumberMe(List):
    #TODO This is creating silly errors such as:
    #FileNotFoundError: [Errno 2] No such file or directory: 
    #"/home/tom/Pictures/Wallpapers/['FT81c6h']"
    # As this is saving a list in a list, even though the list only has one item.
    # Need to 

        WordNum = []
        for item in List:
            SubList = ['','','']
            String = item.split('.')[0]# get value to the left of ".jpg" (or whichever)
            ext = item.split('.')[1]
            Num = String[len(String.rstrip('0123456789')):]
            # Add to list
            SubList[0] = String
            SubList[1] = Num
            SubList[2] = ext
            # Add SubList to Main List
            WordNum.append(SubList)

        # Sort by number, which has the index of 1 on each sublist
        WordNum.sort(key=itemgetter(1)) 

        # Print sorted list:
        # Error is here somewhere!
        for word in WordNum:
            # Delete the number index so we have a clean list
            del word[1]
            [str('.'.join(word)) if x==word else x for x in WordNum]
            print('.'.join(word))
            print(word)

        return WordNum

def cli_progress_test(cur_val, end_val, bar_length=60, suffix=''):
    
    filled_len = int(round(bar_length * cur_val / float(end_val)))

    percents = round(100.0 * cur_val / float(end_val), 1)
    bar = '=' * filled_len + '-' * (bar_length - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r\n' % (bar, percents, '%', suffix))
    sys.stdout.flush()