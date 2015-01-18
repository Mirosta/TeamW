initialisePage();

function initialisePage() {
  dumpRequests()
}

function dumpRequests() {
  friendRequests.getAll(function(success, data) {

    var template = '<div class="user-container" data-friend-key="{{key}}" style="height:40px;">' +
        '<div class="pull-left"><img src="{{profilePicture}}" class="img-rounded" width="25"><span style="font-size:16px;" id="friend_"> {{name}}</span></div>' +
        '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default accept"><i class="glyphicon glyphicon-user"></i></button> </div>' +
        '</div><hr style="margin-bottom:5px;">'

    console.log(data);
    var maxLength = (data.length >= 11) ? 10 : data.length;

    $("#friend-requests").html("");

    if (maxLength == 0) {
      $("#friend-requests").append( "You have no friend requests." );
    }

    for(i=0; i < maxLength; i++) {
      $("#friend-requests").append( processTemplate(template, data[i]) );
    }

    $('button.accept').click( function (e) {
      var friendKey = $(e.currentTarget).parent().parent().data('friend-key');
      friendAccepted(friends.newInstance({"key": friendKey}), $(e.currentTarget));
      });
  });
}

function friendAccepted(newFriend, $button) {
  //friends.newInstance({"key": friendKey});
  $button.attr('disabled', 'disabled')
  $button.parent().parent().addClass("accepted")
  newFriend.create(function(success, data) {
        if(success, data)
        {
            dumpRequests();
        }
        else
        {
            console.log("Error while accepting friend request");
            console.log(data);
            $button.removeAttr('disabled');
        }
    });
}