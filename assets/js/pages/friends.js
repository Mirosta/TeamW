initialisePage();

function initialisePage() {
  $(document).ready(function () {
    addFriendsToContainer();
  });
}

function addFriendsToContainer() {
    // var template = '<div class="user-container">' +
    //                   '<div class="pull-left"><img src="{{ ----- }}" class="img-rounded" width="25"><span style="font-size:16px">{{ user }}</span></div>' +
    //                   '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-trash"></i></button><button type="button" class="btn btn-default"><b>...</b></button></div>' +
    //                 '</div>';

    var template = '<div class="user-container" style="height:40px;">' +
        '<div class="pull-left"><img src="{{profilePicture}}" class="img-rounded" width="25"><span style="font-size:16px;" id="friend_"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.netAmount}}</span>)</div>' +
        '<div class="btn-group pull-right pay-button" role="group"><button type="button" class="btn btn-default" data-toggle="modal" data-target="#add-debt-modal"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#delete-modal" data-friend-key="{{key}}" id="{{key}}"><i class="glyphicon glyphicon-trash"></i></button><button type="button" id="more" class="btn btn-default"><b>...</b></button> </div>' +
        '</div><hr style="margin-bottom:5px;">';
    var friendsListDiv = $("#friends-list-div");
    friendsListDiv.html("");

    friends.getAll(function (success, data) {
        console.log(data);
        for (i = 0; i < data.length; i++) {
            data[i].readOnly.numberClass = (data[i].readOnly.netAmount >= 0 ? "#26A65B" : "#CF000F");
            data[i].readOnly.netAmount = penceToPound(data[i].readOnly.netAmount);
            if (data[i].profilePicture === null) {
                data[i].profilePicture = "http://i.imgur.com/GTxcoJv.png";
            }

            friendsListDiv.append(processTemplate(template, data[i]));
        }
        $('div.user-container').on("click", "#more", expandFriend);
    });}

function removeFriend(key){

    friends.get(key, function(success, data) {
        if(success){
            console.log("got friend");
            console.log(data);
            data.remove(function(success, data) {
                if (!success) {
                    console.log("error");
                    console.log(data);
                }
            });
        }else{
            console.log("error");
            console.log(data);
        }
    });
}
