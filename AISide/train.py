from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from tenkaichi_env import TenkaichiEnv

def main():
    # Create the custom environment
    env = TenkaichiEnv()
    
    # Create the PPO agent
    agent = PPO("MlpPolicy", env, verbose=1)

    # Train the agent for multiple episodes
    num_episodes = 5
    max_steps_per_episode = 1000
    total_timesteps = 0
    for episode in range(num_episodes):
        episode_reward = 0
        obs, _ = env.reset()
        for step in range(max_steps_per_episode):
            action, _ = agent.predict(obs, deterministic=False)
            obs, reward, done, _, info = env.step(action)
            episode_reward += reward
            total_timesteps += 1
            print("Step:", step, "Reward:", reward, "Done:", done)
            if done or step == max_steps_per_episode - 1:
                break

        # Print the episode reward after each episode
        print(f"Episode {episode + 1}/{num_episodes}, Reward: {episode_reward}")

        # Learn from the collected experiences after each episode
        agent.learn(total_timesteps=total_timesteps)

    # Save the trained model
    model_path = "custom_env_model"
    agent.save(model_path)

    # Evaluate the agent
    mean_reward, _ = evaluate_policy(agent, env, n_eval_episodes=num_episodes)
    print(f"Mean reward over {num_episodes} evaluation episodes: {mean_reward}")

if __name__ == "__main__":
    main()