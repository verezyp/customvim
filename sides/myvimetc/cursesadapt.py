from abc import abstractmethod, ABC
import curses


class ITextModule(ABC):

    @abstractmethod
    def clear_scr(self):
        pass

    @abstractmethod
    def add_str(self, row: int, col: int, in_str: str):
        pass

    @abstractmethod
    def refresh_scr(self):
        pass

    @abstractmethod
    def cursor_move(self, y_pos: int, x_pos: int):
        pass

    @abstractmethod
    def getch(self):
        pass

    @abstractmethod
    def set_cursor(self, val):
        pass

    @abstractmethod
    def wrapper(self, func):
        pass

    @abstractmethod
    def end_win(self):
        pass

    @abstractmethod
    def cbreak(self):
        pass

    @abstractmethod
    def keypad(self, val):
        pass

    @abstractmethod
    def noecho(self):
        pass

    @abstractmethod
    def getmaxyx(self):
        pass

    @abstractmethod
    def start_config(self):
        pass

    @abstractmethod
    def newwin(self, nlines, ncols, beg_y, beg_x):
        pass

    @abstractmethod
    def win_clear(self, win):
        pass

    @abstractmethod
    def win_refresh(self, win):
        pass

    @abstractmethod
    def start_color(self):
        pass

    @abstractmethod
    def init_pair(self, num, color1, color2):
        pass

    @abstractmethod
    def win_addstr(self, y, x, s, win, color=None):
        pass


class CursesTextModule(ITextModule):
    def win_addstr(self, y, x, s, win, colornum=None):
        if colornum is None:
            win.addstr(y, x, s)
        else:
            win.addstr(y, x, s, curses.color_pair(colornum))

    def start_color(self):
        curses.start_color()

    def init_pair(self, num, color1, color2):
        if color1 == "RED":
            curses.init_pair(num, curses.COLOR_RED, curses.COLOR_BLACK)
        if color1 == "WHITE":
            curses.init_pair(num, curses.COLOR_WHITE, curses.COLOR_BLACK)

    _scr = None

    def __init__(self):
        self._scr = curses.initscr()

    def newwin(self, nlines, ncols, beg_y, beg_x):
        return curses.newwin(nlines, ncols, beg_y, beg_x)

    def win_clear(self, win):
        win.clear()

    def win_refresh(self, win):
        win.refresh()

    def start_config(self):
        curses.noecho()
        curses.cbreak()

    @property
    def screen(self):
        return self._scr

    def noecho(self):
        curses.noecho()

    def add_str(self, row, col, in_str):
        self._scr.addstr(row, col, in_str)

    def refresh_scr(self):
        self._scr.refresh()

    def cursor_move(self, y_pos: int, x_pos: int):
        self._scr.move(y_pos, x_pos)

    def getch(self):
        return self._scr.getch()

    def set_cursor(self, val):
        curses.curs_set(val)

    def clear_scr(self):
        self._scr.clear()

    def getyx(self):
        return self._scr.getyx()

    def end_win(self):
        curses.endwin()

    def wrapper(self, func):
        curses.wrapper(func)

    def cbreak(self):
        curses.cbreak()

    def keypad(self, val):
        self._scr.keypad(val)

    def getmaxyx(self):
        return self._scr.getmaxyx()


ALT_0 = 407
ALT_1 = 408
ALT_2 = 409
ALT_3 = 410
ALT_4 = 411
ALT_5 = 412
ALT_6 = 413
ALT_7 = 414
ALT_8 = 415
ALT_9 = 416
ALT_A = 417
ALT_B = 418
ALT_BKSP = 504
ALT_BQUOTE = 496
ALT_BSLASH = 528
ALT_C = 419
ALT_COMMA = 501
ALT_D = 420
ALT_DEL = 478
ALT_DOWN = 491
ALT_E = 421
ALT_END = 489
ALT_ENTER = 494
ALT_EQUAL = 485
ALT_ESC = 495
ALT_F = 422
ALT_FQUOTE = 500
ALT_FSLASH = 503
ALT_G = 423
ALT_H = 424
ALT_HOME = 486
ALT_I = 425
ALT_INS = 479
ALT_J = 426
ALT_K = 427
ALT_L = 428
ALT_LBRACKET = 497
ALT_LEFT = 493
ALT_M = 429
ALT_MINUS = 484
ALT_N = 430
ALT_O = 431
ALT_P = 432
ALT_PAD0 = 517
ALT_PAD1 = 518
ALT_PAD2 = 519
ALT_PAD3 = 520
ALT_PAD4 = 521
ALT_PAD5 = 522
ALT_PAD6 = 523
ALT_PAD7 = 524
ALT_PAD8 = 525
ALT_PAD9 = 526
ALT_PADENTER = 461
ALT_PADMINUS = 473
ALT_PADPLUS = 472
ALT_PADSLASH = 474
ALT_PADSTAR = 475
ALT_PADSTOP = 476
ALT_PGDN = 488
ALT_PGUP = 487
ALT_Q = 433
ALT_R = 434
ALT_RBRACKET = 498
ALT_RIGHT = 492
ALT_S = 435
ALT_SEMICOLON = 499
ALT_STOP = 502
ALT_T = 436
ALT_TAB = 483
ALT_U = 437
ALT_UP = 490
ALT_V = 438
ALT_W = 439
ALT_X = 440
ALT_Y = 441
ALT_Z = 442

A_ALTCHARSET = 65536
A_ATTRIBUTES = -65536
A_BLINK = 4194304
A_BOLD = 8388608
A_CHARTEXT = 65535
A_COLOR = -16777216
A_DIM = 0
A_HORIZONTAL = 0
A_INVIS = 0
A_ITALIC = 524288
A_LEFT = 262144
A_LOW = 0
A_NORMAL = 0
A_PROTECT = 0
A_REVERSE = 2097152
A_RIGHT = 131072
A_STANDOUT = 10485760
A_TOP = 0
A_UNDERLINE = 1048576
A_VERTICAL = 0

BUTTON1_CLICKED = 4

BUTTON1_DOUBLE_CLICKED = 8

BUTTON1_PRESSED = 2
BUTTON1_RELEASED = 1

BUTTON1_TRIPLE_CLICKED = 16

BUTTON2_CLICKED = 128

BUTTON2_DOUBLE_CLICKED = 256

BUTTON2_PRESSED = 64
BUTTON2_RELEASED = 32

BUTTON2_TRIPLE_CLICKED = 512

BUTTON3_CLICKED = 4096

BUTTON3_DOUBLE_CLICKED = 8192

BUTTON3_PRESSED = 2048
BUTTON3_RELEASED = 1024

BUTTON3_TRIPLE_CLICKED = 16384

BUTTON4_CLICKED = 131072

BUTTON4_DOUBLE_CLICKED = 262144

BUTTON4_PRESSED = 65536
BUTTON4_RELEASED = 32768

BUTTON4_TRIPLE_CLICKED = 524288

BUTTON5_CLICKED = 4194304

BUTTON5_DOUBLE_CLICKED = 8388608

BUTTON5_PRESSED = 2097152
BUTTON5_RELEASED = 1048576

BUTTON5_TRIPLE_CLICKED = 16777216

BUTTON_ALT = 268435456
BUTTON_CTRL = 134217728
BUTTON_SHIFT = 67108864

COLOR_BLACK = 0
COLOR_BLUE = 1
COLOR_CYAN = 3
COLOR_GREEN = 2
COLOR_MAGENTA = 5
COLOR_RED = 4
COLOR_WHITE = 7
COLOR_YELLOW = 6

CTL_BKSP = 505
CTL_DEL = 527
CTL_DOWN = 481
CTL_END = 448
CTL_ENTER = 529
CTL_HOME = 447
CTL_INS = 477
CTL_LEFT = 443
CTL_PAD0 = 507
CTL_PAD1 = 508
CTL_PAD2 = 509
CTL_PAD3 = 510
CTL_PAD4 = 511
CTL_PAD5 = 512
CTL_PAD6 = 513
CTL_PAD7 = 514
CTL_PAD8 = 515
CTL_PAD9 = 516
CTL_PADCENTER = 467
CTL_PADENTER = 460
CTL_PADMINUS = 469
CTL_PADPLUS = 468
CTL_PADSLASH = 470
CTL_PADSTAR = 471
CTL_PADSTOP = 466
CTL_PGDN = 446
CTL_PGUP = 445
CTL_RIGHT = 444
CTL_TAB = 482
CTL_UP = 480

ERR = -1

KEY_A1 = 449
KEY_A2 = 450
KEY_A3 = 451
KEY_ABORT = 348

KEY_ALT_L = 544
KEY_ALT_R = 545

KEY_B1 = 452
KEY_B2 = 453
KEY_B3 = 454
KEY_BACKSPACE = 263
KEY_BEG = 352
KEY_BREAK = 257
KEY_BTAB = 351
KEY_C1 = 455
KEY_C2 = 456
KEY_C3 = 457
KEY_CANCEL = 353
KEY_CATAB = 342
KEY_CLEAR = 333
KEY_CLOSE = 354
KEY_COMMAND = 355

KEY_CONTROL_L = 542
KEY_CONTROL_R = 543

KEY_COPY = 356
KEY_CREATE = 357
KEY_CTAB = 341
KEY_DC = 330
KEY_DL = 328
KEY_DOWN = 258
KEY_EIC = 332
KEY_END = 358
KEY_ENTER = 343
KEY_EOL = 335
KEY_EOS = 334
KEY_EXIT = 359
KEY_F0 = 264
KEY_F1 = 265
KEY_F10 = 274
KEY_F11 = 275
KEY_F12 = 276
KEY_F13 = 277
KEY_F14 = 278
KEY_F15 = 279
KEY_F16 = 280
KEY_F17 = 281
KEY_F18 = 282
KEY_F19 = 283
KEY_F2 = 266
KEY_F20 = 284
KEY_F21 = 285
KEY_F22 = 286
KEY_F23 = 287
KEY_F24 = 288
KEY_F25 = 289
KEY_F26 = 290
KEY_F27 = 291
KEY_F28 = 292
KEY_F29 = 293
KEY_F3 = 267
KEY_F30 = 294
KEY_F31 = 295
KEY_F32 = 296
KEY_F33 = 297
KEY_F34 = 298
KEY_F35 = 299
KEY_F36 = 300
KEY_F37 = 301
KEY_F38 = 302
KEY_F39 = 303
KEY_F4 = 268
KEY_F40 = 304
KEY_F41 = 305
KEY_F42 = 306
KEY_F43 = 307
KEY_F44 = 308
KEY_F45 = 309
KEY_F46 = 310
KEY_F47 = 311
KEY_F48 = 312
KEY_F49 = 313
KEY_F5 = 269
KEY_F50 = 314
KEY_F51 = 315
KEY_F52 = 316
KEY_F53 = 317
KEY_F54 = 318
KEY_F55 = 319
KEY_F56 = 320
KEY_F57 = 321
KEY_F58 = 322
KEY_F59 = 323
KEY_F6 = 270
KEY_F60 = 324
KEY_F61 = 325
KEY_F62 = 326
KEY_F63 = 327
KEY_F7 = 271
KEY_F8 = 272
KEY_F9 = 273
KEY_FIND = 360
KEY_HELP = 361
KEY_HOME = 262
KEY_IC = 331
KEY_IL = 329
KEY_LEFT = 260
KEY_LHELP = 350
KEY_LL = 347
KEY_MARK = 362
KEY_MAX = 548
KEY_MESSAGE = 363
KEY_MIN = 257
KEY_MOUSE = 539
KEY_MOVE = 364
KEY_NEXT = 365
KEY_NPAGE = 338
KEY_OPEN = 366
KEY_OPTIONS = 367
KEY_PPAGE = 339
KEY_PREVIOUS = 368
KEY_PRINT = 346
KEY_REDO = 369
KEY_REFERENCE = 370
KEY_REFRESH = 371
KEY_REPLACE = 372
KEY_RESET = 345
KEY_RESIZE = 546
KEY_RESTART = 373
KEY_RESUME = 374
KEY_RIGHT = 261
KEY_SAVE = 375
KEY_SBEG = 376
KEY_SCANCEL = 377
KEY_SCOMMAND = 378
KEY_SCOPY = 379
KEY_SCREATE = 380
KEY_SDC = 381
KEY_SDL = 382
KEY_SELECT = 383
KEY_SEND = 384
KEY_SEOL = 385
KEY_SEXIT = 386
KEY_SF = 336
KEY_SFIND = 387
KEY_SHELP = 349

KEY_SHIFT_L = 540
KEY_SHIFT_R = 541

KEY_SHOME = 388
KEY_SIC = 389
KEY_SLEFT = 391
KEY_SMESSAGE = 392
KEY_SMOVE = 393
KEY_SNEXT = 394
KEY_SOPTIONS = 395
KEY_SPREVIOUS = 396
KEY_SPRINT = 397
KEY_SR = 337
KEY_SREDO = 398
KEY_SREPLACE = 399
KEY_SRESET = 344
KEY_SRIGHT = 400
KEY_SRSUME = 401
KEY_SSAVE = 402
KEY_SSUSPEND = 403
KEY_STAB = 340
KEY_SUNDO = 404
KEY_SUP = 547
KEY_SUSPEND = 405
KEY_UNDO = 406
KEY_UP = 259

OK = 0

PAD0 = 506
PADENTER = 459
PADMINUS = 464
PADPLUS = 465
PADSLASH = 458
PADSTAR = 463
PADSTOP = 462

REPORT_MOUSE_POSITION = 536870912

SHF_DC = 538
SHF_DOWN = 536
SHF_IC = 537
SHF_PADENTER = 530
SHF_PADMINUS = 534
SHF_PADPLUS = 533
SHF_PADSLASH = 531
SHF_PADSTAR = 532
SHF_UP = 535
