const rwClient = require("./twitterClient.js");

const tweet = async () => {
    try {
        await rwClient.v1.tweet("bruh")
    } catch (e) {
        console.error(e)
    }
}

tweet()