var party1_tags;
var party2_tags;
var party1_sentiment;
var party2_sentiment;
var party1_gender;
var party2_gender;

var dataMapping = {

}
function setState(p1pos, p1neg, p1neu, p2pos, p2neg, p2neu, p1tags, p2tags, p1g, p2g, p1c, p2c, p1, p2) {
    party1_tags = p1tags;
    party2_tags = p2tags;
    party1_sentiment = [p1pos, p1neg, p1neu]
    party2_sentiment = [p2pos, p2neg, p2neu]
    party1_gender = p1g;
    party2_gender = p2g;
    party1_count = p1c;
    party2_count = p2c;
    dataMapping[p1] = {"t":party1_tags, "s":party1_sentiment, "g":party1_gender, "c": party1_count};
    dataMapping[p2] = {"t":party2_tags, "s":party2_sentiment, "g":party2_gender, "c": party2_count};
}

function changeData(p, change, revert) {
    current = document.getElementById(revert);
    update = document.getElementById(change);
    current.className = "";
    update.className = "card-menu-item active";
    tags = dataMapping[p].t
    sentiment = dataMapping[p].s
    gender = dataMapping[p].g
    count = dataMapping[p].c
    amPieChart("u-tw-sentiment", sentiment[0], sentiment[1], sentiment[2]);

    var tagDiv = document.getElementById("u-tag-content")
    var tagHTML = "";
    var splitTags = tags.split(" ");
    for(var i=0; i<splitTags.length; i++) {
        var link = "/wordcloud/?q=" + splitTags[i];
        var href = "<a href='" + link + "' style='color:#4D5A85;'>#" + splitTags[i] + "</a><br>"
        tagHTML += href;
    }
    tagDiv.innerHTML = tagHTML;
    var postCount = document.getElementById("u-pc");
    postCount.innerHTML = (gender[0] + gender[1]).toString() + " posts";
    amBarChart("u-tw-count", gender[0], gender[1]);
}