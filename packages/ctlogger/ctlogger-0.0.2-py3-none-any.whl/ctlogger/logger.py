import time
import os
import inspect
from sys import stderr

ENV_DEBUG_MODE = 'VERBOSE'
ENV_ENABLE_TIME_PREFIX = 'ENABLE_TIME_PREFIX'
ENV_LINE_INFO_TO_STDERR = 'LINE_INFO_TO_STDERR'


ENABLE_DEBUG_MODE = os.environ.get(ENV_DEBUG_MODE)
ENABLE_TIME_PREFIX = os.environ.get(ENV_ENABLE_TIME_PREFIX)
ENABLE_LINE_INFO_TO_STDERR = os.environ.get(ENV_LINE_INFO_TO_STDERR)

time_format = '[%m-%d %H:%M:%S]'

END = '\x1b[0m'
__bgColors = {
    'BG_BLACK': '40',
    'BG_RED': '41',
    'BG_GREEN': '42',
    'BG_YELLOW': '43',
    'BG_BLUE': '44',
    'BG_MAGENTA': '45',
    'BG_CYAN': '46',
    'BG_WHITE': '47',
}

__effects = {
    'RESET': '0',  # all attributes off
    'BOLD': '1',  # Bold or increased intensity
    'FAINT': '2',  # Faint (decreased intensity), Not widely supported.
    'ITALIC': '3',  # Not widely supported. Sometimes treated as inverse.
    'UNDERLINE': '4',
}

__colors = {
    'BLACK': '30',
    'RED': '31',
    'GREEN': '32',
    'YELLOW': '33',
    'BLUE': '34',
    'MAGENTA': '35',
    'CYAN': '36',
    'WHITE': '37',
}

__fontColorForBGs = {
    'BG_BLACK': 'WHITE',
    'BG_RED': 'CYAN',
    'BG_GREEN': 'MAGENTA',
    'BG_YELLOW': 'BLUE',
    'BG_BLUE': 'YELLOW',
    'BG_MAGENTA': 'GREEN',
    'BG_CYAN': 'RED',
    'BG_WHITE': 'BLACK',
}

__CODE_DICT = {**__bgColors, **__effects, **__colors}


def get_all_options():
    return __CODE_DICT.keys()


def __transform_codes(codes):
    return '\x1b[' + ';'.join(codes) + 'm'


def by_codes(codes, *args, **kwargs):
    """
    This is core function
    """
    arguments = list(args)
    arguments.insert(0, __transform_codes(codes))
    if ENABLE_TIME_PREFIX:
        arguments.insert(0, time.strftime(time_format))

    arguments.append(END)
    print(*arguments, **kwargs)


def __show(title, d):
    cyan(title)
    italic(', '.join(d.keys()))


def show_opts():
    """
    BG__colors
    BG_BLACK, BG_RED, BG_GREEN, BG_YELLOW, BG_BLUE, BG_MAGENTA, BG_CYAN, BG_WHITE
    EFFECTS
    RESET, BOLD, FAINT, ITALIC, UNDERLINE
    COLORS
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
    """
    __show('BG__colors', __bgColors)
    __show('EFFECTS', __effects)
    __show('COLORS', __colors)


def __opts_to_codes(opts):
    opts_upper = [opt.upper() for opt in opts]
    try:
        codes = [__CODE_DICT[opt] for opt in opts_upper]
        return codes
    except KeyError:
        opts.insert(0, 'Unexpected options:')
        red(*opts)
        print('below are possible options(case insensitive)')
        show_opts()


def log(opts, *args):
    codes = __opts_to_codes(opts)
    if codes:
        by_codes(codes, *args)


def print_line_info(*args, **kwargs):
    """
    This function will print Filename/functionName:line at beggining.
    You can set environment variable LINE_INFO_TO_STDERR=1 to print this one to stderr
    """
    previous_frame = inspect.currentframe().f_back
    (filename, line_number, function_name, _, _) = inspect.getframeinfo(previous_frame)
    line_info = filename + ':' + str(line_number) + '/' + function_name
    if ENABLE_LINE_INFO_TO_STDERR:
        by_codes([__colors['RED']], line_info, *args, file=stderr)
    else:
        by_codes([__colors['RED']], line_info, *args)


def print_stack():
    frames = inspect.getouterframes(inspect.currentframe().f_back)
    for f in frames:
        print(f.filename + ':' + str(f.lineno) + '/' + f.function, f.code_context[0].replace(' ', ''), end='')


def debug(opts, *args):
    if ENABLE_DEBUG_MODE:
        log(opts, *args)


def __one_opt(opt):
    return lambda *args: log([opt], *args)


def __bg_color_shorthand(bg_color):
    def with_bg_color(*args):
        try:
            log([bg_color, __fontColorForBGs[bg_color.upper()]], *args)
        except KeyError:
            __show('BG__colors', __bgColors)

    return with_bg_color


def start(*opts):
    codes = __opts_to_codes(opts)
    print(__transform_codes(codes), end='')


def end():
    # Once start with bg color
    # Although using RESET to clear bgColor, but the spaces at the end still remain 1 line
    # Seems there a bug on osx?
    print(__transform_codes(['21', '22', '23', '24', __effects['RESET']]), end='')


black = __one_opt('black')
red = __one_opt('red')
green = __one_opt('green')
yellow = __one_opt('yellow')
blue = __one_opt('blue')
magenta = __one_opt('magenta')
cyan = __one_opt('cyan')
white = __one_opt('white')

bold = __one_opt('bold')
faint = __one_opt('faint')
italic = __one_opt('italic')
underline = __one_opt('underline')

#below are functions so they should be snake_case
bg_black = __bg_color_shorthand('bg_black')
bg_red = __bg_color_shorthand('bg_red')
bg_green = __bg_color_shorthand('bg_green')
bg_yellow = __bg_color_shorthand('bg_yellow')
bg_blue = __bg_color_shorthand('bg_blue')
bg_magenta = __bg_color_shorthand('bg_magenta')
bg_cyan = __bg_color_shorthand('bg_cyan')
bg_white = __bg_color_shorthand('bg_white')

if __name__ == '__main__':
    by_codes([__colors['RED'], __effects['ITALIC'], __bgColors['BG_GREEN']], 1, 2, 3)

    log(['red', 'Bg_Yellow', 'wrongOpt'], 3, 4, 5)
    debug(['BG_CYAN'], 'this is debug msg')

    print_line_info()


    def test():
        print_line_info('1', '2')
        print_stack()


    def a():
        test()


    a()

    green(123, 'abc')
    cyan('aa')

    bg_yellow('log with bg yellow')
    print('start', 'italic blue bg_green')

    start('italic', 'blue', 'bg_green')
    print('first', 'line')
    end()
    print('after', 'end()')
    print('after', 'end()')
