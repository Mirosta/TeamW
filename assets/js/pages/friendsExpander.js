
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

          $('#date').val( year + "-" + month + "-" + day);
          $('#date').datepicker({dateFormat: "yy-mm-dd", showButtonPanel: true});
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
      $('#add-debt-btn').click(function(e) {
          var debtKey = $(e.relatedTarget).parent().parent().data('friend-key');
          addDebt(debtKey);
      });

    $('#delete-friend-modal').on('show.bs.modal', function(e) {
        var friendName = $(e.relatedTarget).parent().parent().data('friend-name');
        $('#friend-to-remove').text(friendName);
        var friendKey = $(e.relatedTarget).parent().parent().data('friend-key');
        $('#remove-friend-btn').click(function() {
            removeFriend(friendKey);
            $('[data-friend-key=' + friendKey + ']').remove();
            return true;
        });
    });

    $('#add-friend-btn').click(function() {
        var newFriend = friends.newInstance({'email': $('#email').val()});
        newFriend.create();
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
                'disputed': false,
                'created': date + " 00:00:00"};

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

function expandFriend(e)
{
    var $target = $(e.target);
    var friendKey = $target.parent().children().first().data('friend-key');
    var $debtContainer = $target.find("div.debts");
    var $creditContainer = $target.find("div.credits");
    console.log(e);

    friends.get(friendKey, function (success, data) {
        if(success)
        {
            lookupField({debts: ['readOnly.credits', 'readOnly.debts']}, data, function(success, data)
            {
                var template = '<div class="debt-container"><div class="col-md-3"><span style="font-size:16px;" id="friend_"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.amountRemaining}}</span>)</div><div class="col-md-3">{{created}}</div><div class="col-md-3"><span style="color:{{readOnly.statusColor}};" "class="glyphicon {{readOnly.statusClass}}"></span></div>' +
                    '<div class="btn-group pull-right pay-button" role="group">{{readOnly.buttonHtml}}</div>' +
                    '</div>';
                var debtButton = '<button type="button" class="btn btn-default" data-toggle="modal" data-target="#add-debt-modal"><i class="glyphicon glyphicon-gbp"></i></button>';
                var creditButton = '<button type="button" class="btn btn-default" data-toggle="modal" data-target="#delete-modal"><i class="glyphicon glyphicon-remove-circle"></i></button>';
                outputDebts(data.readOnly.debts, $debtContainer, "#CF000F", "#26A65B", template, debtButton);
                outputDebts(data.readOnly.credits, $creditContainer, "#26A65B", "#CF000F", template, creditButton);
            });
        }
    });
}

function getColor(disputed, paid)
{
    if(disputed) return 'red';
    else if(!paid) return 'orange';
    else return 'green';
}

function getGlyph(disputed, paid)
{
    if(disputed) return "glyphicon-exclamation-sign";
    else if(!paid) return "glyphicon-question-sign";
    else return "glyphicon-ok-sign";
}

function outputDebts(debtArray, $container, positiveColour, negativeColour, template, button)
{
    for(var i = 0; i < debtArray.length; i++)
    {
        var curDebt = debtArray[i];
        var paid = curDebt.readOnly.amountRemaining <= 0;
        curDebt.readOnly.numberClass = (curDebt.readOnly.amountRemaining >= 0 ? positiveColour : negativeColour);
        curDebt.readOnly.amountRemaining = penceToPound(curDebt.readOnly.amountRemaining);
        curDebt.readOnly.statusClass = getGlyph(curDebt.disputed, paid);
        curDebt.readOnly.statusColor = getColor(curDebt.disputed, paid);
        curDebt.readOnly.buttonHtml = processTemplate(button, curDebt);
        $container.append($(processTemplate(template, curDebt)));
    }
    if(debtArray.length === 0)
    {
        $container.append($('<div class="debt-container"><div class="col-md-9 no-debts">nothing here...</div><div>'));
    }
}