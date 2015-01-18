
function setupAndEventsModals()
{
      $('#add-debt-modal').on('shown.bs.modal', function(e) {
          var debtorName = $(e.relatedTarget).parent().parent().data('friend-name');
          var debtKey = $(e.relatedTarget).parent().parent().data('friend-key');

          $('#debtor').text(debtorName);
          $('#debtor').val(debtorName);
          //datepicker for date of debt input field
          var date = new Date();
          var day = date.getDate();
          var month = date.getMonth() + 1;
          var year = date.getFullYear();

          $('#date').val( year + "-" + month + "-" + day);
          $('#date').datepicker({dateFormat: "yy-mm-dd", showButtonPanel: true});
          $('#add-debt-btn').click(function(e) {
          addDebt(debtKey);
          });
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

function addFriendsToContainer($container, friends, prefix) {
    // var template = '<div class="user-container">' +
    //                   '<div class="pull-left"><img src="{{ ----- }}" class="img-rounded" width="25"><span style="font-size:16px">{{ user }}</span></div>' +
    //                   '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-trash"></i></button><button type="button" class="btn btn-default"><b>...</b></button></div>' +
    //                 '</div>';
    if(prefix === null || prefix === undefined) prefix = ""

    var template = '<div class="user-container" style="height:40px;" data-friend-key="{{key}}" data-friend-name="{{name}}">' +
        '<div class="pull-left"><img src="{{profilePicture}}" class="img-rounded" width="25">' +
        '<span style="font-size:16px;" id="friend_"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">' +
        '{{readOnly.netAmount}}</span>)</div>' +
        '<div class="btn-group pull-right pay-button" role="group">' +
        '<button type="button" class="btn btn-default" data-toggle="modal" data-target="#add-debt-modal">' +
        '<i class="glyphicon glyphicon-gbp"></i></button>' +
        '<button type="button" class="btn btn-default" data-toggle="modal" data-target="#delete-friend-modal">' +
        '<i class="glyphicon glyphicon-trash"></i>' +
        '</button>' +
        '<button type="button" class="btn btn-default" data-toggle="collapse" data-target="#{{readOnly.prefix}}-moreinfo-{{readOnly.num}}"><b>...</b></button> </div>' +
        '</div><hr style="margin-bottom:5px;" data-friend-key="{{key}}">' +
        '<div class="collapse moreinfo" id="{{readOnly.prefix}}-moreinfo-{{readOnly.num}}"><div class="panel panel-default"><div class="panel-body">' +
        '<div class="row summaryRow"><div class="summaryTitle"><h4>debts</h4></div><div class="debts">Loading...</div></div>' +
        '<div class="row summaryRow"><div class="summaryTitle"><h4>credits</h4></div><div class="credits">Loading...</div></div>' +
        '</div></div></div>';

    $container.html("");
            for (i = 0; i < friends.length; i++) {
                friends[i].readOnly.numberClass = (friends[i].readOnly.netAmount >= 0 ? "#26A65B" : "#CF000F");
                friends[i].readOnly.netAmount = penceToPound(friends[i].readOnly.netAmount);
                friends[i].readOnly.prefix = prefix;
                friends[i].readOnly.num = i;
                if (friends[i].profilePicture === null) {
                    friends[i].profilePicture = "http://i.imgur.com/GTxcoJv.png";
                }

                $container.append(processTemplate(template, friends[i]));
            }
            $('div.moreinfo').on('show.bs.collapse', expandFriend);
}

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

function removeDebt(key) {
    debts.get(key, function(success, data) {
        console.log(data);
        if(success)
        {
            data.remove(function(success, data) {
                if(success)
                {
                    location.reload();
                }
                else
                {
                    console.log("Error removing debt");
                    console.log(data);
                }
            });
        }
    });
}

function addDebt(debtorKey) {

    var amount = $('#amount').val();
    var date = $('#date').val();
    var description = $('#description').val();

    var debtParams = {'debtor': debtorKey,
                'creditor': currUser.key,
                'amount': parseFloat(amount) * 100,
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
    var friendKey = $target.prev().prev().data('friend-key');
    var $debtContainer = $target.find("div.debts");
    var $creditContainer = $target.find("div.credits");
    console.log(e);

    friends.get(friendKey, function (success, data) {
        if(success)
        {
            lookupField({debts: ['readOnly.credits', 'readOnly.debts']}, data, function(success, data)
            {
                var template = '<div class="debt-container" data-debt-key={{key}}><div class="col-md-3"><span style="font-size:16px;" id="friend_"> {{description}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.amountRemaining}}</span>)</div><div class="col-md-3">{{created}}</div><div class="col-md-3"><span style="color:{{readOnly.statusColor}};" class="glyphicon {{readOnly.statusClass}}"></span></div>' +
                    '<div class="btn-group pull-right pay-button" role="group">{{readOnly.buttonHtml}}</div>' +
                    '</div>';

                console.log(data);

                var debtButton = '<button type="button" class="btn btn-default" data-toggle="modal" data-target="#add-payment-modal"><i class="glyphicon glyphicon-gbp"></i></button>';
                var creditButton = '<button type="button" class="btn btn-default" data-toggle="modal" data-target="#delete-debt-modal"><i class="glyphicon glyphicon-remove-circle"></i></button>';
                $('#add-payment-modal').on('show.bs.modal', function(e) {
                    var debtKey = $(e.relatedTarget).parent().parent().data('debt-key');
                    console.log(e);
                    console.log(debtKey);

                    $('button.submitPayment').click(function (e) {
                        user.getAll(addPayment);
                    });
                });
                $('#delete-debt-modal').on('show.bs.modal', function(e) {
                    var debtKey = $(e.relatedTarget).parent().parent().data('debt-key');
                    console.log(e);
                    console.log(debtKey);

                    $('#remove-debt-btn').click(function (e) {
                        removeDebt(debtKey);
                    });
                });
                outputDebts(data.readOnly.debts, $debtContainer, "#CF000F", "#26A65B", template, debtButton);
                outputDebts(data.readOnly.credits, $creditContainer, "#26A65B", "#CF000F", template, creditButton);
            });
        }
    });
}

function addPayment(success, data)
{
    if(success)
    {
        var amount = $('input#paymentAmount').val();
        var description = $('textarea#paymentDescription').val();
        var payment = payments.newInstance({
            "debt": debtKey,
            "amount": parseFloat(amount) * 100,
            "description": description,
            "payer": data[0].key
        });
        payment.create(function(success, data) {
                console.log(data);
                if(success) location.reload();
            });
    }
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
    $container.html("");
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