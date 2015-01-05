initialisePage();
getCurrUser();

var currUser;

function initialisePage() {
    $(document).ready(function () {
        addFriendsToContainer($("#friends-list-div"));
        // the key of the friend to be removed
        setupAndEventsModals();

    });
}
