library(mongolite)
library(lubridate)

# connect to MongoDB

m <- mongo(collection="in_cycle",db="cando",url = "mongodb://localhost")

# start and end time of interest
# this is easiest to just specify by day as the start and the next day as the end
start_time <- "2021-01-01T00:00:00Z"
end_time <- "2022-03-20T00:00:00Z"

all_cycles <- m$find(paste0('{"date_time":{
              "$gte": { "$date" : "', start_time, '" }, 
              "$lte": { "$date" : "', end_time, '" }}}'))
