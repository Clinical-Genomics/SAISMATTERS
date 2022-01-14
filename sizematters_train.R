#!/usr/bin/env Rscript
#Rscript sizematters_train.R <input_csv> <output_prefix> <min_correlation>
library(neuralnet)

args = commandArgs(trailingOnly=TRUE)
if (length(args)<3) {
  stop("Rscript sizematters_train.R <input_csv> <output_prefix> <min_correlation>.n", call.=FALSE)
} 

input_csv=args[1]
output_prefix=args[2]
min_correlation=as.numeric(args[3])

size_matters_analysis <- read.csv(input_csv)
df = subset(size_matters_analysis, select = -c(Sample,FFY) )

m="FFY~"
columns=c()
for (i in colnames(df)){
  if (sd(unlist(df[i])) == 0){
    next}
  c=cor(size_matters_analysis$FFY,df[i])
  if (abs(c) > min_correlation){

    m=paste(m,i,sep=" +")
    columns=c(columns,i)
  }
  
}

model=neuralnet(as.formula(m), size_matters_analysis, hidden = 2, stepmax = 1e10)
save('model', 'columns', file = paste0(output_prefix, '.model.RData'))

#dfsub = subset(size_matters_analysis, select = columns)
#hopp=as.matrix(dfsub)
#prediction = as.numeric(predict(model, dfsub))
#cor(size_matters_analysis$FFY,prediction)
#dfp <- data.frame(prediction,size_matters_analysis$FFY)



