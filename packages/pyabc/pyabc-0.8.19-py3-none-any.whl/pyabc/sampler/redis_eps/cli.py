import sys
import socket
import signal
from redis import StrictRedis
import pickle
import os
import cloudpickle
from time import time
import click
from .redis_logging import worker_logger
from .cmd import (N_WORKER, SSA, N_PARTICLES, N_EVAL, QUEUE, START, STOP,
                  MSG)
from multiprocessing import Pool
import numpy as np
import random


TIMES = {"s": 1,
         "m": 60,
         "h": 3600,
         "d":  24*3600}


def runtime_parse(s):
    unit = TIMES[s[-1].lower()]
    nr = float(s[:-1])
    return unit * nr


class KillHandler:
    def __init__(self):
        self.killed = False
        self.exit = True
        signal.signal(signal.SIGTERM, self.handle)
        signal.signal(signal.SIGINT, self.handle)

    def handle(self, *args):
        self.killed = True
        if self.exit:
            sys.exit(0)


def work_on_population(redis: StrictRedis, start_time: int,
                       max_runtime_s: int,
                       kill_handler: KillHandler):
    population_start_time = time()
    cumulative_simulation_time = 0

    ssa = redis.get(SSA)
    if ssa is None:
        return
    sample, simulate, accept = pickle.loads(ssa)
    kill_handler.exit = False

    n_particles_bytes = redis.get(N_PARTICLES)
    if n_particles_bytes is None:
        return
    n_particles = int(n_particles_bytes.decode())

    n_worker = redis.incr(N_WORKER)
    worker_logger.info("Begin population. I am worker {}"
                       .format(n_worker))
    internal_counter = 0
    while n_particles > 0:
        if kill_handler.killed:
            worker_logger.info("Worker {} received stop signal. "
                               "Terminating in the middle of a population"
                               " after {} samples."
                               .format(n_worker, internal_counter))
            redis.decr(N_WORKER)
            sys.exit(0)

        current_runtime = time() - start_time
        if current_runtime > max_runtime_s:
            worker_logger.info("Worker {} stops during population because "
                               "max runtime {} is exceeded {}"
                               .format(n_worker, max_runtime_s,
                                       current_runtime))
            redis.decr(N_WORKER)
            return

        particle_id = redis.incr(N_EVAL)
        internal_counter += 1

        this_sim_start = time()
        new_param = sample()
        new_sim = simulate(new_param)
        cumulative_simulation_time += time() - this_sim_start

        if accept(new_sim):
            n_particles = redis.decr(N_PARTICLES)
            redis.rpush(QUEUE, cloudpickle.dumps((particle_id, new_sim)))
        else:
            n_particles = int(redis.get(N_PARTICLES).decode())

    redis.decr(N_WORKER)
    kill_handler.exit = True
    population_total_time = time() - population_start_time
    worker_logger.info(f"Finished population, did {internal_counter} samples. "
                       f"Simulation time: {cumulative_simulation_time:.2f}s, "
                       f" total time {population_total_time:.2f}.")


@click.command(help="Evaluation parallel redis sampler for pyABC.")
@click.option('--host', default="localhost", help='Redis host.')
@click.option('--port', default=6379, type=int, help='Redis port.')
@click.option('--runtime', type=str, default="2h",
              help='Max worker runtime if the form <NR><UNIT>, '
                   'where <NR> is any number and <UNIT> can be s, '
                   '(S,) m, (M,) '
                   'h, (H,) d, (D) for seconds, minutes, hours and days. '
                   'E.g. for 12 hours you would pass --runtime=12h, for half '
                   'a day you could do 0.5d.')
@click.option('--processes', type=int, default=1, help="The number of worker "
                                                       "processes to start")
def work(host="localhost", port=6379, runtime="2h", processes=1):
    # start a single process right here, not within pool
    # this handles the problem of starting a daemon process within a
    # daemon process
    if processes == 1:
        return _work(host, port, runtime)

    with Pool(processes) as pool:
        res = pool.starmap(_work, [(host, port, runtime)] * processes)
    return res


def _work(host="localhost", port=6379, runtime="2h"):
    np.random.seed()
    random.seed()

    kill_handler = KillHandler()

    start_time = time()
    max_runtime_s = runtime_parse(runtime)
    worker_logger.info(f"Start redis worker. Max run time {max_runtime_s}s, "
                       f"HOST={socket.gethostname()}, PID={os.getpid()}")
    redis = StrictRedis(host=host, port=port)

    p = redis.pubsub()
    p.subscribe(MSG)
    listener = p.listen()
    for msg in listener:
        # check if it is int to run at least once
        try:
            data = msg["data"].decode()
        except AttributeError:
            data = msg["data"]

        if data == START or isinstance(data, int):
            work_on_population(redis, start_time, max_runtime_s, kill_handler)

        if data == STOP:
            worker_logger.info("Received stop signal. Shutdown redis worker.")
            return

        elapsed_time = time() - start_time
        if elapsed_time > max_runtime_s:
            worker_logger.info("Shutdown redis worker. Max runtime {}s reached"
                               .format(max_runtime_s))
            return


@click.command(help="ABC Redis cluster manager. "
                    "The command can be 'info' or 'stop'. "
                    "For 'stop' the workers are shut down cleanly "
                    "after the current population. "
                    "For 'info' you'll see how many workers are connected, "
                    "how many evaluations the current population has, and "
                    "how many particles are still missing. "
                    "For 'reset-workers', the worker count will be resetted to"
                    "zero. This does not cancel the sampling. This is useful "
                    "if workers were unexpectedly killed.")
@click.option('--host', default="localhost", help='Redis host.')
@click.option('--port', default=6379, type=int, help='Redis port.')
@click.argument('command', type=str)
def manage(command, host="localhost", port=6379):
    return _manage(command, host=host, port=port)


def _manage(command, host="localhost", port=6379):
    redis = StrictRedis(host=host, port=port)
    if command == "info":
        pipe = redis.pipeline()
        pipe.get(N_WORKER)
        pipe.get(N_EVAL)
        pipe.get(N_PARTICLES)
        res = pipe.execute()
        res = [r.decode() if r is not None else r for r in res]
        print("Workers={} Evaluations={} Particles={}".format(*res))
    elif command == "stop":
        redis.publish(MSG, STOP)
    elif command == "reset-workers":
        redis.set(N_WORKER, 0)
    else:
        print("Unknown command:", command)
