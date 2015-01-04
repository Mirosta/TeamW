initialisePage();

function initialisePage() {
  $(document).ready(function () {
    addFriendsToContainer();
  });
}

function addFriendsToContainer() {
  // var template = '<div class="user-container">' +
  //                   '<div class="pull-left"><img src="{{ ----- }}" class="img-rounded" width="25"><span style="font-size:16px">{{ user }}</span></div>' +
  //                   '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-trash"></i></button><button type="button" class="btn btn-default"><b>...</b></button></div>' +
  //                 '</div>';

   var template = '<div class="user-container" style="height:40px;">' +
                    '<div class="pull-left"><img src="{{profilePicture}}" class="img-rounded" width="25"><span style="font-size:16px;"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.netAmount}}</span>)</div>' +
                    '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-trash"></i></button><button type="button" class="btn btn-default"><b>...</b></button> </div>' +
                  '</div><hr style="margin-bottom:5px;">';
  var friendsListDiv = $("#friends-list-div");
  friendsListDiv.html("");

  friends.getAll(function(success, data) {
    console.log(data);
    for (i=0; i<data.length; i++) {
      data[i].readOnly.numberClass = (data[i].readOnly.netAmount >= 0 ? "#26A65B" : "#CF000F");
      if (data[i].profilePicture === null) {
        data[i].profilePicture = "http://i.imgur.com/GTxcoJv.png";
      } 
      friendsListDiv.append( processTemplate(template, data[i]) );
    }
  });
}              
