initialisePage();
getCurrUser();

var currUser;

function initialisePage() {
    $(document).ready(function () {
        addFriendsToContainer($("#friends-list-div"));
        // the key of the friend to be removed
        var friendKey;
        setupAndEventsModals();

    });
}

function setupAndEventsModals()
{
      $('#add-debt-modal').on('shown.bs.modal', function(e) {
          var debtorName = $(e.relatedTarget).parent().parent().data('friend-name');
          $('#debtor').text(debtorName);
          $('#debtor').val(debtorName);
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
      var debtKey = $(e.relatedTarget).parent().parent().data('friend-key');
      $('#add-debt-btn').click(function() {
        addDebt(debtKey);
      });

    $('#delete-friend-modal').on('show.bs.modal', function(e) {
        var friendKey = $(e.relatedTarget).parent().parent().data('friend-key');
        $('#remove-friend-btn').click(function() {
            removeFriend(friendKey);
            $('[data-friend-key=' + friendKey + ']').remove();
        });
    });

    $('#add-friend-btn').click(function() {
        var newFriend = friends.newInstance({'email': $('#email').val()});
        newFriend.create();
    });
    $('#add-debt-btn').click(function() {
        addDebt();
    });
}

function addFriendsToContainer($container) {
    // var template = '<div class="user-container">' +
    //                   '<div class="pull-left"><img src="{{ ----- }}" class="img-rounded" width="25"><span style="font-size:16px">{{ user }}</span></div>' +
    //                   '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-trash"></i></button><button type="button" class="btn btn-default"><b>...</b></button></div>' +
    //                 '</div>';

    var template = '<div class="user-container" style="height:40px;" data-friend-key="{{key}}" data-friend-name="{{name}}">' +
        '<div class="pull-left"><img src="{{profilePicture}}" class="img-rounded" width="25"><span style="font-size:16px;" id="friend_"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.netAmount}}</span>)</div>' +
        '<div class="btn-group pull-right pay-button" role="group"><button type="button" class="btn btn-default" data-toggle="modal" data-target="#add-debt-modal"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#delete-friend-modal"><i class="glyphicon glyphicon-trash"></i></button><button type="button" class="btn btn-default" data-toggle="collapse" data-target="#moreinfo-{{num}}"><b>...</b></button> </div>' +
        '</div><hr style="margin-bottom:5px;" data-friend-key="{{key}}">' +
        '<div class="collapse moreinfo" id="moreinfo-{{num}}"><div class="panel panel-default"><div class="panel-body">' +
        '<div class="row summaryRow"><div class="summaryTitle"><h4>Debts</h4></div><div class="debts"></div></div>' +
        '<div class="row summaryRow"><div class="summaryTitle"><h4>Credits</h4></div><div class="credits"></div></div>' +
        '</div></div></div>';

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

            $container.append(processTemplate(template, data[i]));
        }
        $('div.moreinfo').on('show.bs.collapse', expandFriend);
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

function addDebt(debtorKey) {

    var amount = $('#amount').val();
    var date = $('#date').val();
    var description = $('#description').val();

    var debtParams = {'debtor': debtorKey,
                'creditor': currUser.key,
                'amount': parseInt(amount),
                'description': description,
                'isPaid': false,
                'created': date,
                'amountPaid': 0};

    var newDebt = debts.newInstance(debtParams);
    newDebt.create();
}

function getCurrUser() {
    user.getAll(function(success,data){
        if(success){
            console.log("users retrieved");
            console.log(data);
            currUser = data[0];
        }else{
            console.log("error");
            console.log(data);
        }
    });
}

