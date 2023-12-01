install.packages("reticulate")
library(reticulate)

setwd("/Users/MinHo/Downloads")
pd <- import("pandas")
data <- pd$read_pickle("movie_with_var (1).pkl")
dim(data)
head(data)
colnames(data)

data1 <- data[,-c(3,4,11,12,16,17,68)]
head(data1)
colnames(data1)
attach(data1)

# numerical
index <- which(revenue>0)
budget <- as.numeric(budget[index])
popularity <- as.numeric(popularity[index])
runtime <- as.numeric(runtime[index])
vote_average <- as.numeric(vote_average[index])
vote_count <- as.numeric(vote_count[index])
dates <- as.numeric(dates[index])
revenue <- as.numeric(revenue[index])

length(runtime)

# categorical
original_language <- as.factor(original_language)
production_countries <- as.factor(production_countries)
num_genres <- as.factor(num_genres)
all_genres <- as.factor(all_genres)
num_languages <- as.factor(num_languages)
collection <- as.factor(collection)
has_homepage <- as.factor(has_homepage)
release_month <- as.factor(release_month[index])

hist(budget)
hist(log10(budget))
hist(log10(revenue))
hist(log10(popularity))
hist(runtime)
hist(log10(vote_count))
hist(dates)

plot(log10(budget),log10(revenue),pch=20,col=4)
plot(log10(vote_count),log10(revenue),pch=20,col=4)
plot(popularity,log10(revenue),pch=20,col=4)

round(cor(cbind(budget,vote_count,revenue)),3)

pairs(~budget+popularity+vote_count+runtime+dates+revenue,pch=20,col=4)
round(cor(cbind(budget,popularity,vote_count,runtime,dates,revenue)),3)

table(num_genres)
table(original_language)
table(release_month)

release_month <- as.factor(as.numeric(release_month))
boxplot(revenue ~ release_month)
boxplot(log10(revenue) ~ release_month)

Drama <- 1-genre_Drama[index]
barplot(table(Drama,release_month),col=c(4,0))
legend("topleft",c("Drama","Others"),fill=c(4,0))

genre <- matrix(NA,12,11)
for(i in 1:12){
  genre[i,] <- colSums(data1[release_month==i,14:24])
}

th_ho <- apply(genre[,c(3,8)],1,sum)
barplot(rbind(th_ho,table(release_month)-th_ho),col=c(4,0),
        main="Proportion of Thiller & Horror", xlab="month", ylab="number of movies")
legend("topleft",c("Thiller & Horror","Non Thiller & Horror"),fill=c(4,0))
prop <- as.numeric(round(th_ho/table(release_month),2))
text((0.6:11.6)*1.2,20,prop,cex=0.7)


dr_fa <- apply(genre[,c(1,11)],1,sum)
barplot(rbind(dr_fa,table(release_month)-dr_fa),col=c(4,0),
        main="Proportion of Drama & Family", xlab="month", ylab="number of movies")
legend("topleft",c("Drama & Family","Non Drama & Family"),fill=c(4,0))
prop <- as.numeric(round(dr_fa/table(release_month),2))
text((0.6:11.6)*1.2,20,prop,cex=0.7)

library("stringr")
year <- as.numeric(str_sub(data1$release_date[index], 1, 4))
min(year)
max(year)
hist(year)
year <- year*10

boxplot(log10(budget) ~ year)
plot(year,log10(revenue))

cor(year,revenue)

data$original_title[year<1920]
