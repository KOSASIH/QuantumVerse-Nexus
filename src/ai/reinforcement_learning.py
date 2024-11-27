import numpy as np
import random

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.99, min_exploration_rate=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.q_table = np.zeros((state_size, action_size))

    def choose_action(self, state):
        """Choose an action based on the exploration-exploitation trade-off."""
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_size - 1)  # Explore
        else:
            return np.argmax(self.q_table[state])  # Exploit

    def learn(self, state, action, reward, next_state):
        """Update the Q-table based on the action taken and the reward received."""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

    def update_exploration_rate(self):
        """Decay the exploration rate over time."""
        if self.exploration_rate > self.min_exploration_rate:
            self.exploration_rate *= self.exploration_decay

class Environment:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

    def reset(self):
        """Reset the environment to an initial state."""
        return random.randint(0, self.state_size - 1)  # Random initial state

    def step(self, state, action):
        """Take an action in the environment and return the next state and reward."""
        # Example transition logic (to be customized based on the specific environment)
        next_state = (state + action) % self.state_size  # Simple state transition
        reward = 1 if next_state == 0 else -1  # Reward structure
        return next_state, reward

# Example usage
if __name__ == "__main__":
    state_size = 10  # Number of states
    action_size = 2  # Number of actions (e.g., 0: do nothing, 1: take action)
    episodes = 1000  # Number of training episodes

    env = Environment(state_size, action_size)
    agent = QLearningAgent(state_size, action_size)

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            action = agent.choose_action(state)
            next_state, reward = env.step(state, action)
            agent.learn(state, action, reward, next_state)
            state = next_state

            if next_state == 0:  # Define a condition to end the episode
                done = True

        agent.update_exploration_rate()

    print("Training completed.")
    print("Q-Table:\n", agent.q_table)
