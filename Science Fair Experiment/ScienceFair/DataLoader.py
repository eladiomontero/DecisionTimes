import os
import pandas as pd
import re

class DataLoader:
    DATAURL = "../data"
    def loadSessionsData(self):
        experimentData = pd.DataFrame()
        userInformation = pd.DataFrame()
        for f in os.listdir(self.DATAURL):
            answersFiles = []
            usersInfoFiles = []
            if f.startswith("."): continue
            answersFiles = self.loadInfoFromFile("%s/%s/data/" % (self.DATAURL, f), "history")
            usersInfoFiles = self.loadInfoFromFile("%s/%s/data/" % (self.DATAURL, f), "answers")
            experimentData = experimentData.append(self.getAnswersFromFiles( "%s/%s/data/" % (self.DATAURL, f), f, answersFiles))
            userInformation = userInformation.append(self.getInfoUsers("%s/%s/data/" % (self.DATAURL, f), f, usersInfoFiles))
        experimentData = self.formatExperimentData(experimentData)
        experimentData.to_csv("./output/experimentData.csv")
        userInformation.to_csv("./output/userInformation.csv")
        return experimentData, userInformation

    def loadInfoFromFile(self, sessionFolder, fileType):
        files = []
        for dpath, name, fileNames in os.walk(sessionFolder):
            for f in fileNames:
                if str(f).endswith(fileType):
                    files.append(f)
        return files


    def getAnswersFromFiles(self, path ,session, answerFiles):
        formattedAnswers = pd.DataFrame()
        for a in answerFiles:
            user, _ = str(a).split("history")
            answers = pd.read_csv("%s/%s" % (path, a), " ")
            answers["user"] = user
            answers["session"] = session
            answers["subj_id"] = "%s%s" % (user, session)
            formattedAnswers = formattedAnswers.append(answers)
        return formattedAnswers

    def getInfoUsers(self, path, session, userInfoFiles):
        infoUsers = pd.DataFrame()
        age = 0
        gender = ""
        user = ""
        for u in userInfoFiles:
            user, _ = str(u).split("answers")
            with open("%s/%s" % (path, u)) as f:
                ageBool = False
                genderBool = False
                for line in f:
                    if ageBool:
                        age = self.cleanAge(line.strip())
                        ageBool = False
                    elif genderBool:
                        gender = line.strip()
                        genderBool = False
                    if "gender" in line:
                        genderBool = True
                    elif "Age" in line:
                        ageBool = True
            infoUsers = infoUsers.append({"user": user, "age":age, "gender":gender, "session": session, "subj_id": "%s%s" % (user, session)}, ignore_index=True)
        return infoUsers

    def cleanAge(self, ageString):
        if len(ageString) == 0:
            return ""
        else:
            return re.findall("\d+", ageString)[0]

    def formatExperimentData(self, data, subjects=False):
        #data = data[data["who_played"] == "user"]
        del data["Score"], data["Time_php[ms]"], data["PlayedBy"]
        data.rename(columns={'Time_js[ms]': 'rt', "Move": "response", "Round": "round"}, inplace=True)
        data['rt'] = data.rt.astype(int)
        data.loc[data['response'] == "C", "response"] = 1.0
        data.loc[data['response'] == "D", "response"] = 0.0
        data["rt"] = data["rt"] / 1000
        #data = hddm.utils.flip_errors(data)
        if subjects:
            data.rename(columns={"subj_id": "subj_idx"}, inplace=True)
        return data


dl = DataLoader()
#experiment, users = dl.loadSessionsData()
#print (users)
