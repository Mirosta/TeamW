
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