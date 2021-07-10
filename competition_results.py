from result import Result


class CompetitionResults:
    def __init__(self, hill, date, competitors):
        self.hill = hill
        self.date = date
        self.competitors = competitors
        self.results = [Result(jumper) for jumper in competitors]
        self.sorted_results = []

    def sort_results(self):
        self.sorted_results = self.results[:]
        self.sorted_results.sort()
        self.sorted_results.reverse()
        self.sorted_results[0].rank = 1
        for i, res in enumerate(self.sorted_results[:-1]):
            self.sorted_results[i+1].rank = self.sorted_results[i].rank
            if self.sorted_results[i+1].total_points < self.sorted_results[i].total_points:
                self.sorted_results[i+1].rank = i+2

    def ordered_results(self):
        for result in self.sorted_results:
            yield result

    def add_jump_result(self, ind, jmp):
        self.results[ind].add_jump(jmp)


if __name__ == '__main__':
    pass
