initialisePage();

function initialisePage() {
  $(document).ready(function () {
    addFriendsToContainer();
     // the key of the friend to be removed
      var friendKey;
    $('#add-debt-modal').on('shown.bs.modal', function() {
      //datepicker for date of debt input field
      var date = new Date();
      var day = date.getDate();
      var month = date.getMonth() + 1;
      var year = date.getFullYear();

      $('#date').val( day + "/" + month + "/" + year);
      $('#date').datepicker({dateFormat: "dd/mm/yy", showButtonPanel: true});
    });

   //character counter for debt description
    $('#description').keyup(function() {
        var max = parseInt($(this).attr("maxlength"));
        var count = $(this).val().length;
        if(count >= max) {
            $('#chars-left').text("0 characters left");
        } else {
            var remaining =  max - count;
            $('#chars-left').text(remaining + " characters left");
        }
    });

    $('#delete-modal').on('show.bs.modal', function(e) {
        friendKey = $(e.relatedTarget).parent().parent().data('friend-key');
        $('#remove-friend-btn').click(function() {
            removeFriend(friendKey);
        })
    });
    $('#delete-modal').on('hidden.bs.modal', function() {
        $('[data-friend-key=' + friendKey + ']').remove();
    });


    $('#submit').click(function() {
        var newFriend = friends.newInstance({'email': $('#email').val()});
        newFriend.create();
    });
  });
}

function addFriendsToContainer() {
    // var template = '<div class="user-container">' +
    //                   '<div class="pull-left"><img src="{{ ----- }}" class="img-rounded" width="25"><span style="font-size:16px">{{ user }}</span></div>' +
    //                   '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-trash"></i></button><button type="button" class="btn btn-default"><b>...</b></button></div>' +
    //                 '</div>';

    var template = '<div class="user-container" style="height:40px;" data-friend-key="{{key}}">' +
        '<div class="pull-left"><img src="{{profilePicture}}" class="img-rounded" width="25"><span style="font-size:16px;" id="friend_"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.netAmount}}</span>)</div>' +
        '<div class="btn-group pull-right pay-button" role="group"><button type="button" class="btn btn-default" data-toggle="modal" data-target="#add-debt-modal"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#delete-modal"><i class="glyphicon glyphicon-trash"></i></button><button type="button" id="more" class="btn btn-default" data-toggle="collapse" data-target="#moreinfo-{{num}}"><b>...</b></button> </div>' +
        '</div><hr style="margin-bottom:5px;" data-friend-key="{{key}}">' +
        '<div class="collapse moreInfo" id="moreInfo-{{num}}"><div class="panel panel-default"><div class="panel-body">Test<!--<div class="row">Debts</div><div class="row">Credits</div>--></div></div></div>';

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

            data[i].num = i;

            friendsListDiv.append(processTemplate(template, data[i]));
        }
        //$('div.moreInfo').on('show.bs.collapse', expandFriend);
    });}

function removeFriend(key) {

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

function populateDebtorDropdown() {

    users.getAll()
}
