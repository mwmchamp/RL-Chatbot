const {TwitterAPI} = require("twitter-api-v2")

const client = new TwitterAPI({
    appKey: "HJe12HIemeSILHG18uztzTj3g",
    appSecret: "Rzi6o6ZC2fPmBr4K3QnY9qTMguPBFf7vKOBEAD1TJ7KTT4zWLw",
    accessToken: "1908547821579755521-y26HxS3zJodt2ig2uC9H4mRbsBHLjm",
    accessSecret: "tPVW7KHAWxCqTGEEDyqI4Fl1rxe00xuXOXoUdq8w6XevQ"
})

const rwClient = client.readWrite

module.exports = rwClient