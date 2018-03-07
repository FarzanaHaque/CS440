#(column, row)
#(i, j)


class Board:
    field = []
    turn_number = 1
    winner = '.'

    def __init__(self):
        for i in range(0, 7):
            self.field.append([0, 0, 0, 0, 0, 0, 0])
            for j in range(0, 7):
                self.field[i][j] = '.'

    def print_board(self):
        print("  0 1 2 3 4 5 6")
        for i in range(0, 7):
            print(str(i) + " ", end="")
            for j in range(0, 7):
                print(str(self.field[i][j]) + " ", end="")
            print("")

    def get_all_nodes(self, cid):
        output = []
        for i in range(0, 7):
            for j in range(0, 7):
                if self.field[i][j] == cid:
                    output.append((i, j))
        return output

    def check_full(self):
        full = True
        for i in range(0, 7):
            for j in range(0, 7):
                if self.field[i][j] == '.':
                    full = False
        if full:
            self.winner = "&"

        return full

    def check_winner(self):
        pass

class ReflexAgent:
    mid = ''
    oid = ''

    def __init__(self, ID, oID):
        self.mid = ID
        self.oid = oID

    def get_my_stones(self, b, cid):
        my_stones = []
        for i in range(0, 7):
            for j in range(0, 7):
                if b.field[i][j] == cid:
                    my_stones.append((i, j))
        return my_stones

    def instant_win(self, b, cid):
        # Note: this does not check for a "R R . R R" win condition. Might need too
        my_stones = self.get_my_stones(b, cid)
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
                    return best

            # check down
            found_best = True
            for count in range(1, 3 + 1):
                cand = (s[0] + count, s[1])
                if cand not in my_stones or s[0] + count > 6:
                    found_best = False
                    break
            if found_best:
                best = (s[0] + 4, s[1])
                if s[0] + 4 <= 6 and b.field[best[0]][best[1]] == ".":
                    return best

            # check left
            found_best = True
            for count in range(1, 3 + 1):
                cand = (s[0], s[1] - count)
                if cand not in my_stones or s[1] - count < 0:
                    found_best = False
                    break
            if found_best:
                best = (s[0], s[1] - 4)
                if s[1] - 4 >= 0 and b.field[best[0]][best[1]] == ".":
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
                    return best

        return -420, -420

    def find_triple_chain_empty(self, b, cid):
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
                if s[0] + 1 <= 6 and s[0] - 3 >= 0 and b.field[head1[0]][head1[1]] == "." and b.field[head2[0]][head2[1]] == ".":
                    # normal case not at beginning or end
                    return head1, head2
                elif s[0] == 6 and b.field[head2[0]][head2[1]] == ".":
                    # at very bottom, top can be valid
                    return head2, head1

            #check down
            found_best = True
            for count in range(1, 2 + 1):
                cand = (s[0] + count, s[1])
                if cand not in my_stones or s[0] + count > 6:
                    found_best = False
                    break
            if found_best:
                head1 = (s[0] - 1, s[1])
                head2 = (s[0] + 3, s[1])
                if s[0] - 1 >= 0 and s[0] + 3 <= 6 and b.field[head1[0]][head1[1]] == "." and b.field[head2[0]][head2[1]] == ".":
                    return head2, head1
                elif s[0] == 0 and b.field[head2[0]][head2[1]] == ".":
                    return head2, head1

            #check left
            found_best = True
            for count in range(1, 2 + 1):
                cand = (s[0], s[1] - count)
                if cand not in my_stones or s[1] - count < 0:
                    found_best = False
                    break
            if found_best:
                head1 = (s[0], s[1] + 1)
                head2 = (s[0], s[1] - 3)
                if s[1] + 1 <= 6 and s[1] - 3 >= 0 and b.field[head1[0]][head1[1]] == "." and b.field[head2[0]][head2[1]] == ".":
                    return head1, head2
                elif s[1] == 6 and b.field[head2[0]][head2[1]] == ".":
                    return head2, head1

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
                if s[1] - 1 >= 0 and s[1] + 3 <= 6 and b.field[head1[0]][head1[1]] == "." and b.field[head2[0]][head2[1]] == ".":
                    return head2, head1
                elif s[1] == 0 and b.field[head2[0]][head2[1]] == ".":
                    return head2, head1
        return -420, -420

    def find_all_win_segs(self, b, oid):
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

        return win_segs

    def win_seg_move(self, b, mid, oid):
        win_segs = self.find_all_win_segs(b, oid)
        win_seg_count = {}

        if len(win_segs) == 0:
            # catch if no more winning segments, just play down left most valid
            all_empty = b.get_all_nodes('.')
            leftmost = min(all_empty, key=lambda t: t[1])
            leftmostvalues = [y for y in all_empty if y[1] == leftmost[1]]
            downleftmost = max(leftmostvalues, key=lambda t: t[0])
            return downleftmost

        for ws in win_segs:
            score = 0
            for t in ws:
                if b.field[t[0]][t[1]] == mid:
                    score += 1
            win_seg_count[tuple(ws)] = score

        best_score = max(win_seg_count.values())
        win_seg_best = [y for y in win_seg_count.keys() if win_seg_count[y] == best_score]
        leftmost = min(win_seg_best, key=lambda t: t[1])[0]
        leftmostvalues = [y for y in win_seg_best if y[0][1] == leftmost[1]]
        downleftmost = max(leftmostvalues, key=lambda t: t[0])

        # leftdownmostplace = ()
        # for count in downleftmost:
        #     if b.field[t[0]][t[1]] == mid:
        #         leftdownmostplace = t

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
        return downleftmost[0]


        print("Error: win_seg_move has found a win seg that has no valid places")
        return -420, -420

    def make_move(self, b):
        if b.check_full():
            return

        if b.turn_number == 1:
            pass # can add a random later here for strategies
        # Part 1
        best_move = self.instant_win(b, self.mid)
        if best_move != (-420, -420):
            b.field[best_move[0]][best_move[1]] = self.mid
            b.winner = self.mid
            return

        # Part 2
        best_move = self.instant_win(b, self.oid)
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

def normal_run():
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")
    player1 = ReflexAgent('R', 'B')
    player2 = ReflexAgent('B', 'R')
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()

def two_one_run():
    b = Board()
    b.field[1][1] = 'R'
    b.field[5][5] = 'B'
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
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()

def main():
    two_one_run()


if __name__ == "__main__":
    main()
