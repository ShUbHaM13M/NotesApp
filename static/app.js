loggedIn = $('#logged-in');

if (loggedIn) {
    var userFirstInitial = loggedIn.text()

    loggedIn.text(userFirstInitial[0].toUpperCase());
}
