// Load groups
initialisePage();

function initialisePage() {
  loadGroupsIntoDashboard();
}

function loadGroupsIntoDashboard() {
  groups.getAll(function(success, data) {
    var groupData = data[0];
    console.log(groupData);
    $('#groups-content-div').html("");
    $('#groups-content-div').append(
      '<div>' + groupData.name +
      ' <span class="pull-right bold" style="color:#26A65B;">' + groupData.readonly.netAmount + '</span><br>' +
      '</div>');
  });
}

function loadFriendsIntoDashboard() {
  friends.getAll(function(success, data) {
    var friendData = data[0];
    console.log(friendData);
    $('#friends-content-div').html("");
    $('#friends-content-div').append(
      '<div>' + friendData.name +
      ' <span class="pull-right bold" style="color:#26A65B;">' + friendData.readonly.netAmount + '</span><br>' +
      '</div>');
  });
}
