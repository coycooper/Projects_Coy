# 1. U.S. Exports of Goods by State

# 1.0. Setup

setwd("F:/乔治梅森大学/2015 fall/STAT-515/Final_Presentation/final project/Linked MicromapSt(1. 画单图)");
source("theme_clean.r");
library(ggplot2);
library(maps);

# 1.1. Get map coordinates for the conterminous U.S. states and make a map using 
#      an Albers projection 

stateMap <- map_data("state")
colnames(stateMap)
head(stateMap)
is.data.frame(stateMap) # TRUE

ggplot(stateMap,aes(x=long,y=lat,group=group))+
  geom_polygon(fill=rgb(.8,1,.8),
               color="black")+coord_map("albers",29.5,45.5)

# 1.2. A export data set for U.S. states

exports_states <- read.table("clipboard",sep='\t',header=T);exports_states$Total
rownames(exports_states) <- exports_states$State
exports_states$State <- tolower(rownames(exports_states))
exports_states

exports_states_map <- merge(stateMap, exports_states, by.x="region",by.y="State")
head(exports_states_map)
colnames(exports_states_map)

library(plyr)
exports_states_map <- arrange(exports_states_map, group, order) 
head(exports_states_map)

# 1.3. Defining export classes

head(exports_states)

TotalExportQuints<- quantile(exports_states$Total,seq(0,1,by=.2))
exports_states$TotalClass = cut(exports_states$Total,
                                TotalExportQuints,include.lowest=TRUE)
ExportsColors <- colorRampPalette(
  c(rgb(0,.6,0),gray(.95),'purple'))(5)

# 1.4. Finally we produce the plot and clean up the background 

library(grid);
ggplot(exports_states,aes(map_id = State,fill=TotalClass))+
  geom_map(map=exports_states_map, color=gray(0),size=.3)+ 
  scale_fill_manual(values=ExportsColors)+
  expand_limits(x=stateMap$long,y=stateMap$lat)+
  coord_map("albers",29.5,45.5)+
  labs(fill="Total Export Rate",title="U.S. Exports of Goods by State")+
  theme_clean()

# 2. U.S. Imports of Goods by State

# 2.0. Setup

setwd("F:/乔治梅森大学/2015 fall/STAT-515/Final_Presentation/final project/Linked MicromapSt(1. 画单图)");
source("theme_clean.r");
library(ggplot2);
library(maps);

# 2.1. Get map coordinates for the conterminous U.S. states and make a map using 
#      an Albers projecton 

stateMap <- map_data("state")
colnames(stateMap)
head(stateMap)
is.data.frame(stateMap) # TRUE

ggplot(stateMap,aes(x=long,y=lat,group=group))+
  geom_polygon(fill=rgb(.8,1,.8),
               color="black")+coord_map("albers",29.5,45.5)

# 2.2. A Imports data set for U.S. states

imports_states <- read.table("clipboard",sep='\t',header=T);imports_states$Total
rownames(imports_states) <- imports_states$State
imports_states$State <- tolower(rownames(imports_states))
imports_states

imports_states_map <- merge(stateMap, imports_states, by.x="region",by.y="State")
head(imports_states_map)

library(plyr)
imports_states_map <- arrange(imports_states_map, group, order) 
head(imports_states_map)

# 2.3. Defining import classes

head(imports_states)

TotalImportQuints<- quantile(imports_states$Total,seq(0,1,by=.2))
imports_states$TotalClass = cut(imports_states$Total,
                                TotalImportQuints,include.lowest=TRUE)
ImportsColors <- colorRampPalette(
  c(rgb(0,.6,0),gray(.95),'purple'))(5)

# 2.4. Finally we produce the plot and clean up the background 

library(grid)
ggplot(imports_states,aes(map_id = State,fill=TotalClass))+
  geom_map(map=imports_states_map, color=gray(0),size=.3)+ 
  scale_fill_manual(values=ImportsColors)+
  expand_limits(x=stateMap$long,y=stateMap$lat)+
  coord_map("albers",29.5,45.5)+
  labs(fill="Total Imports Rate",title="U.S. Imports of Goods by State")+
  theme_clean()

# 3. micromapST_Combination Data

# 3.0. Setup

library(micromapST)

# 3.1. The micromapST package has a stateNamesFips data.frame That has official 
#      states names as row names. (The District of Columbia name has been shorted 
#      to "D.C.")

stateNamesFips

# 3.2. Defining a data preparation function

micromapSTprep <- function(stateDF,stateId=NULL,ref=stateNamesFips)
  {
  if (is.null(stateId)) 
    nam <- row.names(stateDF) 
  else
    nam <- stateDF[,stateId]
  nam <- ifelse(nam=="District of Columbia","D.C.",nam)
  check <-  match(nam,row.names(ref)) 
  bad <- is.na(check)
  good <- !bad
  nbad <- sum(bad)
  if (nbad>0)
    {
    warning(paste(nbad,"Unmatch Names Removed",nam[bad])) 
    stateDF <- stateDF[!bad,]
    nam <- nam[!bad]
    check <- check[!bad]
    good <- good[!bad]
    }
  ngood <- sum(good)
  if (ngood < 51)
    warning(paste("Only",ngood,"State Ids"))
  row.names(stateDF) <- ref[check,2]
  return(stateDF)
}

# 3.3. Reading and preparing a state data.frame

setwd("F:/乔治梅森大学/2015 fall/STAT-515/Final_Presentation/final project/MicromapSt(2.Combination)");
combination <- read.table("clipboard",sep="\t",header=TRUE,as.is=TRUE)
head(combination)
ImportsMinusExports <- micromapSTprep(combination,"State")
head(ImportsMinusExports)

# 3.4. A quick look at micromapST dot plots
# 3.4.1. Making a panel description data.frame

colNumbers <- 1:ncol(ImportsMinusExports)
names(colNumbers)=colnames(ImportsMinusExports)
colNumbers

panelDesc <- data.frame(
  type=c('map','id','dot','dot','dot'),
  lab1=rep("",5),
  lab2=c('','','Exports','Imports','Imports-Exports'),
  lab3=c('','','Possible 0-500,000','Possible 0-500,000',''),
  col1=c(NA,NA,"Exports","Imports",12))

t(panelDesc)

# 3.4.2. The micromapST() function

pdf("Combination.pdf",width=7.5,height=10)
micromapST(ImportsMinusExports, panelDesc,sortVar=12,ascend=FALSE,
           title=c("Combination of Exports and Imports","Imports - Exports"))
dev.off()

# 3.5. Cumulative maps, arrows, reference values and two variable transformations 

ImportsMinusExports$Zero <- rep(0,nrow(ImportsMinusExports))
panelDesc <- data.frame(
  type=c('mapcum','id','arrow','arrow'),
  lab1=c('','','Exports To','0 To'),
  lab2=c('' ,'','Imports','Imports-Exports'),
  col1 = c(NA,NA,4,13),
  col2 = c(NA,NA,9,12),
  refVals=c(NA,NA,NA,0))
pdf("Combination Arrows.pdf",
    width=7.5,height=10)
micromapST(ImportsMinusExports,panelDesc,
           sortVar=12,ascend=FALSE,
           title=c("Combination of Exports And Imports","Imports - Exports"))
dev.off()

# 3.6. Maptail and Dots with confidence Intervals

panelDesc <- data.frame(
  type=c('maptail','id','dotconf','dotconf'),
  lab1=c('','','Exports Estimates ','Imports Estimates'),
  lab2=c('' ,'','and 95% CIs','and 95% CIs'),
  col1 = c(NA,NA,4,9),
  col2 = c(NA,NA,5,10),
  col3 = c(NA,NA,6,11))

png(file="Combination of Exports and Imports DotConf.png",
    width=7,height=10,
    units="in",res=300)
micromapST(ImportsMinusExports, panelDesc,
           sortVar=12,ascend=FALSE,
           title=c("Combination of Exports and Imports","Imports - Exports"))
dev.off()

# 4 time series

data<- read.table("clipboard",header=TRUE)
data
library(ggplot2)
colnames(data)
ggplot(data = data)+
  geom_line(aes(x=Month,y=Exports,colour =as.character(Year)))+
  geom_point(aes(x=Month,y=Exports),data = data)