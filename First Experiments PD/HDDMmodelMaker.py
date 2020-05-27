import hddm
import numpy as np
import matplotlib as plt
from scipy import stats

class HDDMmodelMaker():

    def fit_model(self, data, size, burn):
        model = hddm.HDDM(data, bias = True)
        #model.find_starting_values()
        model.sample(size, burn = burn)
        return model
    
    def gen_synthetic_data(a,v,z,t0,subj_idx,rounds = 10000):
        sim = pd.DataFrame()
        dec_times = [0] * subjects
        responses = [0] * subjects
        for r in range(rounds):
            N = 100000
            s = z * a  # deliberation status
            D = 1 #Difusion constant
            for i in range(N):
                rand = np.random.normal()
                if (s < a) and s > 0:
                    s = s - v * t0 + D ** .5 * np.random.randn() * t0**0.5
                    #dt = dt + 1
                else:
                    if s > 0:
                        responses[r] = 1
                    dec_times[r] = t0 * i
                    break
            if dec_times[r] == 0.0:
                raise Exception("Not enough steps to reach a decision")
        dic = {"sub_idx": subj_idx,"rt": dec_times, 'response': responses, "round": [r] * rounds}
        sim_times = pd.DataFrame(dic)
        if r == 0:
            sim = sim_times
        else:
            sim = sim.append(sim_times, ignore_index = True)

    def get_stats(self, model, subjects = False):
        stats_df = model.gen_stats()
        stats_df.index.name = 'parameter'
        stats_df.reset_index(inplace=True)
        if subjects:
            new = stats_df["parameter"].str.split("_subj.", n = 1, expand = True)
            stats_df["param"]= new[0]
            stats_df["subject"]= new[1]
            stats_df.drop(columns =["parameter"], inplace = True)
        return stats_df

    def plot_params(self, stats_df, title):
        parameters = ["a", "v", "z", "t"]
        fig, axs = plt.subplots(4, 4)
        fig.set_size_inches(13, 13)
        fig.suptitle('Correlation plots with Pearson coefficient, %s, (subjects model)' % (title), fontsize=16)
        i = 0
        j = 0
        for p2 in parameters:
            j = 0
            for p in parameters:
                x = stats_df.loc[stats_df.param == p, "mean"]
                y = stats_df.loc[stats_df.param == p2, "mean"]
                axs[i, j].scatter(x, y)
                axs[i, j].set_title("Corr: %f, p value: %s" % (
                np.round(stats.pearsonr(x, y)[0], 2), np.round(stats.pearsonr(x, y)[1], 4)))
                j = j + 1
            i = i + 1

        axs.flat[0].set(ylabel='a')
        axs.flat[4].set(ylabel='v')
        axs.flat[8].set(ylabel='z')
        axs.flat[12].set(ylabel='t')
        axs.flat[12].set(xlabel='a')
        axs.flat[13].set(xlabel='v')
        axs.flat[14].set(xlabel='z')
        axs.flat[15].set(xlabel='t')

