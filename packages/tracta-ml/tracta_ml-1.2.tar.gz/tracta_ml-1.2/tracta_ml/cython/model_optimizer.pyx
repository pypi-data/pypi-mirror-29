from tracta_ml.evolve import model_tuner
from datetime import datetime
import pickle
from dispout import sol_disp, graph_disp

class ModelTuner:

    def __init__(self, model, param_dict, cv, score):
        self.mod = model
        self.param_dict = param_dict
        self.cv = cv
        self.score = score

    def fit(self, X, y, verbose=False, max_back=0.5, tot_gen=2000, known_best=None):
        '''optimizing hyper-params and features for the given model'''

        sol_disp("Starting optimization")
        t1 = datetime.now()
        self.best_sol, self.monitor = model_tuner(X, y, self.mod, self.param_dict,\
                                                  self.cv, self.score, verbose,\
                                                  look_back=int(max_back*tot_gen), n_gen=tot_gen,\
                                                  known_best=known_best)
        t2 = datetime.now()
        sol_disp(str("Time taken : ")+str(t2 - t1))

        sol_disp(str("\n")+str("Best Model Stats: \n")+str(self.best_sol))

        up_param_dict = dict(zip(self.param_dict.keys(), self.best_sol.hpGene))
        self.mod.set_params(**up_param_dict)
        X_trans = X.loc[:,(self.best_sol.featGene==1)]

        pickle.dump(list(X_trans.columns.values), open('best_features.pkl', 'wb'))
        pickle.dump(self.mod, open('best_model.pkl', 'wb'))
        pickle.dump(self.best_sol, open('best_solution.pkl', 'wb'))
        sol_disp(str("\n")+str("Best model & feature set saved to disk"))

        return self


    def load_file(self, file):
        return pickle.load(open(file,'rb'))


    def get_best_model(self):
        return self.mod


    def transform(self,X):
        return X.loc[:,(self.best_sol.featGene==1)]


    def get_features(self):
        return self.best_sol.featGene == 1


    def plot_monitor(self,metric):
        graph_disp(self, metric)
        return














