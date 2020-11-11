import zmq
import pickle

from dqn.atari import AtariEnv
from dqn.cnn_model import CNNModel
from dqn.dqn_agent import DQNAgent
from dqn.protobuf.data import Data, bytes2arr


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://172.17.0.2:5000")

    env = AtariEnv('PongNoFrameskip-v4', 4)
    timesteps = 1000000

    dqn_agent = DQNAgent(
        CNNModel,
        env.get_observation_space(),
        env.get_action_space()
    )

    weight = b''
    for step in range(timesteps):

        socket.send(weight)
        weight = b''

        data = Data()
        data.ParseFromString(socket.recv())
        state, next_state = bytes2arr(data.state), bytes2arr(data.next_state)
        dqn_agent.memorize(state, data.action, data.reward, next_state, data.done)

        if step > dqn_agent.training_start:
            dqn_agent.learn()

            if step % dqn_agent.update_freq == 0:
                dqn_agent.update_target_model()
                weight = pickle.dumps(dqn_agent.get_weights())


if __name__ == '__main__':
    main()
