#Import Document and Make Changes
setwd("/Users/redpal/Desktop/data_science/overwatch_project/")
train_df = read.csv("norm/damage_train.csv", header = TRUE)
str(train_df)
colnames(train_df)

#Get Test Features
test_df = read.csv("norm/damage_test.csv", header = TRUE)
test_feat = test_df[,-1]
test_ans = test_df[,1]

#Use a Simple Linear Model
out = lm(rating ~ .,data=train_df)
summary(out)

#Get Some Basic Plots
plot(fitted(out),rstudent(out), main = "Simple LM's fitted values versus residual values", 
     xlab = "Fitted Values", ylab="Residual Values")
abline(h=0,col="red")

#QQ-plot
qqnorm(rstudent(out))
qqline(rstudent(out))

#Get Cook's Distance
plot(train_df$rating,cooks.distance(out))

#Preform an Prediction
n = nrow(test_feat)
linearPred = predict(out1,test_feat)
Z_log = (linearPred - test_ans)^2
lower = mean(Z_log)-1.96*sd(Z_log)/sqrt(n)
upper = mean(Z_log)+1.96*sd(Z_log)/sqrt(n)
mean(Z_log)
lower
upper

#Now Do Variable Elimination
library(glmnet)
Y = train_df[,1]
X = data.matrix(train_df[,-1])

#For Cross-Validation
grid = seq(-6,2,length=500)
grid = 10^grid

#Get Out
out = cv.glmnet(X, Y, alpha = 1, lambda = grid)
plot(out)

#Get Lambda Points
out$lambda.min
out$lambda.1se 

#Get OG Plots
fit = glmnet(X,Y,alpha = 1)
plot(fit,xvar="lambda")
abline(v=out$lambda.1se, col="black")

#Now do New Plots
fit = glmnet(X,Y,alpha = 1, lambda = out$lambda.min)
plot(fit$beta,type="h")

#Get Co-efficients
coef(out,s="lambda.1se")

#Alt_X
n = nrow(test_feat)
X_new = as.matrix(test_feat)
ans = predict(fit,X_new)
Z_lasso = (linearPred - test_ans)^2
lower = mean(Z_lasso)-1.96*sd(Z_lasso)/sqrt(n)
upper = mean(Z_lasso)+1.96*sd(Z_lasso)/sqrt(n)
mean(Z_lasso)
lower
upper

#Ranger
library(ranger)
forestOut = ranger(x=X,y=Y)

#Print Forest
names(forestOut)
forestOut$r.squared

#Preform Prediction
n = nrow(test_feat)
rf_pred = predict(forestOut,data=test_feat)
Z_rf = (rf_pred$predictions - test_ans)^2
lower_rf = mean(Z_rf)-1.96*sd(Z_rf)/sqrt(n)
upper_rf = mean(Z_rf)+1.96*sd(Z_rf)/sqrt(n)
mean(Z_rf)
lower_rf
upper_rf

#Do Additive Model
library(mgcv)
func = s(ashe_timePlayed)

#Get Game Formula
use = colnames(train_df)
form<-as.formula(
  paste0("rating ~",paste0("s(",use,")",collapse="+"),collapse=""))

#Do the Modeling
gamOut = gam(form, data = train_df)
gm_pred = predict(gamOut,data=test_feat)
Z_gm = (gm_pred - test_ans)^2
lower_gm = mean(Z_gm)-1.96*sd(Z_gm)/sqrt(n)
upper_gm = mean(Z_gm)+1.96*sd(Z_gm)/sqrt(n)
mean(Z_gm)
lower_gm
upper_gm
