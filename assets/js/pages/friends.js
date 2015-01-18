initialisePage();
getCurrUser();

var currUser;

function initialisePage() {
    $(document).ready(function () {
        friends.getAll(function (success, data) {
            console.log(data);
            if(success)
            {
                addFriendsToContainer($("#friends-list-div"), data);
            }
        });
        // the key of the friend to be removed
        setupAndEventsModals();

    });
}
