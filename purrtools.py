from time import sleep, mktime, gmtime, strftime
from datetime import datetime


def print_with_prepend(print_prepend='[+] ', print_string='', print_end='\n'):
    print('{}{}'.format(print_prepend, print_string), end=print_end)


def pause(initial_prompt='', amount=5, clear_pause_prompt=True):
    print_with_prepend('[+] ', initial_prompt)
    for tick in range(amount, 0, -1):
        print_with_prepend('[*] ', 'Pause ends in: {}    '.format(tick), '\r')
        sleep(1)
    if clear_pause_prompt:
        print('                                        ', end='\r')  # clear the line completely


def print_list(prompt='', list_to_print=[]):
    if len(list_to_print) == 0:
        print_with_prepend('[-] ', 'No list passed to be printed')
    else:
        print('[+] ', prompt)
        for element in list_to_print:
            print_with_prepend('\t', '> {}'.format(element))


def get_current_time(return_type='epoch'):
    current_time = datetime.now()
    current_time_epoch = int(mktime(current_time.timetuple()))
    if return_type == 'epoch':
        return current_time_epoch
    elif return_type == 'timestamp':
        current_time = strftime('%d/%m/%Y %H:%M:%S', gmtime(current_time_epoch))
        return current_time
    else:
        print_with_prepend('[-] ', 'No time return type requested')


def get_time_elapsed(new_time, old_time, return_type='hours', round_amount=2):
    if type(new_time) == datetime:
        new_time = mktime(new_time.timetuple())
    if type(old_time) == datetime:
        old_time = mktime(old_time.timetuple())
    epoch_passed = new_time - old_time
    if return_type == 'hours':
        epoch_passed = (epoch_passed / 60) / 60
    elif return_type == 'minutes':
        epoch_passed /= 60
    return round(epoch_passed, round_amount)


if __name__ == '__main__':
    pause('Testing pause', 2)
    test_list = ['hello', 'my', 'name', 'is', 'simon']
    print_list('Testing list printing:', test_list)
    print('Epoch: {} Timestamp: {}'.format(get_current_time('epoch'), get_current_time('timestamp')))
    print('Time elapsed from 01/01/70 00:00 to now: {}'.format(get_time_elapsed(get_current_time('epoch'), 0, 'seconds')))
