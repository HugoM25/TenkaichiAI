from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from customenv import CustomEnv 


# Create the custom environment
env = CustomEnv()

# Create the PPO agent
agent = PPO("MlpPolicy", env, verbose=1)

# Train the agent for more episodes
total_timesteps = 50000
agent.learn(total_timesteps=total_timesteps)

# Save the trained model
model_path = "custom_env_model"
agent.save(model_path)

# Evaluate the agent
mean_reward, _ = evaluate_policy(agent, env, n_eval_episodes=10)
print(f"Mean reward over 10 evaluation episodes: {mean_reward}")