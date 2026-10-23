import pysd

# Load your Vensim model
model = pysd.read_vensim('New EPI Aedes Months.mdl')

# Run with default parameters
results = model.run()
print(results)

##Run code below in terminal to translate the model to Python
#python -m pysd --translate ('New EPI Aedes Months.mdl')
