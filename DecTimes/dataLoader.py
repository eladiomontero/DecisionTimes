import hddm


class dataLoader():


    def parse_files(self, files_to_parse):
        o = open("output_data.dat", "w")
        for index, i in enumerate(files_to_parse):
            if index == 0:
                for line in open("raw data/history_" + i + ".dat"):
                    o.write(line.replace(" ", ",").replace("usuario", i + "_usuario"))
            else:
                f = open("raw data/history_" + i + ".dat")
                f.readline()
                for line in f:
                    o.write(line.replace(" ", ",").replace("usuario", i + "_usuario"))
        o.close()
        data = hddm.load_csv('output_data.dat')
        return data

    def formatData(self, data, subjects=False):
        data = data[data["who_played"] == "user"]
        del data["who_played"], data["opponent"], data["payoff"], data["time_php"], data["action_opponent"]
        data.rename(columns={'time_js': 'rt', "action_player": "response"}, inplace=True)
        data['rt'] = data.rt.astype(int)
        data.loc[data['response'] == "C", "response"] = 1.0
        data.loc[data['response'] == "D", "response"] = 0.0
        data["rt"] = data["rt"] / 1000
        data = hddm.utils.flip_errors(data)
        session = data["player"].str.split("_", n=1, expand=True)
        data["session"] = session[0]
        data["treatment"] = ""
        data.loc[data["session"].isin(['s1m5', 's2m5', 's4m8', 's8n3', 's9n3', 's10n5']), 'treatment'] = "fix"
        data.loc[data["session"].isin(['s5m20', 's6m22', 's7m22', 's11n9', 's12n11', 's13n12']), 'treatment'] = "changing"
        data.loc[data["session"].isin(['s3m7']), 'treatment'] = "weak"
        if subjects:
            data.rename(columns={"player": "subj_idx"}, inplace=True)
        return data