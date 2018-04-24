##############################
##AUTHOR: Shom Mazumder
##DATE LAST UPDATED: 04/24/2018
##PURPOSE: Clean raw data
##############################
rm(list = ls())

#### SETUP ####

# packages
library(tidyverse) #tidy functions
library(haven) #read in stata files
library(stringr) #string functions
library(stringi) #more string functions

# set working directory
setwd("~/Dropbox/ideas/lincoln-brigade/")

# read in data
df <- read_csv("01-data/raw-brigades-data.csv")

#### CLEAN DATA ####

# check data
head(df)

# get all numbers from the bio (these contain the birthyear)
#get_birthyear <- function(x){
#  numbers <- str_extract_all(x,"\\(?[0-9]+\\)?")[[1]] #get all numbers
#  potential_birthyears <- stri_sub(numbers, stri_locate_last_regex(numbers, "\\d{4}")) #potential birth years (four digits)
#  potential_birthyears <- na.omit(potential_birthyears) #remove NAs
#  estimated_birthyear <- as.numeric(potential_birthyears[1]) #estimated birth year
#  return(estimated_birthyear)
#}

get_birthyear <- function(x){
  split_bio <- str_split(x,pattern = fixed("b.")) #split the bio string
  potential_birthyear <- split_bio[[1]][2] #estimated birth year string location
  potential_birthyear <- stri_sub(potential_birthyear, stri_locate_first_regex(potential_birthyear, "\\d{4}")) #potential birth years (four digits)
  potential_birthyear <- as.numeric(potential_birthyear)
  return(potential_birthyear)
}

# apply estimated birthyear function
df$birthyr <- unlist(lapply(df$bio,get_birthyear))

# function to get first name
get_first_name <- function(x){
  split_name <- str_split(x,pattern = fixed(" "))
  first_name <- split_name[[1]][1]
  return(first_name)
}

# function to get last name
get_last_name <- function(x){
  split_name <- str_split(x,pattern = fixed(" "))
  last_name <- split_name[[1]][length(split_name[[1]])]
  return(last_name)
}

# apply name functions
df$namefrst <- unlist(lapply(df$name,get_first_name)) #get first name
df$namelast <- unlist(lapply(df$name,get_last_name)) #get last name

# function to estimate state of residence
get_state <- function(x){
  strings_with_states <- sapply(state.name, grepl, x=strsplit(x, ";")[[1]])
  if(!is.null(ncol(strings_with_states))){
    potential_states <- colSums(strings_with_states > 0)
    estimated_states <- names(which(potential_states > 0))
  }else{
    potential_states <- which(strings_with_states == T)
    estimated_states <- names(potential_states)
  }
  return(estimated_states[1])
}

df$statename <- unlist(lapply(df$bio,get_state)) #get state of residence

#output csv
write_csv(x = df,path = "01-data/cleaned-brigades-data.csv")

