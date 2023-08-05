from simglucose.controller.base import Action
import matplotlib.pyplot as plt
import logging
import matplotlib.dates as mdates
from datetime import timedelta
import time
import os

pathos = True
try:
    from pathos.multiprocessing import ProcessPool as Pool
except ImportError:
    print('You could install pathos to enable parallel simulation.')
    pathos = False

logger = logging.getLogger(__name__)


class SimObj(object):
    def __init__(self,
                 env,
                 controller,
                 sim_time,
                 animate=True,
                 path=None):
        self.env = env
        self.controller = controller
        self.sim_time = sim_time
        self.animate = animate
        self._ctrller_kwargs = None
        self.path = path

    def simulate(self):
        # basal = self.env.patient._params.u2ss * self.env.patient._params.BW / 6000
        # action = Action(basal=basal, bolus=0)
        obs, reward, done, info = self.env.reset()
        tic = time.time()
        while self.env.time < self.env.scenario.start_time + self.sim_time:
            if self.animate:
                self.env.render()
            action = self.controller.policy(obs, reward, done, **info)
            obs, reward, done, info = self.env.step(action)
        toc = time.time()
        logger.info('Simulation took {} seconds.'.format(toc - tic))

    def results(self):
        return self.env.show_history()

    def save_results(self):
        df = self.results()
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        filename = os.path.join(self.path, str(self.env.patient.name) + '.csv')
        df.to_csv(filename)

    def reset(self):
        self.env.reset()
        self.controller.reset()


def sim(sim_object):
    print("Process ID: {}".format(os.getpid()))
    print('Simulation starts ...')
    sim_object.simulate()
    sim_object.save_results()
    print('Simulation Completed!')
    return sim_object.results()


def batch_sim(sim_instances, parallel=False):
    tic = time.time()
    if parallel and pathos:
        with Pool() as p:
            results = p.map(sim, sim_instances)
    else:
        if parallel and not pathos:
            print('Simulation is using single process even though parallel=True.')
        results = [sim(s) for s in sim_instances]
    toc = time.time()
    print('Simulation took {} sec.'.format(toc - tic))
    return results


if __name__ == '__main__':
    from simglucose.simulation.env import T1DSimEnv
    from simglucose.controller.basal_bolus_ctrller import BBController
    from simglucose.sensor.cgm import CGMSensor
    from simglucose.actuator.pump import InsulinPump
    from simglucose.patient.t1dpatient import T1DPatient
    from simglucose.simulation.scenario_gen import RandomScenario

    path = './results'

    patient1 = T1DPatient.withName('adolescent#001')
    sensor1 = CGMSensor.withName('Dexcom', seed=1)
    pump1 = InsulinPump.withName('Insulet')
    scenario1 = RandomScenario(seed=1)
    env1 = T1DSimEnv(patient1, sensor1, pump1, scenario1)
    controller1 = BBController()

    s1 = SimObj(env1, controller1, sim_time=timedelta(days=1), path=path)
    s1.animate = False
    # s1.animate = True
    # s1.set_controller_kwargs(patient_name=patient1.name,
    #                          sample_time=s1.env.sample_time)

    # s1.simulate()

    patient2 = T1DPatient.withName('adolescent#002')
    sensor2 = CGMSensor.withName('Dexcom', seed=1)
    pump2 = InsulinPump.withName('Insulet')
    scenario2 = RandomScenario(seed=1)
    env2 = T1DSimEnv(patient2, sensor2, pump2, scenario2)
    controller2 = BBController()

    s2 = SimObj(env2, controller2, sim_time=timedelta(days=1), path=path)
    # s2.set_controller_kwargs(patient_name=patient2.name,
    #                          sample_time=s2.env.sample_time)
    s2.animate = False

    sim_objects = [s1, s2]

    nodes = 2
    p = Pool(nodes=nodes)
    tic = time.time()
    results = p.map(sim, sim_objects)
    toc = time.time()
    print('{} workers took {} sec.'.format(nodes, toc - tic))
    print(results)

    # with Pool(processes=nodes) as p:
    #     tic = time.time()
    #     p.map(sim, sim_objects)
    #     toc = time.time()
    #     print('{} workers took {} sec.'.format(nodes, toc - tic))

    # tic = time.time()
    # map(simulation, sim_objects)
    # toc = time.time()
    # print('Serial took {} sec.'.format(toc - tic))

    # for s in sim_objects:
    #     s.simulate()
    # processes = [Process(target=simulation, args=(s,)) for s in sim_objects]
    # for p in processes:
    #     p.start()
    #     p.join()

    # # for p in processes:
    # #     p.join()

    # # for s in sim_objects:
    # #     p = Process(target=s.simulate, args=())
    # #     p.start()

    # with Pool(processes=2) as pool:
    #     # pool.map(simulation, sim_objects)
    #     res = [pool.apply_async(simulation, (s,)) for s in sim_objects]
    #     # res = pool.apply_async(simulation, ())
    #     # print(res.get())

    #     for r in res:
    #         print(r.get())
