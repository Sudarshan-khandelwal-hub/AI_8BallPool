# AI_8BallPool

### Execute all of the following commands from the root directory of the DQN folder:

## (Optional) Establish and enable a virtual environment
- To create a virtual environment, run the command:
- <code> virtualenv .venv </code>

- Then, activate the virtual environment by running:
- <code> source .venv/bin/activate </code>

## (Optional) Establish and enable a virtual environment Using Anaconda 
- To create an environment:
- <code> conda create --name <my-env> </code>

Replace <my-env> with the name of your environment.
- When conda asks you to proceed, type y:
- proceed ([y]/n)?

This creates the myenv environment in /envs/. No packages will be installed in this environment.
- To create an environment with a specific version of Python:
- <code> conda create -n myenv python=3.8.19 </code>

- To create an environment with a specific package:
- <code> conda create -n myenv Pool </code>

Please review the contents of the requirements.txt file to ensure that all necessary prerequisites have been met before proceeding with the execution. Alternatively, you can install the package: To install the required packages listed in the "requirements.txt" file, use the following command in the Python terminal:

<code> python -m pip install -r requirements.txt </code>

## Execute game:
<code> python -m src.game.main </code>
Initiate the training process. The value of the variable ALGO is 'dqn'. The variable BALLS should have a value of 2 or more. The option to show the training epochs is optional.

the environment look like this:

https://github.com/Sudarshan-khandelwal-hub/AI_8BallPool/assets/68321559/735ea7ef-58f4-4b9f-8aeb-b5c8afd114a8

## The command:
<code> python -m src.model.train [--balls  No. of Balls] [--algo ALGO] --visualize output_model </code>

Example: python -m src.model.train --balls 8 --algo dqn output_model

python -m src.model. is used to run a Python module named "model" located in the "src" package.Train [--balls BALLS] The user is specifying the algorithm to be used, using the command [--algo ALGO]. [--visualize] output_model

## Conduct the evaluation. 
The value of ALGO is dqn. BALLS refers to 2 or more balls. MODEL represents the name of the output_model that was used. --The "visualize" option is available for seeing testing results. Periods of time, often used in the context of historical or geological eras.

To execute the evaluation module of the model, run the following command in the terminal: 

<code> python -m src.model.eval </code> 
The user can provide the model by using the [--model MODEL] option. [--balls BALLS] The user is specifying the algorithm to be used, denoted as "ALGO". [--display]


## Visualizing Average training rewards

- Display the mean rewards for each epoch - Execute the following command in the terminal:
  
  <code> python -m src.utils.training_rewards_dqn_vis dqn-log.txt OUTPUT_FILE` </code>

Test rewards and training loss are automatically visualized at the end of test and training epochs, respectively. It is necessary to store the locally created plots.

## References
https://github.com/nkatz565/CS229-pool
