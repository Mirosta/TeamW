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
                        '<label for="debtor-check-{{readOnly.num}}">{{name}} {{familyName}}</label><input class="group-user" id="debtor-check-{{readOnly.num}}" data-user-key="{{key}}" type="checkbox">' +
                     '<div>';
                 lookupField({friends: ['users']}, data, function(success, data)
                 {
                     var $container = $('div.group-members');
                     $container.html()
                     for(var i =0; i < data.users.length; i++)
                     {
                         var curFriend = data.users[i];
                         curFriend.readOnly.num = i;
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
          $('#add-debt-btn').click(function(e) {
              addDebtToGroup(groupKey);
          })
    });

    $('#new-group-sbmt').click(function() {
       var newGroup = groups.newInstance({"name": $('#new-group-name').val()});
       newGroup.create(function (success, data) {
           if (success){
               location.reload();
           }
       });
       $('#create-group-modal').modal('hide')
    });

    $('#edit-group-modal').on('show.bs.modal', function(e) {
        var key = $(e.relatedTarget).parent().parent().data('group-key');
        var grp = null;
        var keys = [];
        groups.get(key, function(success, data) {
               if (success) {
                   grp = data;
                   $('#edit-group-name').val(grp.name);
                   var members = "";
                   var count = 0;
                   for (elem in grp.users) {
                       friends.get(grp.users[elem], function (success, usr) {
                          if (success) {
                              members += usr.email + ", ";
                              keys[usr.email] = usr.key;
                              count++;
                              if (count === grp.users.length) {
                                  $('#edit-group-members').val(members);
                              }
                          }
                       });
                   }
               }
        });
        $('#edit-group-sbmt').click(function(e) {
               grp.name = $('#edit-group-name').val();
               var emails = $('#edit-group-members').val().split(", ");
               var newkeys = [];
               friends.getAll(function (success, all) {
                  if (success) {
                      for (var i = 0; i < emails.length; i++) {
                          for (var j = 0; j < all.length; j++) {
                              if (emails[i] === all[j].email) {
                                  newkeys.push(all[j].key);
                                  break;
                              }
                          }
                      }
                      console.log(newkeys);
                      grp.users = newkeys;
                      grp.update(function (success, data){
                        if (success) {
                            location.reload();
                        }
                      });
                  }
               });
        });
        $('#remove-group-member-modal').on('show.bs.modal', function(e) {
            var groupKey = $(e.relatedTarget).data('groupKey');
            var memberKey = $(e.relatedTarget).data('key');

            $('#remove-group-member-btn').click(function() {
                removeGroupMember(groupKey, memberKey);
            });
            location.reload();
        });
    });
  });
}

function addGroupsToContainer() {
   var template = '<div class="group-container" style="height:40px;" data-group-key="{{key}}">' +
                    '<div class="pull-left"><span style="font-size:16px;"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.netAmount}}</span>)</div>' +
                    '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default" data-toggle="modal" data-target="#add-debt-modal"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#edit-group-modal"><i class="glyphicon glyphicon-edit"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#delete-modal"><i class="glyphicon glyphicon-trash"></i><button type="button" class="btn btn-default" data-toggle="collapse" data-target="#moreinfo-{{readOnly.num}}"><b>...</b></button></div>' +
                  '</div><hr style="margin-bottom:5px;" data-friend-key="{{key}}">' +
                 '<div class="collapse moreinfo" id="moreinfo-{{readOnly.num}}"><div class="panel panel-default"><div class="panel-body">' +
                '<div class="row summaryRow"><div class="summaryTitle" style="margin-left: 20px"><h4>friends</h4></div><div class="friends" style="margin-left: 20px">Loading...</div></div>' +
                '</div></div>';
  var groupsListDiv = $("#groups-list-div");

  groups.getAll(function(success, data) {
    console.log(data);
    groupsListDiv.html("");
    for (i=0; i<data.length; i++) {
      data[i].readOnly.numberClass = (data[i].readOnly.netAmount >= 0 ? "#26A65B" : "#CF000F");
      data[i].readOnly.netAmount = penceToPound(data[i].readOnly.netAmount);
      data[i].readOnly.num = i;
      groupsListDiv.append( processTemplate(template, data[i]) );
    }
    $('div.moreinfo').on('show.bs.collapse', expandGroup);
  });
}

function expandGroup(e)
{
    var $target = $(e.target);
    var groupKey = $target.prev().prev().data('group-key');
    var $friendContainer = $target.find("div.friends");
    console.log(e);

    var template = '<div class="user-container" style="height:40px;" data-friend-key="{{key}}" data-friend-name="{{name}}">' +
        '<div class="pull-left"><img src="{{profilePicture}}" class="img-rounded" width="25">' +
        '<span style="font-size:16px;" id="friend_"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">' +
        '{{readOnly.netAmount}}</span>)</div>' +
        '<div class="btn-group pull-right pay-button" role="group">' +
        '<button type="button" class="btn btn-default" data-toggle="modal"' +
        ' data-target="#remove-group-member-modal" data-member-key="{{key}}" data-group-key="{{groupKey}}">' +
        '<i class="glyphicon glyphicon-trash"></i></button>' +
        '</div>'

    prefix = "group-" + groupKey;
    groups.get(groupKey, function (success, data) {
        if(success){
            console.log(data);
            lookupField({friends: ["users"]}, data, function (success, data) {
                $friendContainer.html("");
                if(success)
                {
                    var friendsKeysArr = data.users;
                    for (i=0; i<friendsKeysArr.length; i++) {
                        friendsKeysArr[i].readOnly.numberClass = (friendsKeysArr[i].readOnly.netAmount >= 0 ? "#26A65B" : "#CF000F");
                        friendsKeysArr[i].readOnly.netAmount = penceToPound(friendsKeysArr[i].readOnly.netAmount);
                        friendsKeysArr[i].readOnly.prefix = prefix;
                        friendsKeysArr[i].readOnly.num = i;
                        if (friendsKeysArr[i].profilePicture === null) {
                            friendsKeysArr[i].profilePicture = "http://i.imgur.com/GTxcoJv.png";
                        }

                        $friendContainer.append(processTemplate(template, friendsKeysArr[i]));
                    }
                    if(friendsKeysArr.length === 0)
                    {
                        $friendContainer.html("Nothing here...");
                    }
                }
                else
                {
                    console.log("Error while looking up friends in group");
                    console.log(data);
                }
            });
        }
        else {
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

function removeGroupMember(groupKey, memberKey) {

    var memberKeyArr;

    groups.get(groupKey, function(success, data) {
        if(success){
            memberKeyArr = data.users;
            for (i=0; i<memberKeyArr.length; i++){
                if(memberKeyArr[i] === memberKey){
                    memberKeyArr.splice(i, 1);
                }
            }
            data.users = memberKeyArr;
            data.update(function(success, data) {
                    if(success)
                    {
                        location.reload();
                    }
                    else
                    {
                        console.log("Error while removing group member");
                        console.log(data);
                    }
                });
        }else{
          console.log(data);
        }
    })

}

function addDebtToGroup(groupKey)
{
    user.getAll(function (success, data) {
            if(success)
            {
                var currUser = data[0];
                var addingFriends = [];
                $('input.group-user').each(function() {
                        if(this.checked) addingFriends.push($(this).data('user-key'));
                    });
                if(addingFriends.length > 0) {
                    var synch = new Synchronise(addingFriends.length, function(success, data) { console.log("done"); /*location.reload();*/ } );
                    var total = Math.floor(parseFloat($("#amount").val()) * 100);
                    var amount = Math.floor(total / (addingFriends.length + 1));
                    var remainder = total % (addingFriends.length + 1);
                    var date = $('#date').val();
                    var description = $('#description').val();
                    var randomPerson = Math.floor(Math.random() * (addingFriends.length + 1));
                    for(var i = 0; i < addingFriends.length; i++) {
                         var debtParams = {'debtor': addingFriends[i],
                            'creditor': currUser.key,
                            'amount': amount + (i === randomPerson ? remainder : 0),
                            'description': description,
                            'disputed': false,
                            'dateOf': date + " 00:00:00"};
                        var newDebt = debts.newInstance(debtParams);
                        newDebt.create(function(success, data) {
                                console.log(data);
                                synch.complete();
                                if(!success)
                                {
                                    console.log("Error adding debt to friend " + i);
                                }
                            });
                    }
                }
            }
            else
            {
                console.log("Error getting current user");
                console.log(data);
            }
        }
    );
}