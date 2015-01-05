initialisePage();

function initialisePage() {
  dumpRequests()
}

function dumpRequests() {
  friendsRequests.getAll(function(success, data) {

    var template = '<div class="user-container" data-friend-key="{{key}}" style="height:40px;">' +
        '<div class="pull-left"><img src="{{profilePicture}}" class="img-rounded" width="25"><span style="font-size:16px;" id="friend_"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.netAmount}}</span>)</div>' +
        '<div class="btn-group pull-right pay-button" role="group"><button type="button" class="accept btn btn-default"><i class="icon-plus-sign-alt"></i> </button> <button type="button" class="btn btn-default"> <i class="glyphicon glyphicon-trash"></i> </button> </div>' +
        '</div><hr style="margin-bottom:5px;">'

    console.log(data);
    var maxLength = (data.length >= 11) ? 10 : data.length;
    for(i=0; i < maxLength; i++) {
      $("#friend-requests").append( processTemplate(template, data[i]) );
    }
    $('button.accept').click( function (e) {
      var friendKey = $(e.currentTarget).parent().data('friend-key');
      var newFriend = friends.newInstance({"key": friendKey});
      newFriend.create();
    })
  });
}