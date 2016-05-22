graphics.off()
rm(list=ls(all=TRUE))
library(gdata)
library(gplots)
?sleep


datafile <- "C:\\Users\\Aicey\\Documents\\GitHub\\asymmetry-of-serial-position-effect\\Experiments\\ProbedRecallNContextRetrieval\\Data Analysis\\test.txt"
Data <- read.table(datafile, header=TRUE, fill=TRUE)
summary(Data)

diffScoreSP <- Data$ItemRecallSPAsymmetry - Data$OrderRecallSPAsymmetry
summary(diffScoreSP)
bfSP = ttestBF(x = diffScoreSP)
bfSP
1/bfSP


diffScoreTrans <- log(Data$ItemRecallTransAsymmetry / Data$OrderRecallTransAsymmetry)
summary(diffScoreTrans)
bfTrans = ttestBF(x = diffScoreTrans)
bfTrans
chains = posterior(bfTrans, iterations = 1000)
summary(chains)
plot(chains[, 1:2])

# log transform
logItemRecallTrans <- log(Data$ItemRecallTransAsymmetry)
summary(logItemRecallTrans)
bfLogItemTrans = ttestBF(x = logItemRecallTrans)
bfLogItemTrans
chains = posterior(bfLogItemTrans, iteration = 1000)
summary(chains)
plot(chains[,1:2])
