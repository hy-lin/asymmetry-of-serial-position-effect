graphics.off()
rm(list=ls(all=TRUE))
library(gdata)
library(gplots)
library(BayesFactor)

datafile <- "C:\\Users\\Aicey\\Documents\\GitHub\\asymmetry-of-serial-position-effect\\Experiments\\ProbedRecallNContextRetrieval\\Data Analysis\\test.txt"
Data <- read.table(datafile, header=TRUE, fill=TRUE)
summary(Data)

# test the asymmetry of item-recall-serial-position effect
summary(log(Data$ItemRecallSPAsymmetry))
bfItemSP = ttestBF(x = log(Data$ItemRecallSPAsymmetry))
summary(bfItemSP)
chains = posterior(bfItemSP, iterations = 1000)
summary(chains)
plot(chains[, 1])

# test the asymmetry of order-recall-serial-position effect
summary(log(Data$OrderRecallSPAsymmetry))
bfOrderSP = ttestBF(x = log(Data$OrderRecallSPAsymmetry))
summary(bfOrderSP)
chains = posterior(bfOrderSP, iterations = 1000)
summary(chains)
plot(chains[, 1])

# test the difference between item and order recall
summary(log(Data$ItemRecallSPAsymmetry/Data$OrderRecallSPAsymmetry))
diffScoreSP <- log(Data$ItemRecallSPAsymmetry / Data$OrderRecallSPAsymmetry)
bfSP = ttestBF(x = diffScoreSP)
summary(bfSP)
chains = posterior(bfSP, iterations = 1000)
summary(chains)
plot(chains[, 1])

###############################

# test the asymmetry of item-recall-transposition gradient
summary(log(Data$ItemRecallTransAsymmetry))
bfItemTrans = ttestBF(x = log(Data$ItemRecallTransAsymmetry))
summary(bfItemTrans)
chains = posterior(bfItemTrans, iterations = 1000)
summary(chains)
plot(chains[, 1])

# test the asymmetry of order-recall-transposition gradient
summary(log(Data$OrderRecallTransAsymmetry))
bfOrderTrans = ttestBF(x = log(Data$OrderRecallTransAsymmetry))
summary(bfOrderTrans)
chains = posterior(bfOrderTrans, iterations = 1000)
summary(chains)
plot(chains[, 1])

# test the difference between item and order recall
summary(log(Data$ItemRecallTransAsymmetry/Data$OrderRecallTransAsymmetry))
diffScoreTrans <- log(Data$ItemRecallTransAsymmetry / Data$OrderRecallTransAsymmetry)
bfTrans = ttestBF(x = diffScoreTrans)
summary(bfTrans)
chains = posterior(bfTrans, iterations = 1000)
summary(chains)
plot(chains[, 1])