from gym_zelda_1 import Zelda1Env
import tqdm


env = Zelda1Env()
done = True


try:
    for _ in tqdm.tqdm(range(5000)):
        if done:
            state = env.reset()
            done = False
        else:
            state, reward, done, info = env.step(env.action_space.sample())
except KeyboardInterrupt:
    pass
