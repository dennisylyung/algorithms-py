from typing import Tuple, Iterable


class Scheduler:
    """
    A greedy scheduler that schedule jobs with specific weight and length with greedy algorithms.
    The objective function is weighted sum of completion time.
    """

    def __init__(self, jobs: Iterable[Tuple[float, float]] = None):
        """
        Initialize a scheduler with optional jobs.
        An empty scheduler is created by default.
        An optional iterable of jobs can also be provided to initialize a scheduler with jobs loaded.
        :param jobs: Jobs represented by tuples of (weight, length)
        """
        self.jobs = list(jobs) if jobs else []

    def register(self, job: Tuple[float, float]) -> None:
        """
        Register a job to the scheduler
        :param job: The job represented by tuples of (weight, length)
        :return: None
        """
        self.jobs.append(job)

    def schedule(self, method='ratio') -> float:
        """
        Schedule the registered jobs using a greedy algorithm.
        Two algorithms are currently supported:
            Ratio: Score jobs by weight / length. Guaranteed to find optimal solution.
            Difference: Score jobs by weight - length. May find non-optimal solution
        :param method: The algorithm to use. One of {"ratio", "difference"}. Defaults to "ratio"
        :return: the scheduling cost (weighted sum of completion time)
        """

        # implement specific methods
        if method == 'ratio':
            def score(job):
                weight, length = job
                return weight / length

            sort_desc = True
        elif method == 'difference':
            def score(job):
                weight, length = job
                return weight - length + weight * 1.e-10  # add a small weight for ties

            sort_desc = True
        else:
            raise ValueError(f'method {method} is not supported. supported are ["ratio", "difference"]')

        scheduled = sorted(self.jobs, key=score, reverse=sort_desc)

        weighted_completion_time = 0
        current_time = 0
        for job in scheduled:
            weight, length = job
            current_time += length
            weighted_completion_time += weight * current_time

        return weighted_completion_time

    def __len__(self):
        return len(self.jobs)


if __name__ == '__main__':

    with open('data/scheduling.txt') as f:
        lines = f.readlines()

    num_jobs = int(lines[0])
    scheduler = Scheduler()

    for line in lines[1:]:
        if not line:
            continue
        weight, length = tuple(line.split(' ', 2))
        scheduler.register((int(weight), int(length)))

    assert len(scheduler) == num_jobs

    print('Weighted Completion Time')
    wct = scheduler.schedule(method='difference')
    print(f'difference cost: {wct}')
    wct = scheduler.schedule(method='ratio')
    print(f'ratio cost: {wct}')
