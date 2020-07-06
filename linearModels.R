library(MASS)
actions <- read.csv("~/Documents/GitHub/DecisionTimes/SVO Context Analysis/actions.csv")

for (r in c(10,20,30,40,50,60,70,80,90,100)) {
  x = subset(actions, treatment == "fix", select = c(paste0("score", r), "score100")) 
  model = lm(score100 ~ ., x)
  print(summary(model)$adj.r.squared)
}

for (r in c(10,20,30,40,50,60,70,80,90,100)) {
  x = subset(actions, treatment == "weak", select = c(paste0("score_adj", r), "score_adj")) 
  model = lm(score_adj ~ ., x)
  print(summary(model)$adj.r.squared)
}

x = subset(actions, treatment == "fix", select = c("score20", "score30", "score"))
model = lm(score ~ ., x)
#step = stepAIC(model, direction = "both")
summary(model)

x = subset(actions, treatment == "fix", select = c("score_adj10", "score_adj20", "score_adj30", "score_adj40", "score_adj50", "score_adj"))
model = lm(score_adj ~ ., x)
step = stepAIC(model, direction = "forward")
summary(model)

x = subset(actions, treatment == "weak", select = c("score_adj10", "score_adj20", "score_adj30", "score_adj40", "score_adj50", "score_adj"))
model = lm(score_adj ~ ., x)
#step = stepAIC(model, direction = "both")
summary(model)

variables = c("score10","score20","score30","score40","score50")
variables_adj = c("score_adj10","score_adj20","score_adj30","score_adj40","score_adj50")

vars = c()
rs = c()
for (r in c(1:5)) {
  vars = c(vars, variables_adj[r])
  x = subset(actions, treatment == "weak", select = c(vars, "score_adj"))
  model = lm(score_adj ~ ., x)
  rs = c(rs, summary(model)$adj.r.squared)
}


x = subset(actions, treatment == "changing", select = c("score_adj10", "score_adj20", "score_adj30", "score_adj40", "score_adj50", "score_adj"))

model = lm(score_adj ~ ., x)
summary(model)

x = subset(actions, treatment == "changing", select = c("score10", "score20", "score30", "score40", "score"))

model = lm(score ~ ., x)
summary(model)
