import copy
import random

"""
This file is for part 2 of HW 2 of CS 440 Spring 2018.
Creates and runs AI actors in a simulation of Gomoku
Note all accesses are all in (y, x)

"""


class Board:
    field = []  # the game field
    field_watcher = []
    turn_number = 1
    winner = '.'
    red_ticker = 'a'
    blue_ticker = 'b'

    def __init__(self):
        for i in range(0, 7):
            self.field.append([0, 0, 0, 0, 0, 0, 0])
            self.field_watcher.append([0, 0, 0, 0, 0, 0, 0])
            for j in range(0, 7):
                self.field[i][j] = '.'
                self.field_watcher[i][j] = '.'

    def print_board(self):
        print("  0 1 2 3 4 5 6")
        for i in range(0, 7):
            print(str(i) + " ", end="")
            for j in range(0, 7):
                print(str(self.field[i][j]) + " ", end="")
            print("")

    def get_all_nodes(self, cid):
        """
        Gets all the nodes that match a cid
        :param cid: the current id
        :return: a list of tuples that match
        """
        output = []
        for i in range(0, 7):
            for j in range(0, 7):
                if self.field[i][j] == cid:
                    output.append((i, j))
        return output

    def check_full(self):
        """
        Checks if the board is full. If it is, then return True and set the winner to "&"
        :return: a bool if it is full or not
        """
        full = True
        for i in range(0, 7):
            for j in range(0, 7):
                if self.field[i][j] == '.':
                    full = False
        if full:
            self.winner = "&"

        return full

    def update_field(self):
        for i in range(0, 7):
            for j in range(0, 7):
                if (self.field[i][j] == 'R' or self.field[i][j] == 'B') and (self.field_watcher[i][j] == '.'):
                    if self.field[i][j] == 'R':
                        self.field_watcher[i][j] = self.red_ticker
                        self.red_ticker = (chr(ord(self.red_ticker)+1))
                    elif self.field[i][j] == 'B':
                        self.field_watcher[i][j] = self.blue_ticker
                        self.blue_ticker = (chr(ord(self.blue_ticker) + 1))

    def print_watcher(self):
        print("  0 1 2 3 4 5 6")
        for i in range(0, 7):
            print(str(i) + " ", end="")
            for j in range(0, 7):
                print(str(self.field_watcher[i][j]) + " ", end="")
            print("")

    def check_winner(self, field, cid):
        """
        Check if cid has won on the current board
        This is a modified get win segs. Check if there's a sequence of 5 and return True if there are any
        :return: bool if cid has won
        """
        win_segs = []
        # look at right segs
        for i in range(0, 7):
            for j in range(0, 3):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if field[i][j + count] == cid:
                        win_seg.append((i, j + count))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        # look at upward segs
        for i in range(4, 7):
            for j in range(0, 7):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if field[i - count][j] == cid:
                        win_seg.append((i - count, j))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        # look at NorthWestern segs
        for i in range(4, 6 + 1):
            for j in range(0, 3):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if field[i - count][j + count] == cid:
                        win_seg.append((i - count, j + count))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        # look at SouthWestern segs
        for i in range(0, 3):
            for j in range(0, 3):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if field[i + count][j + count] == cid:
                        win_seg.append((i + count, j + count))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        return len(win_segs) > 0

    def check_possible(self, field, mid, oid):
        """
        Checks to see if a board state is possible (2 winners)
        :param field: my gamefield
        :param mid: first id
        :param oid: second id
        :return: True if possible, False if impossible
        """
        return not (self.check_winner(field, mid) and self.check_winner(field, oid))


class ReflexAgent:
    mid = ''  # My ID
    oid = ''  # Opponents ID

    def __init__(self, ID, oID):
        self.mid = ID
        self.oid = oID

    def get_my_stones(self, b, cid):
        """
        Gets all stones that match the current id
        :param b: board
        :param cid: current id
        :return: list of tuples (column, row) that matches the cid
        """
        my_stones = []
        for i in range(0, 7):
            for j in range(0, 7):
                if b.field[i][j] == cid:
                    my_stones.append((i, j))
        return my_stones

    def instant_win(self, b, cid, oid):
        """
        Checks if there's a single move that wins
        :param b: board
        :param cid: current id
        :return: (-420, -420) if there is none, the tuple if there is such a move
        """
        my_stones = self.get_my_stones(b, cid)
        # Check if there's a 4 in a row with an open slot
        for s in my_stones:
            # check up
            found_best = True
            for count in range(1, 3 + 1):
                cand = (s[0] - count, s[1])
                if cand not in my_stones or s[0] - count < 0:
                    found_best = False
                    break
            if found_best:
                best = (s[0] - 4, s[1])
                if s[0] - 4 >= 0 and b.field[best[0]][best[1]] == ".":
                    #place in top most
                    return best
                best = (s[0] + 1, s[1])
                if s[0] + 1 <= 6 and b.field[best[0]][best[1]] == ".":
                    #place in bottom most
                    return best

            # check right
            found_best = True
            for count in range(1, 3 + 1):
                cand = (s[0], s[1] + count)
                if cand not in my_stones or s[1] + count > 6:
                    found_best = False
                    break
            if found_best:
                best = (s[0], s[1] + 4)
                if s[1] + 4 <= 6 and b.field[best[0]][best[1]] == ".":
                    #place at right most
                    return best
                best = (s[0], s[1] - 1)
                if s[1] - 1 >= 0 and b.field[best[0]][best[1]] == ".":
                    #place at left most
                    return best

            # check northeast
            found_best = True
            for count in range(1, 3 + 1):
                cand = (s[0] - count, s[1] + count)
                if cand not in my_stones or s[0] - count < 0 or s[1] + count > 6:
                    found_best = False
                    break
            if found_best:
                best = (s[0] - 4, s[1] + 4)
                if s[0] - 4 >= 0 and s[1] + 4 <= 6 and b.field[best[0]][best[1]] == ".":
                    # place at northeastern
                    return best
                best = (s[0] + 1, s[1] - 1)
                if s[0] + 1 <= 6 and s[1] - 1 >= 0 and b.field[best[0]][best[1]] == ".":
                    # place at southwestern
                    return best

            # check southeast
            found_best = True
            for count in range(1, 3 + 1):
                cand = (s[0] + count, s[1] + count)
                if cand not in my_stones or s[0] + count > 6 or s[1] + count > 6:
                    found_best = False
                    break
            if found_best:
                best = (s[0] + 4, s[1] + 4)
                if s[0] + 4 <= 6 and s[1] + 4 <= 6 and b.field[best[0]][best[1]] == ".":
                    # place at southeastern
                    return best
                best = (s[0] - 1, s[1] - 1)
                if s[0] - 1 >= 0 and s[1] - 1 >= 0 and b.field[best[0]][best[1]] == ".":
                    # place at northwestern
                    return best

        # Check for a "R R . R R" win condition.
        win_segs = self.find_all_win_segs(b, oid)

        # catch if no more winning segments, just play down left most valid
        if len(win_segs) == 0:
            all_empty = b.get_all_nodes('.')
            leftmost = min(all_empty, key=lambda t: t[1])
            leftmostvalues = [y for y in all_empty if y[1] == leftmost[1]]
            downleftmost = max(leftmostvalues, key=lambda t: t[0])
            return -420, -420

        # has winning segments score all the segments (1 stone is 1 point)
        win_seg_count = {}
        for ws in win_segs:
            score = 0
            for t in ws:
                if b.field[t[0]][t[1]] == cid:
                    score += 1
            win_seg_count[tuple(ws)] = score

        # check if best score is 4, the instant win
        best_score = max(win_seg_count.values())
        if best_score == 4:
            # this calculates the most left and the most downward position that that matches the best score (4)
            win_seg_best = [y for y in win_seg_count.keys() if win_seg_count[y] == best_score]
            leftmost = min(win_seg_best, key=lambda t: t[1])[0]
            leftmostvalues = [y for y in win_seg_best if y[0][1] == leftmost[1]]
            downleftmost = max(leftmostvalues, key=lambda t: t[0])

            for pos in downleftmost:
                if b.field[pos[0]][pos[1]] == '.':
                    return pos

        return -420, -420

    def find_triple_chain_empty(self, b, cid):
        """
        For step 3 of the prompt, looks for a chain of three rocks that matches the cid with open ends
        If its on the edge, only consider the end that's on the board
        :param b: board
        :param cid: current id
        :return: the left-down most chain of three that matches the cid
        """
        my_stones = self.get_my_stones(b, cid)
        for s in my_stones:
            #check up
            found_best = True
            for count in range(1, 2 + 1):
                cand = (s[0] - count, s[1])
                if cand not in my_stones or s[0] - count < 0:
                    found_best = False
                    break
            if found_best:
                head1 = (s[0] + 1, s[1])
                head2 = (s[0] - 3, s[1])
                if s[0] + 1 <= 6 and s[0] - 3 >= 0 and \
                    b.field[head1[0]][head1[1]] == "." and b.field[head2[0]][head2[1]] == ".":
                    # normal case not at beginning or end
                    return head1, head2
                elif s[0] == 6 and b.field[head2[0]][head2[1]] == ".":
                    # at very bottom, top can be valid
                    return head2, head1
                elif s[0] - 2 == 0 and b.field[head1[0]][head1[1]] == ".":
                    # at very top, bottom can be valid
                    return head1, head2

            #check right
            found_best = True
            for count in range(1, 2 + 1):
                cand = (s[0], s[1] + count)
                if cand not in my_stones or s[1] + count > 6:
                    found_best = False
                    break
            if found_best:
                head1 = (s[0], s[1] - 1)
                head2 = (s[0], s[1] + 3)
                if s[1] - 1 >= 0 and s[1] + 3 <= 6 and \
                    b.field[head1[0]][head1[1]] == "." and b.field[head2[0]][head2[1]] == ".":
                    #normal
                    return head1, head2
                elif s[1] == 0 and b.field[head2[0]][head2[1]] == ".":
                    # at very left, right can be valid
                    return head2, head1
                elif s[1] == 6 and b.field[head1[0]][head1[1]] == ".":
                    # at very right, left can be valid
                    return head1, head2

            # check northwestern
            found_best = True
            for count in range(1, 2 + 1):
                cand = (s[0] - count, s[1] + count)
                if cand not in my_stones or s[0] - count < 0 or s[1] + count > 6:
                    found_best = False
                    break
            if found_best:
                head1 = (s[0] + 1, s[1] - 1)
                head2 = (s[0] - 3, s[1] + 3)
                if s[0] + 1 <= 6 and s[0] - 3 >= 0 and \
                    s[1] - 1 >= 0 and s[1] + 3 <= 6 and \
                    b.field[head1[0]][head1[1]] == "." and b.field[head2[0]][head2[1]] == ".":
                    return head1, head2
                elif (s[0] == 6 or s[1] == 0) and \
                        s[0] - 3 >= 0 and s[1] + 3 <= 6 and \
                        b.field[head2[0]][head2[1]] == ".":
                    # at bottom left corner, top right can be valid
                    return head2, head1
                elif (s[0] - 2 == 0 or s[1] + 2 == 6) and \
                        s[0] + 1 <= 6 and s[1] - 1 >= 0 and \
                        b.field[head1[0]][head1[1]] == ".":
                    # at top right corner, bottom left can be valid
                    return head1, head2

            # check southwestern
            found_best = True
            for count in range(1, 2 + 1):
                cand = (s[0] + count, s[1] + count)
                if cand not in my_stones or s[0] + count > 6 or s[1] + count > 6:
                    found_best = False
                    break
            if found_best:
                head1 = (s[0] - 1, s[1] - 1)
                head2 = (s[0] + 3, s[1] + 3)
                if s[0] - 1 >= 0 and s[0] + 3 <= 6 and \
                        s[1] - 1 >= 0 and s[1] + 3 <= 6 and \
                        b.field[head1[0]][head1[1]] == "." and b.field[head2[0]][head2[1]] == ".":
                    return head1, head2
                elif (s[0] == 0 or s[1] == 0) and \
                        s[0] + 3 <= 6 and s[1] + 3 <=6 and \
                        b.field[head2[0]][head2[1]] == ".":
                    # at top left, bottom right can be valid
                    return head2, head1
                elif (s[0] + 2 == 0 or s[1] + 2 == 6) and \
                        s[0] - 1 >= 0 and s[1] - 1 >= 0 and \
                        b.field[head1[0]][head1[1]] == ".":
                    # at bottom right, top left can be valid
                    return head1, head2

        return -420, -420

    def find_all_win_segs(self, b, oid):
        """
        For step 4, gets all possible winning segments: blocks of 5 where there isn't my opponents stone
        :param b: board
        :param oid: opponenets id
        :return: a list of lists: the sublists hold 5 tuples that match that winning segment
        """
        win_segs = []
        # look at right segs
        for i in range(0, 7):
            for j in range(0, 3):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if b.field[i][j + count] != oid:
                        win_seg.append((i, j+count))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        # look at upward segs
        for i in range(4, 7):
            for j in range(0, 7):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if b.field[i - count][j] != oid:
                        win_seg.append((i - count, j))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        # look at NorthWestern segs
        for i in range(4, 6 + 1):
            for j in range(0, 3):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if b.field[i - count][j + count] != oid:
                        win_seg.append((i - count, j + count))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        # look at SouthWestern segs
        for i in range(0, 3):
            for j in range(0, 3):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if b.field[i + count][j + count] != oid:
                        win_seg.append((i + count, j + count))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        return win_segs

    def win_seg_move(self, b, mid, oid):
        """
        For step 4, calculates the best move to make with the step 4 algorithm.
        Find the down left most position to place a stone that can still win.
        If there are no more winning positions, then returns the down left most valid position.
        :param b: board
        :param mid: my id
        :param oid: opponents id
        :return: the move
        """
        win_segs = self.find_all_win_segs(b, oid)

        # catch if no more winning segments, just play down left most valid
        if len(win_segs) == 0:
            # catch if no more winning segments, just play down left most valid
            all_empty = b.get_all_nodes('.')
            leftmost = min(all_empty, key=lambda t: t[1])
            leftmostvalues = [y for y in all_empty if y[1] == leftmost[1]]
            downleftmost = max(leftmostvalues, key=lambda t: t[0])
            return downleftmost

        # has winning segments score all the segments (1 stone is 1 point)
        win_seg_count = {}
        for ws in win_segs:
            score = 0
            for t in ws:
                if b.field[t[0]][t[1]] == mid:
                    score += 1
            win_seg_count[tuple(ws)] = score

        # this calculates the most left and the most downward position that that matches the best score
        best_score = max(win_seg_count.values())
        win_seg_best = [y for y in win_seg_count.keys() if win_seg_count[y] == best_score]
        leftmost = min(win_seg_best, key=lambda t: t[1])[0]
        leftmostvalues = [y for y in win_seg_best if y[0][1] == leftmost[1]]
        downleftmost = max(leftmostvalues, key=lambda t: t[0])

        #return the the most left most down stone that is adjacent to another stone
        for count in range(0, 5):
            cand = downleftmost[count]
            candprev = (-420, -420)
            if count > 0:
                candprev = downleftmost[count-1]
            candnext = (-420, -420)
            if count < 4:
                candnext = downleftmost[count+1]
            if b.field[cand[0]][cand[1]] == '.' and (
                    (candprev != (-420, -420) and b.field[candprev[0]][candprev[1]] == mid) or
                    (candnext != (-420, -420) and b.field[candnext[0]][candnext[1]] == mid)):
                return cand

        #default, should never reach this
        return downleftmost[0]

    def make_move(self, b):
        """
        Top level function. Make a move following the rules given
        :param b: board
        :return: None, modifies the board's field
        """
        if b.check_full():
            return

        if b.turn_number == 1:
            pass # can add a random later here for strategies

        # Part 1
        best_move = self.instant_win(b, self.mid, self.oid)
        if best_move != (-420, -420):
            b.field[best_move[0]][best_move[1]] = self.mid
            b.winner = self.mid
            return

        # Part 2
        best_move = self.instant_win(b, self.oid, self.mid)
        if best_move != (-420, -420):
            b.field[best_move[0]][best_move[1]] = self.mid
            return

        # Part 3
        empty_triple = self.find_triple_chain_empty(b, self.oid)
        if empty_triple != (-420, -420):
            b.field[empty_triple[0][0]][empty_triple[0][1]] = self.mid
            return

        # Part 4
        best_move = self.win_seg_move(b, self.mid, self.oid)
        b.field[best_move[0]][best_move[1]] = self.mid
        return


class MiniMaxAgent:
    mid = ''  # My ID
    oid = ''  # Opponents ID
    is_alpha_beta = False
    name = ''
    nodes_expanded_list = []

    def __init__(self, ID, oID, is_alpha_beta_in, NAME):
        self.mid = ID
        self.oid = oID
        self.is_alpha_beta = is_alpha_beta_in
        self.name = NAME

    def make_move(self, b):
        # build my minimax tree
        root = self.init_tree(b, self.mid, self.oid)

        # fill all my nodes with values
        if self.is_alpha_beta:
            self.alpha_beta(root)
        else:
            self.evaluate(root)

        # get the optimal move in this case
        best_move = self.return_best_move(root)

        # make my move
        b.field[best_move[0]][best_move[1]] = self.mid

        return

    def init_tree(self, b, mid, oid):
        # initialize the depth of 0
        level_0_field = copy.deepcopy(b.field)
        level_0_node = {'type': 'max',
                        'mid': mid,
                        'children': [],
                        'value': 0,
                        'initial_board': level_0_field,
                        'move': (-420, -420)}

        # initialize the depth of 1
        moves = self.get_all_moves(level_0_node['initial_board'])
        for m in moves:
            new_field = copy.deepcopy(level_0_node['initial_board'])
            new_field[m[0]][m[1]] = level_0_node['mid']
            if b.check_possible(new_field, mid, oid):
                level_1_node = {'type': 'min',
                            'mid': oid,
                            'children': [],
                            'value': 0,
                            'initial_board': new_field,
                            'move': m}
                level_0_node['children'].append(level_1_node)

        # initialize the depth of 2
        for level_1_node in level_0_node['children']:
            moves = self.get_all_moves(level_1_node['initial_board'])
            for m in moves:
                new_field = copy.deepcopy(level_1_node['initial_board'])
                new_field[m[0]][m[1]] = level_1_node['mid']
                if b.check_possible(new_field, mid, oid):
                    level_2_node = {'type': 'max',
                                'mid': mid,
                                'children': [],
                                'value': 0,
                                'initial_board': new_field,
                                'move': m}
                    level_1_node['children'].append(level_2_node)

        # initialize the depth of 3
        for level_1_node in level_0_node['children']:
            for level_2_node in level_1_node['children']:
                moves = self.get_all_moves(level_1_node['initial_board'])
                for m in moves:
                    new_field = copy.deepcopy(level_2_node['initial_board'])
                    new_field[m[0]][m[1]] = level_2_node['mid']
                    if b.check_possible(new_field, mid, oid):
                        level_3_node = {'type': 'state',
                                    'mid': '@',
                                    'children': [],
                                    'value': 0,
                                    'initial_board': new_field,
                                    'move': m}
                        level_2_node['children'].append(level_3_node)

        return level_0_node

    def find_all_win_segs(self, field, oid):
        win_segs = []
        # look at right segs
        for i in range(0, 7):
            for j in range(0, 3):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if field[i][j + count] != oid:
                        win_seg.append((i, j + count))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        # look at upward segs
        for i in range(4, 7):
            for j in range(0, 7):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if field[i - count][j] != oid:
                        win_seg.append((i - count, j))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        # look at NorthWestern segs
        for i in range(4, 6 + 1):
            for j in range(0, 3):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if field[i - count][j + count] != oid:
                        win_seg.append((i - count, j + count))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        # look at SouthWestern segs
        for i in range(0, 3):
            for j in range(0, 3):
                # attempt to build win seg
                win_seg = []
                good_win = True
                for count in range(0, 4 + 1):
                    if field[i + count][j + count] != oid:
                        win_seg.append((i + count, j + count))
                    else:
                        good_win = False
                        break
                if good_win:
                    win_segs.append(win_seg)

        return win_segs

    def check_full(self, field):
        full = True
        for i in range(0, 7):
            for j in range(0, 7):
                if field[i][j] == '.':
                    full = False
                    break
        return full

    def eval_function(self, field):
        w4 = 1000
        w3 = 500
        w2 = 100
        w1 = 30
        w0 = 10
        # this is calculating my chains
        win_segs = self.find_all_win_segs(field, self.oid)
        chainr = [0, 0, 0, 0, 0, 0]  # segs length 0,1, 2,3,4,5
        weightr = 0;
        # has winning segments score all the segments (1 stone is 1 point)
        win_seg_count = {}
        for ws in win_segs:
            score = 0
            for t in ws:
                if field[t[0]][t[1]] == self.mid:
                    score += 1
            chainr[score] += 1  # increment the chain by that #
        weightr = chainr[0] * w0 + chainr[1] * w1 + chainr[2] * w2 + chainr[3] * w3 + chainr[4] * w4
        win_segsb = self.find_all_win_segs(field, self.mid)
        chainb = [0, 0, 0, 0, 0, 0]  # segs length 0,1, 2,3,4,5
        weightb = 0;

        # has winning segments score all the segments (1 stone is 1 point)
        win_seg_count = {}
        for ws in win_segsb:
            score = 0
            for t in ws:
                if field[t[0]][t[1]] == self.oid:  # used to be b.field
                    score += 1

            # win_seg_count[tuple(ws)] = score
            chainb[score] += 1  # increment the chain by that #
        weightb = chainb[0] * w0 + chainb[1] * w1 + chainb[2] * w2 + chainb[3] * w3 + chainb[4] * w4
        if (chainr[5] != 0 or chainr[
            4] >= 2):  # r won ***** doesn't take into account situation where it's the same open spot for both 4 chains for opponnet to prevent
            return float('inf')
        if (chainb[5] != 0 or chainb[4] >= 2):  # b won
            return float('-inf')
        if (self.check_full(field)):
            return 0
        return weightr - weightb

    def evaluate(self, level_0_node):
        nodes_expanded = 0
        # evaluate all states at depth 3 (state)
        for level_1_node in level_0_node['children']:
            for level_2_node in level_1_node['children']:
                for level_3_node in level_2_node['children']:
                    level_3_node['value'] = self.eval_function(level_3_node['initial_board'])
                    nodes_expanded += 1

        # evaluate best states at depth 2 (max)
        for level_1_node in level_0_node['children']:
            for level_2_node in level_1_node['children']:
                values = []
                for level_3_node in level_2_node['children']:
                    values.append(level_3_node['value'])
                level_2_node['value'] = max(values)

        # evaluate best states at depth 1 (min)
        for level_1_node in level_0_node['children']:
            values = []
            for level_2_node in level_1_node['children']:
                values.append(level_2_node['value'])
            level_1_node['value'] = min(values)

        # evaluate best states at depth 0 (max)
        values = []
        for level_1_node in level_0_node['children']:
            values.append(level_1_node['value'])
        level_0_node['value'] = max(values)

        self.nodes_expanded_list.append(nodes_expanded)

    def alpha_beta(self, level_0_node):
        nodes_expanded = 0

        lev_0_max = float('-inf')
        for level_1_node in level_0_node['children']:
            lev_1_min = float('inf')
            for level_2_node in level_1_node['children']:
                lev_3_max = float('-inf')
                valid = 1
                for level_3_node in level_2_node['children']:
                    nodes_expanded += 1
                    ret = self.eval_function(level_3_node['initial_board'])
                    if ret > lev_1_min:
                        valid = 0
                        break
                    if ret > lev_3_max:
                        lev_3_max = ret

                if valid:
                    level_2_node['value'] = lev_3_max
                else:
                    level_2_node['value'] = float('inf')
                if level_2_node['value'] < lev_1_min:
                    lev_1_min = level_2_node['value']

            level_1_node['value'] = lev_1_min
            if level_1_node['value'] > lev_0_max:
                lev_0_max = level_1_node['value']

        level_0_node['value'] = lev_0_max

        self.nodes_expanded_list.append(nodes_expanded)

    def return_best_move(self, level_0_node):
        # find any move that matches the best move
        best_value = level_0_node['value']
        best_children = [child for child in level_0_node['children'] if child['value'] == best_value]
        return best_children[0]['move']

    def get_all_moves(self, field):
        """
        Gets all the nodes that are available
        :param field: the game field
        :return: a list of tuples that match
        """
        output = []
        for i in range(0, 7):
            for j in range(0, 7):
                if field[i][j] == '.':
                    output.append((i, j))
        return output

    def print_nodes_expanded(self):
        print(self.name + " expansion list")
        print("-------------------------")
        for count in range(0, len(self.nodes_expanded_list)):
            print("Turn " + str(count + 1) + ": " +
                  str(self.nodes_expanded_list[count]))


# Tester for Reflex
def normal_run():
    # Initialize board
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")

    # Load Agents
    player1 = ReflexAgent('R', 'B')
    player2 = ReflexAgent('B', 'R')

    #Play
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")

    #Print Winner
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()


# Tester for 2.1
def two_one_run():
    b = Board()
    b.field[5][1] = 'R'
    b.field[1][5] = 'B'
    b.field_watcher[5][1] = 'a'
    b.field_watcher[1][5] = 'A'
    b.red_ticker = 'b'
    b.blue_ticker = 'B'
    b.turn_number = 2
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")
    player1 = ReflexAgent('R', 'B')
    player2 = ReflexAgent('B', 'R')
    while b.winner == '.':
        if b.turn_number == 5:
            print("")
        print("Turn " + str(b.turn_number))
        print("Normal------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        # print("")
        # print("Watcher-----------------------")
        # b.print_watcher()
        b.update_field()
        b.turn_number += 1
        print("")
    print("Finished! Winner is " + b.winner)
    print("Normal------------------------")
    b.print_board()
    print("")
    print("Watcher-----------------------")
    b.print_watcher()

# Part 2.2 Runs

def alphabeta_vs_minimax():
    # Initialize board
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")

    # Load Agents
    player1 = MiniMaxAgent('R', 'B', True, 'AlphaBeta')
    player2 = MiniMaxAgent('B', 'R', False, 'MiniMax')

    # Play
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")

    # Print Winner
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()

    player1.print_nodes_expanded()
    player2.print_nodes_expanded()

def minimax_vs_alphabeta():
    # Initialize board
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")

    # Load Agents
    player1 = MiniMaxAgent('R', 'B', False, 'MiniMax')
    player2 = MiniMaxAgent('B', 'R', True, 'AlphaBeta')

    # Play
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")

    # Print Winner
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()

    player1.print_nodes_expanded()
    player2.print_nodes_expanded()

def alphabeta_vs_reflex():
    # Initialize board
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")

    # Load Agents
    player1 = MiniMaxAgent('R', 'B', True, 'AlphaBeta')
    player2 = ReflexAgent('B', 'R')

    # Play
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")

    # Print Winner
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()

def reflex_vs_alphabeta():
    # Initialize board
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")

    # Load Agents
    player1 = ReflexAgent('R', 'B')
    player2 = MiniMaxAgent('B', 'R', True, 'AlphaBeta')

    # Play
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")

    # Print Winner
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()

def reflex_vs_minimax():
    # Initialize board
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")

    # Load Agents
    player1 = ReflexAgent('R', 'B')
    player2 = MiniMaxAgent('B', 'R', False, 'MiniMax')

    # Play
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")

    # Print Winner
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()

def minimax_vs_reflex_run():
    # Initialize board
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")

    # Load Agents
    player1 = MiniMaxAgent('R', 'B', False, 'MinMax')
    player2 = ReflexAgent('B', 'R')

    # Play
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")

    # Print Winner
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()

    player1.print_nodes_expanded()

# 2.4
def play_against_reflex():
    """
    This allows play against the reflex agent in a Terminal based GUI.
    Enforce that the player plays second
    :return: nothing
    """
    import os
    from time import sleep

    # Introduction:
    os.system('clear')
    print("Welcome to Gomoku!")

    # play first or second
    user_play = 'yes'
    bad_in = True
    while bad_in:
        try:
            user_play = input('Would you like to go first? (\'yes\' or \'no\'): ')
            assert user_play == 'yes' or user_play == 'no'
            bad_in = False
        except AssertionError:
            print('Please only type \'yes\' or \'no\'')

    os.system('clear')

    # load stuff
    b = Board()
    com_player = None
    user_id = '!'
    if user_play == 'no':
        com_player = ReflexAgent('R', 'B')
        print('You are playing second! You are Blue (B).')
        user_id = 'B'
    else:
        com_player = ReflexAgent('B', 'R')
        print('You are playing first! You are Red (R).')
        user_id = 'R'
    print("------------------------------")
    b.print_board()
    sleep(3)

    # Play
    while b.winner == '.':
        if user_play == 'no':
            # Let Reflex Agent Move
            os.system('clear')
            print("Gomoku")
            print("------------------------------")
            com_player.make_move(b)
            b.print_board()
            print("")
            if b.winner != '.':
                break

        # Let user input
        bad_in = True
        user_x = -420
        user_y = -420
        while bad_in:
            try:
                user_x = input('Enter enter row to place stone: ')
                user_y = input('Enter enter column to place stone: ')
                user_x = int(user_x)
                user_y = int(user_y)
                assert 0 <= user_x <= 6
                assert 0 <= user_y <= 6
                assert b.field[user_y][user_x] == '.'
                bad_in = False
            except ValueError:
                print("\nPlease input a number\n")
                user_x = -420
                user_y = -420
            except AssertionError:
                print("\nPlease input a valid number [0,6] on a slot that doesn't have a stone on it\n")
                user_x = -420
                user_y = -420

        # Run User Input
        b.field[user_y][user_x] = user_id
        b.check_winner(b.field, user_id)
        if b.check_winner(b.field, user_id):
            b.winner = user_id
            break

        # Show board with User Input
        os.system('clear')
        print("Gomoku")
        print("------------------------------")
        b.print_board()
        sleep(1)

        if user_play == 'yes':
            # Let Reflex Agent Move
            os.system('clear')
            print("Gomoku")
            print("------------------------------")
            com_player.make_move(b)
            b.print_board()
            if b.winner != '.':
                break

    # Print Winner
    os.system('clear')
    if b.winner == user_id:
        print("Finished! You Win!")
    else:
        print("Finished! Sorry, you lose!")
    print("------------------------------")
    b.print_board()

def main():
    #normal_run()
    #two_one_run()
    #play_against_reflex()

    alphabeta_vs_minimax()
    #minimax_vs_alphabeta()
    #alphabeta_vs_reflex()
    #reflex_vs_alphabeta()
    #reflex_vs_minimax()
    #minimax_vs_reflex_run()

    pass


if __name__ == "__main__":
    main()
