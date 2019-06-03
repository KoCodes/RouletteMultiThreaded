import multiprocessing as mp
import random as rnd
import threading
import time

print_lock = threading.Lock()

class TableClass:

    def __init__(self, red, black, win_loss, max_turns, biggest_play, Old_roll, row_not_red, row_not_black,
                 Longest_row_not_red, Longest_row_not_black, stats_red_black_green, roll, i, idx):
        self.red = red
        self.black = black
        self.win_loss = win_loss
        self.max_turns = max_turns
        self.biggest_play = biggest_play
        self.Old_roll = Old_roll
        self.row_not_red = row_not_red
        self.row_not_black = row_not_black
        self.Longest_row_not_red = Longest_row_not_red
        self.Longest_row_not_black = Longest_row_not_black
        self.stats_red_black_green = stats_red_black_green
        self.roll = roll
        self.i = i
        self.idx = idx

    def print_variables(self):
        print(list(vars(TableClass)))


def start_roulette(idx):
    with print_lock:
        print(f'starting worker: {idx}')
        # print(red_marks, black_marks)
    while table[idx].i < table[idx].max_turns:
        table[idx].win_loss -= table[idx].black + table[idx].red
        table[idx].roll = rnd.randint(0, 36)

        if table[idx].roll not in red_marks:
            table[idx].row_not_red += 1
            if not table[idx].roll == 0: table[idx].row_not_black = 0
            if table[idx].Old_roll not in red_marks:
                if table[idx].row_not_red > table[idx].Longest_row_not_red:
                    table[idx].Longest_row_not_red = table[idx].row_not_red
        if table[idx].roll not in black_marks:
            table[idx].row_not_black += 1
            if not table[idx].roll == 0: table[idx].row_not_red = 0
            if table[idx].Old_roll not in black_marks:
                if table[idx].row_not_black > table[idx].Longest_row_not_black:
                    table[idx].Longest_row_not_black = table[idx].row_not_black
        else:
            table[idx].row_not_red = 0
            table[idx].row_not_black = 0


        if table[idx].roll in red_marks:
            if debug: print('table[idx].red: ', table[idx].roll)
            table[idx].win_loss += table[idx].red * 2
            table[idx].red = 1
            table[idx].black *= 2
            table[idx].stats_red_black_green[1][0] += 1
        elif table[idx].roll in black_marks:
            if debug: print('table[idx].black: ', table[idx].roll)
            table[idx].win_loss += table[idx].black * 2
            table[idx].black = 1
            table[idx].red *= 2
            table[idx].stats_red_black_green[1][1] += 1
        else:
            if debug: print('green: ', table[idx].roll)
            table[idx].red *= 2
            table[idx].black *= 2
            table[idx].stats_red_black_green[1][2] += 1
        if debug: print(f"table[idx].red play: {table[idx].red}, table[idx].black play: {table[idx].black}\n")

        if table[idx].red > table[idx].biggest_play:
            table[idx].biggest_play = table[idx].red
        elif table[idx].black > table[idx].biggest_play:
            table[idx].biggest_play = table[idx].black

        table[idx].Old_roll = table[idx].roll
        if table[idx].i == table[idx].max_turns-1:
            if table[idx].row_not_black > 1 or table[idx].row_not_red > 1:
                table[idx].max_turns += 1


        if table[idx].i == max_i and debug:
            with print_lock:
                print(f'worker: {idx}: ', ', '.join("%s: %s" % item for item in vars(table[idx]).items()))
            exit()

        table[idx].i += 1
    with print_lock:
        # print(f'worker: {idx} finished: ', vars(table[idx]))
        print(f'worker: {idx} finished')
    return vars(table[idx])


def main(results):
    # Step 1: Init multiprocessing.Pool()
    pool = mp.Pool(tot_threads)
    # results = [pool.apply_async(howmany_within_range, args=(row, 4, 8)) for row in data]
    results = pool.map(start_roulette, [idx for idx in range(tot_jobs)])
    # results = pool.starmap(start_roulette, [(row, 4, 8) for row in data])
    # pool.starmap_async(howmany_within_range2, [(row, 4, 8) for row in range(int(mp.cpu_count()/2))])
    # results = pool.starmap_async(howmany_within_range2, [(i, row, 4, 8) for i, row in enumerate(data)]).get()
    # results = pool.map_async(howmany_within_range_rowonly, [row for row in data]).get()
    # # Step 3: Don't forget to close
    pool.close()
    # print('\n', '\n'.join(map(str, results)))
    return results


red = 1
black = 1
win_loss = 0
max_turns = int(1e7)  # total number of turns that will be divided over the jobs and threads
# Constants below
red_marks = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black_marks = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
stats_red_black_green = [['Red', 'Black', 'Green'], [0, 0, 0]]
debug = False
max_i = 100
tot_jobs = 20
tot_threads = 10
turns_divided = int(max_turns / tot_jobs)
if tot_threads > mp.cpu_count(): tot_threads = int(mp.cpu_count() * 0.8)
# print("{:,}".format(turns_divided))
# exit()

table = {}
for x in range(0, tot_jobs):
    table["string{0}".format(x)] = "Table" + str(x)
    table[x] = TableClass(red=red, black=black, win_loss=win_loss, max_turns=turns_divided, biggest_play=0,
                          Old_roll=50, row_not_red=0, row_not_black=0,
                          Longest_row_not_red=0, Longest_row_not_black=0,
                          stats_red_black_green=stats_red_black_green, roll=0, i=0, idx=x)

if __name__ == '__main__':
    # freeze_support() here if program needs to be frozen
    start = time.time()
    output = []
    output = main(output)
    # print('\nOutput: ', '\n'.join(map(str, output)))  #raw output of each roulette table

    biggest_play, Longest_row_not_red, Longest_row_not_black = 0, 0, 0
    stats_red_black_green2 = [0, 0, 0]
    for row in output:  #combine all tables into the final results
        win_loss += row.get('win_loss', )
        max_turns += row.get('max_turns', )
        stats_red_black_green1 = row.get('stats_red_black_green', )
        stats_red_black_green2 = [x + y for x, y in zip(stats_red_black_green2, stats_red_black_green1[1])]
        if row.get('biggest_play', ) > biggest_play: biggest_play = row.get('biggest_play', )
        if row.get('Longest_row_not_red', ) > Longest_row_not_red: Longest_row_not_red = row.get(
            'Longest_row_not_red', )
        if row.get('Longest_row_not_black', ) > Longest_row_not_black: Longest_row_not_black = row.get(
            'Longest_row_not_black', )
    stats_red_black_green[1] = stats_red_black_green2

# PRINT FINAL RESULTS
    print(f"""\nFinal Results with {'{:,}'.format(max_turns)} turns:
win_loss: {'{:,}'.format(win_loss)}
max_turns: {'{:,}'.format(max_turns)}
biggest_play: {'{:,}'.format(biggest_play)}
Longest not red: {Longest_row_not_red}
Longest_row_not_black: {Longest_row_not_black}
stats: {stats_red_black_green}""")
    print(f'\nEntire job took:{time.time() - start}\nWith {tot_threads} Threads')

