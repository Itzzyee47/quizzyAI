import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from dotenv import load_dotenv
import requests

from dbFuctions import extract_quiz_json

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


# Create the model
generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-8b",
  generation_config=generation_config,
  system_instruction="You are an AI assistant tasked with analyzing course materials. Given a course module, perform the following tasks:\n\nSummarize the key points of the module in 2-3 concise paragraphs.\nCreate a 5-question multiple-choice quiz based on the module's content. Each question must have 4 options, with only one correct answer.\nFormat and return the quiz as a JSON object in the following structure: {\n    \"quiz\": [\n        {\n            \"question\": \"What is AI?\",\n            \"options\": [\"Option 1\", \"Option 2\", \"Option 3\", \"Option 4\"],\n            \"answer\": \"Option 1\"\n        },\n        {\n            \"question\": \"Define ML.\",\n            \"options\": [\"Option 1\", \"Option 2\", \"Option 3\", \"Option 4\"],\n            \"answer\": \"Option 1\"\n        }\n    ]\n}",
  tools = [
    genai.protos.Tool(
      function_declarations = [
        genai.protos.FunctionDeclaration(
          name = "generateQuiz",
          description = "Generates quiz questions and answers from given notes",
          parameters = content.Schema(
            type = content.Type.OBJECT,
            properties = {
              "notes": content.Schema(
                type = content.Type.STRING,
                description = "The course notes from which to generate quiz questions.",
              ),
            },
          ),
        ),
      ],
    ),
  ],
  tool_config={'function_calling_config':'ANY'},
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "generate me a quiz for these notes:\nWhat is a neural network?\nLast Updated : 03 Jan, 2024\nNeural Networks are computational models that mimic the complex functions of the human brain. The neural networks consist of interconnected nodes or neurons that process and learn from data, enabling tasks such as pattern recognition and decision making in machine learning. The article explores more about neural networks, their working, architecture and more.\n\nTable of Content\n\nEvolution of Neural Networks\nWhat are Neural Networks?\nHow does Neural Networks work?\nLearning of a Neural Network\nTypes of Neural Networks\nSimple Implementation of a Neural Network\nEvolution of Neural Networks\nSince the 1940s, there have been a number of noteworthy advancements in the field of neural networks:\n\n1940s-1950s: Early Concepts\nNeural networks began with the introduction of the first mathematical model of artificial neurons by McCulloch and Pitts. But computational constraints made progress difficult.\n1960s-1970s: Perceptrons\nThis era is defined by the work of Rosenblatt on perceptrons. Perceptrons are single-layer networks whose applicability was limited to issues that could be solved linearly separately.\n1980s: Backpropagation and Connectionism\nMulti-layer network training was made possible by Rumelhart, Hinton, and Williams’ invention of the backpropagation method. With its emphasis on learning through interconnected nodes, connectionism gained appeal.\n1990s: Boom and Winter\nWith applications in image identification, finance, and other fields, neural networks saw a boom. Neural network research did, however, experience a “winter” due to exorbitant computational costs and inflated expectations.\n2000s: Resurgence and Deep Learning\nLarger datasets, innovative structures, and enhanced processing capability spurred a comeback. Deep learning has shown amazing effectiveness in a number of disciplines by utilizing numerous layers.\n2010s-Present: Deep Learning Dominance\nConvolutional neural networks (CNNs) and recurrent neural networks (RNNs), two deep learning architectures, dominated machine learning. Their power was demonstrated by innovations in gaming, picture recognition, and natural language processing.\nWhat are Neural Networks?\nNeural networks extract identifying features from data, lacking pre-programmed understanding. Network components include neurons, connections, weights, biases, propagation functions, and a learning rule. Neurons receive inputs, governed by thresholds and activation functions. Connections involve weights and biases regulating information transfer. Learning, adjusting weights and biases, occurs in three stages: input computation, output generation, and iterative refinement enhancing the network’s proficiency in diverse tasks.\n\nThese include:\n\nThe neural network is simulated by a new environment.\nThen the free parameters of the neural network are changed as a result of this simulation.\nThe neural network then responds in a new way to the environment because of the changes in its free parameters.\nnn-Geeksforgeeks\n\n\n\n\nImportance of Neural Networks\nThe ability of neural networks to identify patterns, solve intricate puzzles, and adjust to changing surroundings is essential. Their capacity to learn from data has far-reaching effects, ranging from revolutionizing technology like natural language processing and self-driving automobiles to automating decision-making processes and increasing efficiency in numerous industries. The development of artificial intelligence is largely dependent on neural networks, which also drive innovation and influence the direction of technology.\n\nHow does Neural Networks work?\nLet’s understand with an example of how a neural network works:\n\nConsider a neural network for email classification. The input layer takes features like email content, sender information, and subject. These inputs, multiplied by adjusted weights, pass through hidden layers. The network, through training, learns to recognize patterns indicating whether an email is spam or not. The output layer, with a binary activation function, predicts whether the email is spam (1) or not (0). As the network iteratively refines its weights through backpropagation, it becomes adept at distinguishing between spam and legitimate emails, showcasing the practicality of neural networks in real-world applications like email filtering.\n\nWorking of a Neural Network\nNeural networks are complex systems that mimic some features of the functioning of the human brain. It is composed of an input layer, one or more hidden layers, and an output layer made up of layers of artificial neurons that are coupled. The two stages of the basic process are called backpropagation and forward propagation.\n\nnn-ar-Geeksforgeeks\n\n\n\n\nForward Propagation\nInput Layer: Each feature in the input layer is represented by a node on the network, which receives input data.\nWeights and Connections: The weight of each neuronal connection indicates how strong the connection is. Throughout training, these weights are changed.\nHidden Layers: Each hidden layer neuron processes inputs by multiplying them by weights, adding them up, and then passing them through an activation function. By doing this, non-linearity is introduced, enabling the network to recognize intricate patterns.\nOutput: The final result is produced by repeating the process until the output layer is reached.\nBackpropagation\nLoss Calculation: The network’s output is evaluated against the real goal values, and a loss function is used to compute the difference. For a regression problem, the Mean Squared Error (MSE) is commonly used as the cost function.\nLoss Function:MSE = \\frac{1}{n} \\Sigma^{n}_{i=1} (y_{i} - \\hat y_{i})^2  \nGradient Descent: Gradient descent is then used by the network to reduce the loss. To lower the inaccuracy, weights are changed based on the derivative of the loss with respect to each weight.\nAdjusting weights: The weights are adjusted at each connection by applying this iterative process, or backpropagation, backward across the network.\nTraining: During training with different data samples, the entire process of forward propagation, loss calculation, and backpropagation is done iteratively, enabling the network to adapt and learn patterns from the data.\nActvation Functions: Model non-linearity is introduced by activation functions like the rectified linear unit (ReLU) or sigmoid. Their decision on whether to “fire” a neuron is based on the whole weighted input.\nLearning of a Neural Network\n1. Learning with supervised learning\nIn supervised learning, the neural network is guided by a teacher who has access to both input-output pairs. The network creates outputs based on inputs without taking into account the surroundings. By comparing these outputs to the teacher-known desired outputs, an error signal is generated. In order to reduce errors, the network’s parameters are changed iteratively and stop when performance is at an acceptable level.\n\n2. Learning with Unsupervised learning\nEquivalent output variables are absent in unsupervised learning. Its main goal is to comprehend incoming data’s (X) underlying structure. No instructor is present to offer advice. Modeling data patterns and relationships is the intended outcome instead. Words like regression and classification are related to supervised learning, whereas unsupervised learning is associated with clustering and association.\n\n3. Learning with Reinforcement Learning\nThrough interaction with the environment and feedback in the form of rewards or penalties, the network gains knowledge. Finding a policy or strategy that optimizes cumulative rewards over time is the goal for the network. This kind is frequently utilized in gaming and decision-making applications.\n\nTypes of Neural Networks\nThere are seven types of neural networks that can be used.\n\nFeedforward Neteworks: A feedforward neural network is a simple artificial neural network architecture in which data moves from input to output in a single direction. It has input, hidden, and output layers; feedback loops are absent. Its straightforward architecture makes it appropriate for a number of applications, such as regression and pattern recognition.\nMultilayer Perceptron (MLP): MLP is a type of feedforward neural network with three or more layers, including an input layer, one or more hidden layers, and an output layer. It uses nonlinear activation functions.\nConvolutional Neural Network (CNN): A Convolutional Neural Network (CNN) is a specialized artificial neural network designed for image processing. It employs convolutional layers to automatically learn hierarchical features from input images, enabling effective image recognition and classification. CNNs have revolutionized computer vision and are pivotal in tasks like object detection and image analysis.\nRecurrent Neural Network (RNN): An artificial neural network type intended for sequential data processing is called a Recurrent Neural Network (RNN). It is appropriate for applications where contextual dependencies are critical, such as time series prediction and natural language processing, since it makes use of feedback loops, which enable information to survive within the network.\nLong Short-Term Memory (LSTM): LSTM is a type of RNN that is designed to overcome the vanishing gradient problem in training RNNs. It uses memory cells and gates to selectively read, write, and erase information.\nSimple Implementation of a Neural Network\n \nimport numpy as np\n \n# array of any amount of numbers. n = m\nX = np.array([[1, 2, 3],\n              [3, 4, 1],\n              [2, 5, 3]])\n \n# multiplication\ny = np.array([[.5, .3, .2]])\n \n# transpose of y\ny = y.T\n \n# sigma value\nsigm = 2\n \n# find the delta\ndelt = np.random.random((3, 3)) - 1\n \nfor j in range(100):\n   \n    # find matrix 1. 100 layers.\n    m1 = (y - (1/(1 + np.exp(-(np.dot((1/(1 + np.exp(\n        -(np.dot(X, sigm))))), delt))))))*((1/(\n            1 + np.exp(-(np.dot((1/(1 + np.exp(\n                -(np.dot(X, sigm))))), delt)))))*(1-(1/(\n                    1 + np.exp(-(np.dot((1/(1 + np.exp(\n                        -(np.dot(X, sigm))))), delt)))))))\n \n    # find matrix 2\n    m2 = m1.dot(delt.T) * ((1/(1 + np.exp(-(np.dot(X, sigm)))))\n                           * (1-(1/(1 + np.exp(-(np.dot(X, sigm)))))))\n    # find delta\n    delt = delt + (1/(1 + np.exp(-(np.dot(X, sigm))))).T.dot(m1)\n \n    # find sigma\n    sigm = sigm + (X.T.dot(m2))\n \n# print output from the matrix\nprint(1/(1 + np.exp(-(np.dot(X, sigm)))))\nOutput:\n\n[[0.99999325 0.99999375 0.99999352]\n [0.99999988 0.99999989 0.99999988]\n [1.         1.         1.        ]]\n\nAdvantages of Neural Networks\nNeural networks are widely used in many different applications because of their many benefits:\n\nAdaptability: Neural networks are useful for activities where the link between inputs and outputs is complex or not well defined because they can adapt to new situations and learn from data.\nPattern Recognition: Their proficiency in pattern recognition renders them efficacious in tasks like as audio and image identification, natural language processing, and other intricate data patterns.\nParallel Processing: Because neural networks are capable of parallel processing by nature, they can process numerous jobs at once, which speeds up and improves the efficiency of computations.\nNon-Linearity: Neural networks are able to model and comprehend complicated relationships in data by virtue of the non-linear activation functions found in neurons, which overcome the drawbacks of linear models.\nDisadvantages of Neural Networks\nNeural networks, while powerful, are not without drawbacks and difficulties:\n\nComputational Intensity: Large neural network training can be a laborious and computationally demanding process that demands a lot of computing power.\nBlack box Nature: As “black box” models, neural networks pose a problem in important applications since it is difficult to understand how they make decisions.\nOverfitting: Overfitting is a phenomenon in which neural networks commit training material to memory rather than identifying patterns in the data. Although regularization approaches help to alleviate this, the problem still exists.\nNeed for Large datasets: For efficient training, neural networks frequently need sizable, labeled datasets; otherwise, their performance may suffer from incomplete or skewed data.",
      ],
    },
    {
      "role": "model",
      "parts": [
        " questions = [\n        {\n            \"question\": \"What are neural networks?\",\n            \"options\": [\"Computational models mimicking human brain functions\", \"Simple linear equations\", \"Software programs for data analysis\", \"Hardware components for processing data\"],\n            \"answer\": \"Computational models mimicking human brain functions\"\n        },\n        {\n            \"question\": \"What is the primary function of a hidden layer in a neural network?\",\n            \"options\": [\"To receive input data\", \"To produce the final output\", \"To process input and introduce non-linearity\", \"To connect input to output\"],\n            \"answer\": \"To process input and introduce non-linearity\"\n        },\n         {\n            \"question\": \"What is backpropagation?\",\n            \"options\": [\"Forward movement of data in a neural network\", \"A method for adjusting weights in a neural network\", \"A type of activation function\", \"A type of neural network\"],\n            \"answer\": \"A method for adjusting weights in a neural network\"\n        },\n        {\n            \"question\": \"What is a common activation function in neural networks?\",\n            \"options\": [\"Linear function\", \"Exponential function\", \"Rectified Linear Unit (ReLU)\", \"Trigonometric function\"],\n            \"answer\": \"Rectified Linear Unit (ReLU)\"\n        },\n         {\n            \"question\": \"What is a major advantage of neural networks?\",\n            \"options\": [\"Ease of training with small datasets\", \"Ability to process only linear data\", \"Inability to adapt to new situations\", \"Ability to identify patterns and adapt to changing environments\"],\n            \"answer\": \"Ability to identify patterns and adapt to changing environments\"\n        }\n    ]\n\n ",
      ],
    },
  ]
)



response = chat_session.send_message(f'Generate me a quiz ')

# Print out each of the function calls requested from this single call.
# Note that the function calls are not executed. You need to manually execute the function calls.
# For more see: https://github.com/google-gemini/cookbook/blob/main/quickstarts/
# Function_calling.ipynb
print('getting respods')
for part in response.parts:
  if fn := part.function_call:
    args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
    print(f"{fn.name}")
    #print(response.parts[0].text)
    payload = dict(message=f"Generate me a 5-question multiple-choice quiz based on the sumarized module's content of highest importance. Each question must have 4 options, with only one correct answer. Heres the module notes , return only the questions and options in a json format i can easily read with code.")
    r = requests.post('https://genzylla.onrender.com/getResponds', data=payload)
    print(f"The responds data type is: {type(r.text)}")
    res = r.json()
    #print(res['answer'])
    print(extract_quiz_json(res['answer']))
    break