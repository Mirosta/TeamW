initialisePage();

function initialisePage() {
  $(document).ready(function () {
    addGroupsToContainer();

    $('#delete-modal').on('show.bs.modal', function(e) {
        groupKey = $(e.relatedTarget).parent().parent().data('group-key');
        $('#remove-group-btn').click(function() {
            removeGroup(groupKey);
            $('[data-group-key=' + groupKey + ']').remove();
            $('#delete-modal').modal('hide');
        });
    });

    $('#add-debt-modal').on('shown.bs.modal', function(e) {
          var groupKey = $(e.relatedTarget).parent().parent().data('group-key');
          groups.get(groupKey, function(success, data)
          {
             if(success)
             {
                 var template =
                     '<div>' +
                        '<label for="debtor-check-{{readOnly.num}}">{{name}} {{familyName}}</label><input id="debtor-check-{{readOnly.num}}" data-user-key="{{key}}" type="checkbox">' +
                     '<div>';
                 lookupField({friends: ['users']}, data, function(success, data)
                 {
                     for(var i =0; i < data.users.length; i++)
                     {
                         var curFriend = data.users[i];
                         curFriend.readOnly.num = i;
                         var $container = $('div.group-members');
                         $container.append($(processTemplate(template, curFriend)));
                     }
                 });
             }
          });
          //datepicker for date of debt input field
          var date = new Date();
          var day = date.getDate();
          var month = date.getMonth() + 1;
          var year = date.getFullYear();

          $('#date').val( year + "-" + month + "-" + day);
          $('#date').datepicker({dateFormat: "yy-mm-dd", showButtonPanel: true});
    });

    $('#new-group-sbmt').click(function() {
       var newGroup = groups.newInstance({"name": $('#new-group-name').val()});
       newGroup.create(function (success, data) {
           if (success){
               location.reload();
           }
       });
       $('#create-group-modal').modal('hide');
    });
  });
}

function addGroupsToContainer() {
   var template = '<div class="group-container" style="height:40px;" data-group-key="{{key}}">' +
                    '<div class="pull-left"><span style="font-size:16px;"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.netAmount}}</span>)</div>' +
                    '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default" data-toggle="modal" data-target="#add-debt-modal"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#edit-modal"><i class="glyphicon glyphicon-edit"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#delete-modal"><i class="glyphicon glyphicon-trash"></i><button type="button" class="btn btn-default" data-toggle="collapse" data-target="#moreinfo-{{num}}"><b>...</b></button></div>' +
                  '</div><hr style="margin-bottom:5px;" data-friend-key="{{key}}">' +
                 '<div class="collapse moreinfo" id="moreinfo-{{num}}"><div class="panel panel-default"><div class="panel-body">' +
                '<div class="row summaryRow"><div class="summaryTitle"><h4>friends</h4></div><div class="friends"></div></div>' +
                '</div></div>';
                    '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default" data-toggle="modal" data-target="#add-debt-modal"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#edit-group-modal"><i class="glyphicon glyphicon-edit"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#delete-modal"><i class="glyphicon glyphicon-trash"></i></button><button type="button" class="btn btn-default"><b>...</b></button> </div>' +
                  '</div><hr style="margin-bottom:5px;">';
  var groupsListDiv = $("#groups-list-div");
  groupsListDiv.html("");

  groups.getAll(function(success, data) {
    console.log(data);
    for (i=0; i<data.length; i++) {
      data[i].readOnly.numberClass = (data[i].readOnly.netAmount >= 0 ? "#26A65B" : "#CF000F");
      data[i].readOnly.netAmount = penceToPound(data[i].readOnly.netAmount);
      groupsListDiv.append( processTemplate(template, data[i]) );
    }
    $('div.moreinfo').on('show.bs.collapse', expandGroup);
  });
}

function expandGroup(e)
{
    var $target = $(e.target);
    var groupKey = $target.parent().children().first().data('group-key');
    var $friendContainer = $target.find("div.friends");
    console.log(e);

    var template = '<div class="friends-container"><div class="col-md-3"><span style="font-size:16px;" id="friend"> {{name}}</span><br> ' +
                           '<hr style="margin-bottom:5px;">' +
                           '</div></div>';
    $friendContainer.html("");

    groups.get(groupKey, function (success, data) {
        if(success){
            console.log(data);
            var friendsKeysArr = data.users;
            console.log(friendsKeysArr.toString());
            for (i=0; i<friendsKeysArr.length; i++){
                friends.get(friendsKeysArr[i], function (success, data) {
                    if(success){
                        console.log(data);
                        $friendContainer.append(processTemplate(template, {'name' : data.name}));
                    }
                });

            }
        }else{
            console.log("failed");
             console.log(data);
        }

    });
}

function removeGroup(key) {
  groups.get(key, function(success, data) {
      if (success) {
          console.log("got group");
          console.log(data);
          data.remove(function(success, data) {
              if (!success) {
                  console.log("error");
                  console.log(data);
              }
          });
      } else {
          console.log(data);
      }
  });
}
