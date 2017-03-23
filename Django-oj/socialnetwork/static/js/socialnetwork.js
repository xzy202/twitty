// Sends a new request to update the to-do list
function getList() {
    $.ajax({
        url: "/socialnetwork/get-list-json",
        dataType : "json",
        success: updateList
    });
}

function updateComment(response){

        items = response
        console.log(items)
	append_len = items.length
        postid = items[0]["fields"]["postid"]
        var old_list = document.getElementById("comments"+postid);
        var li_len = old_list.getElementsByTagName("div").length;     
        // console.log(old_list)
        // console.log(li_len)  
        // console.log(append_len / 3)
        start = li_len * 3
        for ( i = start ; i < append_len ; i = i + 3){

            id = items[i]["fields"]["user"]
            entryid = items[i+2]["pk"]        
            console.log(id)
	    console.log(entryid)         
            timestamp = items[i]["fields"]["timestamp"]
            time = new Date(timestamp);
            // console.log(timestamp)
            picture = items[i+2]["fields"]["picture"]
            // console.log(picture)
            username = items[i+1]['fields']['username']
            // console.log(username)
            comment = items[i]["fields"]["comment"]
             $("#comments" + postid).append(
                "<div><img class='viewprofile' src= '/socialnetwork/photo/" + entryid +" '> " +
                "<a href='/socialnetwork/viewprofile/" + id+ " '> " + username +" </a> " +
                "<p1>" + time +"</p1><br><br><p4>"+
                 sanitize(comment)+          
                 "</p4></div>")
         }
}

function updateList(items) {
    // Removes the old to-do list items

    var old_list = document.getElementById("showpost");
    var li_len = old_list.getElementsByTagName("li").length;
    // console.log(li_len)
    // $('#box3 li').remove();
    // $('#showpost li').remove();
    // $('#container li').remove();
    item_len = items.length;
    total_list = item_len / 3;
    // console.log(item_len / 3)
    append_len = item_len / 3 - li_len
    // add = total_len / 3 - tag ;
    // console.log(tag)
    // console.log(total_len / 3)

        for ( i = 0; i < append_len * 3; i = i + 3){
            // console.log("append"+ i / 3)
            id = items[i]["fields"]["user"]
            entryid = items[i+2]["pk"]
	    console.log(i)
            console.log(entryid)

            postid = items[i]["pk"]

            timestamp = items[i]["fields"]["timestamp"]
            time = new Date(timestamp);
            // console.log(timestamp)
            picture = items[i+1]["fields"]["picture"]
            // console.log(picture)
            username = items[i+2]['fields']['username']
            // console.log(username)
            text = items[i]["fields"]["text"]
            // console.log(text)

             $("#showpost").prepend(
                "<li><div id = 'showpost" + postid + "'>" +             
                "<img class='viewprofile' src= '/socialnetwork/photo/" + entryid +" '> " +
                "<a href='/socialnetwork/viewprofile/" + id+ " '> " + username +" </a> " +
                "<p1>" + time +"</p1><br>"+
                "<p><p2>"+sanitize(text)+ "</p2></p></div><br>"+
                "<button id = '"+ postid+ "' onclick='getComment( " + postid + ")' >ViewCommnts</button>"+           
                "<div id='comments"+postid +"'></div>"+    
                 "comment : <input class='Addcomment' id='comment"+ postid + "'type='text'>"+
                 "<button id = '"+ postid+ "' onclick='addComment( " + postid + ")' >AddComments</button>"+
                 
                 "</li>")
         }

         get_comments_json(total_list)
}

function get_comments_json(total_list) {

    for ( postid = 1 ; postid <= total_list ; postid ++){
        getComment(postid)
    }
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    $("#error").html(message);
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}


function getComment(id){

    $.ajax({
        url: "/socialnetwork/get-comment-json/"+id,
        type: "GET",
        dataType : "json",
        success: showComment
    });
}


function showComment(items){
        // console.log(items.length)
        append_len = items.length
        if (append_len !== 0){
            postid = items[0]["fields"]["postid"]
            // postid = items[0]["pk"]
            var old_list = document.getElementById("comments"+postid);
            var li_len = old_list.getElementsByTagName("div").length;     
            // console.log(old_list)
            // console.log(li_len)  
            // console.log(append_len / 3)
            start = li_len * 3
            for ( i = start ; i < append_len ; i = i + 3){

                id = items[i]["fields"]["user"]
                entryid = items[i+2]["pk"]
                timestamp = items[i]["fields"]["timestamp"]
                time = new Date(timestamp);
                // console.log(timestamp)
                picture = items[i+2]["fields"]["picture"]
                // console.log(picture)
                username = items[i+1]['fields']['username']
                // console.log(username)
                comment = items[i]["fields"]["comment"]
                 $("#comments" + postid).append(
                    "<div><img class='viewprofile' src= '/socialnetwork/photo/" + entryid +" '> " +
                    "<a href='/socialnetwork/viewprofile/" + id+ " '> " + username +" </a> " +
                    "<p1>" + time +"</p1><br><br><p4>"+
                     sanitize(comment)+          
                     "</p4></div>")
             }
     }

}


function addComment(id) {
    var itemTextElement = $("#comment"+id);
    var itemTextValue   = itemTextElement.val();

    // console.log(itemTextValue)
    // Clear input box and old error message (if any)
    itemTextElement.val('');
    displayError('');
    
    $.ajax({
        url: "/socialnetwork/add-comment/"+id,
        type: "POST",
        data: "item="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updateComment(response);
            } else {
                displayError(response.error);
            }
        }
    });
}

function deleteItem(id) {
    $.ajax({
        url: "/jquery-todolist/delete-item/"+id,
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: updateList
    });
}

// The index.html does not load the list, so we call getList()
// as soon as page is finished loading
window.onload = getList;

// causes list to be re-fetched every 5 seconds
window.setInterval(getList, 5000);
