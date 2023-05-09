import random
import math
class NODE():
    def __init__(self,w,b):
        self.weights = w
        self.bias = b
        
    
    def DOT(self,layer,weights):
        i = 0
        for q in zip(layer,weights):
            i+=q[0]*q[1]
        return i
    
    def OUTPUT(self,inp,act):
        return act(self.DOT(inp,self.weights)+self.bias)
    
    def COPY(self):
        return NODE(self.weights.copy(),self.bias)

    
    
class AI():
    def __init__(self,units = [],weights = []):
        self.layers = []
        self.activation_functions = []
        self.fitness = 0
        if len(weights)==0:
            for i in range(len(units)):
                if i!=0:
                    appending2 = []
                    for i2 in range(units[i][0]):
                        appending = []
                        for i3 in range(units[i-1][0]):
                            random_weight = random.uniform(-1,1)
                            appending.append(random_weight)
                        random_bias = random.uniform(-1,1)
                        appending2.append(NODE(appending,random_bias))
                    self.layers.append(appending2)
                    
                    self.activation_functions.append(units[i][1])

                else:
                    appending2 = []
                    for i2 in range(units[i][0]):
                        appending2.append(NODE([0],0))
                    self.layers.append(appending2)
                    self.activation_functions.append(0)

        else:
            for i in weights[0]:
                appending = []
                for e in i:
                    appending.append(NODE(e[0],e[1]))
                self.layers.append(appending)
            self.activation_functions = weights[1]
            
    def COPY(self):
        return AI(weights = self.GET_WEIGHTS_AND_BIASES())
    
    def MUTATE(self,M):
        for L in range(len(self.layers)):
            if L!=0:
                for N in self.layers[L]:
                    for W in range(len(N.weights)):
                        if random.uniform(0,1)<=M[0]:
                            N.weights[W] += random.gauss(0,M[2])
                    if random.uniform(0,1)<=M[1]:
                        N.bias += random.gauss(0,M[2])
        return self
    def RANDOMIZE(self):
        for L in range(len(self.layers)):
            if L!=0:
                for N in self.layers[L]:
                    for W in range(len(N.weights)):
                        N.weights[W] = random.uniform(-1,1)
                    N.bias = random.uniform(-1,1)
        return self
    def CROSSOVER(self,p):
        for L in range(len(self.layers)):
            if L!=0:
                for N in range(len(self.layers[L])):
                    if random.randint(0,1)==1:
                        self.layers[L][N] = p.layers[L][N].COPY()
        return self
                            
    def GET_WEIGHTS_AND_BIASES(self):
        ret = []
        for i in self.layers:
            appending = []
            for e in i:
                appending.append([e.COPY().weights,e.bias])
            ret.append(appending)
        return [ret,self.activation_functions.copy()]
    
    def SET_WEIGHTS_AND_BIASES(self,array):
        self.layers = array[0]
        self.activation_functions = array[1]
    def SIGMOID(self,x):
        if x>-10 and x<10:
            return 1/(1+(2.718281828459045)**(-x))
        elif x<=-10:
            return 0
        else:
            return 1
    def RELU(self,x):
        if x<0:
            return 0
        return x
    def LINEAR(self,x):
        return x
    def TANH(self,x):
        return math.tanh(x)

    def PREDICT_LAYER(self,layer,inp,act):
        output = []
        for i in range(len(self.layers[layer])):
            output.append(self.layers[layer][i].OUTPUT(inp,act))
        return output
    
    def DECODE_ACTIVATION_FUNCTION(self,x):

        if x == "SIGMOID":
            return self.SIGMOID
        elif x == "TANH":
            return self.TANH
        else:
            return self.RELU
        
    def PREDICT(self,inp):
        for i in range(len(self.layers)-1):
            if i+2!=len(self.layers):
                inp = self.PREDICT_LAYER(i+1,inp,self.DECODE_ACTIVATION_FUNCTION(self.activation_functions[i+1]))
            else:
                inp = self.PREDICT_LAYER(i+1,inp,self.DECODE_ACTIVATION_FUNCTION(self.activation_functions[i+1]))
            
        return inp
    
    def TRAIN(self,inputs,outputs,rate):
        newai = self.COPY()        
        
        for x,y in zip(inputs,outputs):
            newai.fitness = 0
            p = newai.PREDICT(x)
            for i in range(len(p)):
                newai.fitness+=(p[i]-y[i])**2
            
            
                
            
                
            
        
        
    
    
class AI_HANDLER():
    def __init__(self,population,selection,ai = 0,ailist = []):
        self.population_count = population
        self.ai_population = []
        self.selection = selection
        if ai!=0:
            for i in range(population):
                ai = ai.COPY()
                self.ai_population.append([ai,0])
        if ailist!= []:
            self.ai_population = ailist

    
    
