initialisePage();

function initialisePage() {
  dumpRequests()
}

function dumpRequests() {
  friendRequests.getAll(function(success, data) {

    var template = '<div class="user-container" data-friend-key="{{key}}" style="height:40px;">' +
        '<div class="pull-left"><img src="{{profilePicture}}" class="img-rounded" width="25"><span style="font-size:16px;" id="friend_"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.netAmount}}</span>)</div>' +
        '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default accept"><span class="glyphicons glyphicons-gbp"> </span> </button> <button type="button" class="btn btn-default reject"> <span class="glyphicon glyphicon-trash"> </span> </button> </div>' +
        '</div><hr style="margin-bottom:5px;">'

    console.log(data);
    var maxLength = (data.length >= 11) ? 10 : data.length;

    if (maxLength == 0) {
      $("#friend-requests").append( "You have no friend requests." );
    }

    for(i=0; i < maxLength; i++) {
      $("#friend-requests").append( processTemplate(template, data[i]) );
    }
    $('button.accept').click( function (e) {
      var friendKey = $(e.currentTarget).parent().parent().data('friend-key');
      var newFriend = friends.newInstance({"key": friendKey});
      newFriend.create();
      })
  });
}